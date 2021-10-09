<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import { RepositoryFactory } from '@/repositories/RepositoryFactory';

import maplibregl from 'maplibre-gl';
import { Auth } from 'aws-amplify';
import location from 'aws-sdk/clients/location';
import { Signer } from '@aws-amplify/core';

const LocationsRepository = RepositoryFactory.get('locations');

export default {
  name: 'MapContext',
  data() {
    return {
      container: null,
      credentials: null,
      service: null,
      locations: [],
      center: null,
      zoom: null,
      markers: [],
      map: null,
      locationCallbacks: [],
    };
  },
  watch: {
    container: {
      immediate: true,
      async handler(newContainer) {
        if (newContainer) {
          this.credentials = await Auth.currentCredentials();

          this.service = new location({
            credentials: this.credentials,
            region: process.env.VUE_APP_AWS_REGION,
          });

          await this.getLocations();

          this.initializeMap();
        }
      },
    },
    locations(newLocations) {
      this.locationCallbacks.forEach((callback) => callback(newLocations));
    },
  },
  provide() {
    return {
      locationMapContext: {
        registerMapContainer: this.registerContainer,
        onLocationsChange: this.onLocationsChange,
        changeViewport: this.setViewport,
      },
    };
  },
  methods: {
    registerContainer(container) {
      this.container = container;
    },
    onLocationsChange(callback) {
      /**
       * note: we would ideally provide a way to unsubscribe from changes to locations
       * so things don't break when subscribed components unmount but for now we can assume they won't do so
       * unless this component does as well
       * */

      this.locationCallbacks.push(callback);
    },
    transformRequest(url, resourceType) {
      if (resourceType === 'Style' && !url.includes('://')) {
        // resolve to an AWS URL
        url =
          'https://maps.geo.' +
          process.env.VUE_APP_AWS_REGION +
          '.amazonaws.com/maps/v0/maps/' +
          url +
          '/style-descriptor';
      }
      if (url.includes('amazonaws.com')) {
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
      return { url: url || '' };
    },
    async getLocations() {
      let locationsResult = await LocationsRepository.get();

      this.locations = locationsResult.data;
    },
    async initializeMap() {
      if (this.locations && this.locations.length != 0) {
        this.center = new maplibregl.LngLat(this.locations[0].Longitude, this.locations[0].Latitude);
        this.zoom = 9;
      } else {
        // The Venetian Resort
        this.center = new maplibregl.LngLat(-115.170227, 36.121159);
        this.zoom = 18;
      }

      this.map = new maplibregl.Map({
        container: this.container,
        //Specify the centre of the map when it gets rendered
        center: this.center,
        zoom: this.zoom, //Adjust the zoom level
        style: process.env.VUE_APP_LOCATION_RESOURCE_NAME,
        transformRequest: this.transformRequest,
      });

      //Zoom in and out button
      this.map.addControl(new maplibregl.NavigationControl(), 'top-left');

      //A button that allows the map to fly to user’s current location when pressed
      this.map.addControl(
        new maplibregl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true,
          },
          trackUserLocation: true,
        }),
      );

      if (this.locations) {
        this.markers = [];
        for (let i = 0; i < this.locations.length; i++) {
          const html = `<h1>${this.locations[i].Name}</h1><p>${this.locations[i].Address}</p><a href="tel:${this.locations[i].Phone}"><i class="fas fa-phone"></a></i><i class="fas fa-directions"></i>`;
          const marker = new maplibregl.Marker()
            .setLngLat([this.locations[i].Longitude, this.locations[i].Latitude])
            .setPopup(new maplibregl.Popup().setHTML(html)) // add popup
            .addTo(this.map);
          this.markers.push(marker);
          this.locations[i].marker = marker;
        }
      }
    },
    setViewport(location) {
      this.locations.forEach(({marker}) => {
        const popup = marker.getPopup();

        if (popup.isOpen()) {
          popup.remove();
        }
      });

      this.map.panTo([location.Longitude, location.Latitude], 5000);
      location.marker.togglePopup();
    },
  },
};
</script>
