<template>
  <div className="container">
    <h1>Locations</h1>

    <LoadingFallback v-if="isLoading" class="col my-4 text-center"></LoadingFallback>
    <div v-else v-for="location in locations" :key="location.Id">
      <LocationDetail :location="location" :changeViewport="changeViewport" />
    </div>
  </div>
</template>

<script>
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';
import LocationDetail from '@/components/Locations/LocationDetail';

export default {
  name: 'LocationList',
  props: {
    locations: {
      type: Array,
      required: false,
    },
    changeViewport: null,
  },
  components: {
    LoadingFallback,
    LocationDetail,
  },
  computed: {
    isLoading() {
      return !this.locations;
    },
  },
  methods: {
  }
};
</script>

<style scoped>
</style>
