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
      geojson: {
        'type': 'FeatureCollection',
        'features': []
      },
      distance: 0,
      duration: 0,
      currentLocation: {
        latitude: null,
        longitude: null
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
        showDirections: this.showDirections,
        getDistance: () => this.distance,
        getDuration: () => this.duration
      }
    };
  },
  mounted() {
    this.setCurrentLocation();
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

      //A button that allows the map to show the user's current location
      this.map.addControl(
        new maplibregl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true,
          },
          trackUserLocation: true,
        })
      );

      if (this.locations) {
        this.markers = this.locations.map((location) => {
          const marker = new maplibregl.Marker().setLngLat([location.Longitude, location.Latitude]);
          const domContentContainer = document.createElement('div');
          domContentContainer.innerHTML = `
            <h1>${location.Name}</h1>
            <p>${location.Address}</p>
            <a href="tel:${location.Phone}"><i class="fas fa-phone"></i></a>
          `;
          const directionsButton = document.createElement('button');
          directionsButton.classList.add('directions-button');
          directionsButton.innerHTML = `<i class="fas fa-directions"></i>`;
          directionsButton.addEventListener('click', () => this.showDirections(location));
          domContentContainer.appendChild(directionsButton);
          return marker.setPopup(new maplibregl.Popup().setDOMContent(domContentContainer));
        });
        this.markers.forEach((marker, i) => {
          marker.addTo(this.map);
          this.locations[i].marker = marker;
        });
      }

      const theMap = this.map;
      const theGeojson = this.geojson;

      this.map.on("load", function () {
        theMap.addSource("geojson", {
          type: "geojson",
          data: theGeojson,
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
      this.hideAllPopups(locationToToggle);

      locationToToggle.marker.togglePopup();
      this.map.panTo(
        [locationToToggle.Longitude, locationToToggle.Latitude],
        5000
      );
    },
    setCurrentLocation() {
      var options = {
        enableHighAccuracy: true,
        timeout: 20000,
        maximumAge: 0
      };

      navigator.geolocation.getCurrentPosition(this.currentLocationSuccess, this.currentLocationError, options);
    },
    currentLocationSuccess(position) {
      console.log('Current location lat/long:', position.coords.latitude, position.coords.longitude);
      this.currentLocation = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      }
    },
    currentLocationError(error) {
      console.error(`Error getting current location`, error);
    },
    async showDirections(location) {
      this.hideAllPopups();
      const routeData = await this.calculateRoute(location);
      console.log('routeData', routeData)

      this.distance = routeData.Summary.Distance;
      this.duration = routeData.Summary.DurationSeconds;

      console.log('distance/duration', this.distance, this.duration)

      const route = await this.makeLegFeatures(routeData.Legs);

      console.log("makeLegFeatures route", route);

      this.geojson = {
        'type': 'FeatureCollection',
        'features': route
      };

      // draw the route
      this.map.getSource('geojson').setData(
        this.geojson
      );

      // show the starting point, current location
      this.map.setCenter([this.currentLocation.longitude, this.currentLocation.latitude]);

      this.map.zoomTo(12, {
        duration: 1000
      });
    },
    hideAllPopups(locationToToggle = undefined) {
      this.locations.forEach((location) => {
        if (locationToToggle !== location) {
          const popup = location.marker.getPopup();
          if (popup.isOpen()) {
            popup.remove();
          }
        }
      });
    },
    async calculateRoute(to) {
      const params = {
        CalculatorName: "FindMyBrewRouteCalculator",
        DeparturePosition: [this.currentLocation.longitude, this.currentLocation.latitude],
        // DeparturePosition: [-115.170227, 36.121159],
        DestinationPosition: [to.Longitude, to.Latitude],
        IncludeLegGeometry: true,
        DistanceUnit: 'Miles',
        TravelMode: 'Walking'
      };

      return await this.service.calculateRoute(params).promise();
    },
    makeLegFeatures(legs) {
      return legs.map((leg) => {
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
