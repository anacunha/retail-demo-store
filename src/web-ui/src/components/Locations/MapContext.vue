<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import * as turf from "@turf/turf";
import maplibregl from "maplibre-gl";
import { Auth } from "aws-amplify";
import Location from "aws-sdk/clients/location";
import { createMap } from "maplibre-gl-js-amplify";

const WYNN_LAS_VEGAS_COORDINATES = [-115.164833, 36.127106];

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
      selectedLocation: null,
      currentLocation: {
        latitude: null,
        longitude: null
      },
      travelMode: 'Walking'
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
    travelMode() {
      // update directions when travel mode is changed
      this.showDirections();
    }
  },
  provide() {
    return {
      locationMapContext: {
        registerMapContainer: this.registerContainer,
        onLocationsChange: this.onLocationsChange,
        changeViewport: this.setViewport,
        showDirections: this.showDirections,
        changeTravelMode: this.changeTravelMode,
        setSelectedLocation: this.setSelectedLocation,
        getDistance: () => this.distance,
        getDuration: () => this.duration,
        getTravelMode: () => this.travelMode
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

      this.service = new Location({
        credentials: this.credentials,
        region: process.env.VUE_APP_AWS_REGION,
      });
      this.initializeMap();
    },
    async initializeMap() {
      if (this.locations && this.locations.length != 0) {
        this.center = [this.locations[0].Longitude, this.locations[0].Latitude];
        this.zoom = 9;
      } else {
        // The Wynn Las Vegas
        this.center = WYNN_LAS_VEGAS_COORDINATES;
        this.zoom = 18;
      }

      this.map = await createMap({
        container: this.container,
        center: this.center,
        zoom: this.zoom,
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
          const markerDom = document.createElement('div');
          markerDom.classList.add('location-marker');
          markerDom.innerHTML = `
              <i class="fas fa-map-pin fa-2x"></i>
            `;

          const marker = new maplibregl.Marker({element: markerDom}).setLngLat([location.Longitude, location.Latitude]);
          const domContentContainer = document.createElement('div');
          domContentContainer.innerHTML = `
            <h1>${location.Name}</h1>
            <p>${location.Address}</p>
            <a href="tel:${location.Phone}"><i class="fas fa-phone"></i></a>
          `;
          const directionsButton = document.createElement('button');
          directionsButton.classList.add('directions-button');
          directionsButton.innerHTML = `<i class="fas fa-directions"></i>`;
          directionsButton.addEventListener('click', () => this.showDirections());
          domContentContainer.appendChild(directionsButton);
          const popup = new maplibregl.Popup().setDOMContent(domContentContainer);
          popup.on('open', () => this.selectedLocation = location);
          return marker.setPopup(popup);
        });
        this.markers.forEach((marker, i) => {
          marker.addTo(this.map);
          this.locations[i].marker = marker;
        });
      }

      if (this.currentLocation.latitude && this.currentLocation.longitude) {
        const markerDom = document.createElement('div');
        markerDom.classList.add('current-location-marker');
        markerDom.innerHTML = `
            <i class="fas fa-circle"></i>
          `;
        const marker = new maplibregl.Marker({element: markerDom}).setLngLat([this.currentLocation.longitude, this.currentLocation.latitude]);
        marker.addTo(this.map);
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
    async showDirections() {
      this.hideAllPopups();
      const routeData = await this.calculateRoute(this.selectedLocation);
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
    setSelectedLocation(location) {
      this.selectedLocation = location;
    },
    changeTravelMode(travelMode) {
      this.travelMode = travelMode;
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
    async calculateRoute() {
      const params = {
        CalculatorName: "FindMyBrewRouteCalculator",
        DeparturePosition: [this.currentLocation.longitude, this.currentLocation.latitude],
        DestinationPosition: [this.selectedLocation.Longitude, this.selectedLocation.Latitude],
        IncludeLegGeometry: true,
        DistanceUnit: 'Miles',
        TravelMode: this.travelMode
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
