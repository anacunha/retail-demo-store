<template>
  <Layout>
    <div class="container">
      <div id="markmap" class="location-map"></div>

      <LocationList :locations="locations" :changeViewport="setViewport" />
    </div>
  </Layout>
</template>

<script>
import { mapState } from 'vuex';

import { RepositoryFactory } from '@/repositories/RepositoryFactory';

import Layout from '@/components/Layout/Layout';
import LocationList from '@/components/Locations/LocationList';

import maplibregl from "maplibre-gl";
import { Auth } from "aws-amplify";
import location from "aws-sdk/clients/location";
import { Signer } from "@aws-amplify/core";

const LocationsRepository = RepositoryFactory.get('locations');

export default {
  name: 'Main',
  components: {
    Layout,
    LocationList
  },
  data() {
    return {
      credentials: null,
      service: null,
      locations: [],
      center: null,
      zoom: null,
      markers: [],
      map: null
    };
  },
  computed: {
    ...mapState({ user: (state) => state.user }),
  },
  async mounted() {
    this.credentials = await Auth.currentCredentials();
    this.service = new location({
        credentials: this.credentials,
        region: process.env.VUE_APP_AWS_REGION,
    });
    await this.getLocations();
    this.initializeMap();
  },
  methods: {
    transformRequest(url,resourceType){
        if (resourceType === "Style" && !url.includes("://")) {
            // resolve to an AWS URL
            url = "https://maps.geo." + process.env.VUE_APP_AWS_REGION + ".amazonaws.com/maps/v0/maps/" + url +"/style-descriptor";
        }
        if (url.includes("amazonaws.com")) {
            // only sign AWS requests (with the signature as part of the query string)
            return {
                url: Signer.signUrl(url, {
                    access_key: this.credentials.accessKeyId,
                    secret_key: this.credentials.secretAccessKey,
                    session_token: this.credentials.sessionToken,
                }),
            };
        }
        // Don't sign
        return { url: url || "" };
    },
    async getLocations() {
      let locationsResult = await LocationsRepository.get();
      this.locations = locationsResult.data;
    },
    async initializeMap() {
      if (this.locations && this.locations.length != 0) {
        this.center = new maplibregl.LngLat(this.locations[0].Longitude, this.locations[0].Latitude)
        this.zoom = 9
      }
      else {
        // The Venetian Resort
        this.center = new maplibregl.LngLat(-115.170227, 36.121159)
        this.zoom = 18
      }

      this.map = new maplibregl.Map({
            container: "markmap",
           //Specify the centre of the map when it gets rendered
            center: this.center,
            zoom: this.zoom, //Adjust the zoom level
            style: process.env.VUE_APP_LOCATION_RESOURCE_NAME,
            transformRequest: this.transformRequest
        });
        //Zoom in and out button
        this.map.addControl(new maplibregl.NavigationControl(), "top-left");
        //A button that allows the map to fly to user’s current location when pressed
        this.map.addControl(
            new maplibregl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true,
            })
        );
        if (this.locations) {
          this.markers = [];
          for (let i = 0; i < this.locations.length; i++) {
            const html = `<h3>${this.locations[i].Name}</h3><p style="text-align:left;">${this.locations[i].Address}</p><p style="text-align:left;">${this.locations[i]["Business Hours"]}</p>`
            const marker = new maplibregl.Marker()
              .setLngLat([this.locations[i].Longitude, this.locations[i].Latitude])
              .setPopup(new maplibregl.Popup().setHTML(html)) // add popup
              .addTo(this.map);
            this.markers.push(marker);
            this.locations[i].marker = marker;
          }
        }
    },
    setViewport (location) {
      this.map.panTo([location.Longitude, location.Latitude], 5000);
      location.marker.togglePopup();
    }
  },
  watch: {
    user() {
      this.fetchData();
    },
  },
};
</script>

<style scoped>
.location-map {
  width: 100%;
  height: 40vw;
}

@media (max-width: 768px) {
  .layout--has-nav {
    padding-top: 95px;
  }

  .container {
    padding: 0;
    margin: 0;
  }

  .location-map {
    width: 100%;
    height: 100vw;
  }
}

</style>
