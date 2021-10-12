<template>
  <div className="container">
    <h1>Locations</h1>

    <LoadingFallback v-if="isLoading" class="col my-4 text-center"></LoadingFallback>
    <div v-else v-for="location in locations" :key="location.Id">
      <LocationDetail :location="location" :changeViewport="locationMapContext.changeViewport" :showDirections="locationMapContext.showDirections" />
    </div>
  </div>
</template>

<script>
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';
import LocationDetail from './LocationDetail';

export default {
  name: 'LocationList',
  inject: ['locationMapContext'],
  components: {
    LoadingFallback,
    LocationDetail,
  },
  data() {
    return { locations: null };
  },
  mounted() {
    this.locationMapContext.onLocationsChange((newLocations) => {
      this.locations = newLocations;
    });
  },
  computed: {
    isLoading() {
      return !this.locations;
    },
  },
};
</script>
