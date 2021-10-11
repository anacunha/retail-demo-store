<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import * as turf from "@turf/turf";
import maplibregl from "maplibre-gl";
import { Auth } from "aws-amplify";
import location from "aws-sdk/clients/location";
import { Signer } from "@aws-amplify/core";

export default {
  name: "MapContext",
  props: {
    locations: {
      required: true,
    },
  },
  data() {
    return {
      container: null,
      credentials: null,
      service: null,
      center: null,
      zoom: null,
      markers: [],
      map: null,
      locationCallbacks: [],
      // features: []
      geojson: {
        'type': 'FeatureCollection',
        'features': []
      }
    };
  },
  watch: {
    container: {
      immediate: true,
      async handler(newContainer) {
        if (newContainer) {
          this.loadCredentialsAndMap();
        }
      },
    },
    locations(newLocations) {
      this.locationCallbacks.forEach((callback) => callback(newLocations));
      this.loadCredentialsAndMap();
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
    async loadCredentialsAndMap() {
      this.credentials = await Auth.currentCredentials();

      this.service = new location({
        credentials: this.credentials,
        region: process.env.VUE_APP_AWS_REGION,
      });
      this.initializeMap();
    },
    transformRequest(url, resourceType) {
      if (resourceType === "Style" && !url.includes("://")) {
        // resolve to an AWS URL
        url =
          "https://maps.geo." +
          process.env.VUE_APP_AWS_REGION +
          ".amazonaws.com/maps/v0/maps/" +
          url +
          "/style-descriptor";
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
    async initializeMap() {
      if (this.locations && this.locations.length != 0) {
        this.center = new maplibregl.LngLat(
          this.locations[0].Longitude,
          this.locations[0].Latitude
        );
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
      this.map.addControl(new maplibregl.NavigationControl(), "top-left");

      //A button that allows the map to fly to user’s current location when pressed
      this.map.addControl(
        new maplibregl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true,
          },
          trackUserLocation: true,
        })
      );

      if (this.locations) {
        this.markers = [];
        for (let i = 0; i < this.locations.length; i++) {
          const html = `<h1>${this.locations[i].Name}</h1><p>${this.locations[i].Address}</p><a href="tel:${this.locations[i].Phone}"><i class="fas fa-phone"></a></i><i class="fas fa-directions"></i>`;
          const marker = new maplibregl.Marker()
            .setLngLat([
              this.locations[i].Longitude,
              this.locations[i].Latitude,
            ])
            .setPopup(new maplibregl.Popup().setHTML(html)) // add popup
            .addTo(this.map);
          this.markers.push(marker);
          this.locations[i].marker = marker;
        }
      }

      // GeoJSON object to hold our measurement features
      // var geojson = {
      //   'type': 'FeatureCollection',
      //   'features': this.features
      // };

      // // Used to draw a line between points
      // var linestring = {
      //   'type': 'Feature',
      //   'geometry': {
      //     'type': 'LineString',
      //     'coordinates': []
      //   }
      // };

      const theMap = this.map;
      const theGeojson = this.geojson;

      this.map.on("load", function () {
        theMap.addSource("geojson", {
          type: "geojson",
          data: theGeojson,
        });

        // Add styles to the map
        theMap.addLayer({
          id: "measure-points",
          type: "circle",
          source: "geojson",
          paint: {
            "circle-radius": 5,
            "circle-color": "#000",
          },
          filter: ["in", "$type", "Point"],
        });
        theMap.addLayer({
          id: "measure-lines",
          type: "line",
          source: "geojson",
          layout: {
            "line-cap": "round",
            "line-join": "round",
          },
          paint: {
            "line-color": "#000",
            "line-width": 2.5,
          },
          filter: ["in", "$type", "LineString"],
        });
      });
    },
    async setViewport(locationToToggle) {
      this.locations.forEach((location) => {
        if (locationToToggle !== location) {
          const popup = location.marker.getPopup();
          if (popup.isOpen()) {
            popup.remove();
          }
        }
      });

      locationToToggle.marker.togglePopup();
      this.map.panTo(
        [locationToToggle.Longitude, locationToToggle.Latitude],
        5000
      );

      const routeData = await this.calculateRoute(locationToToggle);
      console.log("Legs", routeData.Legs);
      const route = await this.makeLegFeatures(routeData.Legs);

      console.log("route", route);

      this.geojson = {
        'type': 'FeatureCollection',
        'features': route
      };

      this.map.getSource('geojson').setData(
        this.geojson
      );

      // this.features = route;
      // Used to draw a line between points
      var linestring = {
        'type': 'Feature',
        'geometry': {
          'type': 'LineString',
          'coordinates': []
        }
      };
      linestring.geometry.coordinates = route.map(function (
        point
      ) {
        return point.geometry.coordinates;
      });
    },
    async calculateRoute(to) {
      const params = {
        CalculatorName: "FindMyBrewRouteCalculator",
        // DeparturePosition: [from.longitude, from.latitude],
        DeparturePosition: [-115.170227, 36.121159],
        DestinationPosition: [to.Longitude, to.Latitude],
        IncludeLegGeometry: true,
        DistanceUnit: 'Miles'
      };

      console.log(params);

      const data = await this.service.calculateRoute(params).promise();

      return data;
    },
    makeLegFeatures(legs) {
      return legs.map((leg) => {
        console.log("leg", leg);
        const geom = leg.Geometry;

        const { ...properties } = leg;

        return turf.feature(
          {
            type: Object.keys(geom)[0],
            coordinates: Object.values(geom)[0],
          },
          properties
        );
      });
    },
  },
};
</script>
