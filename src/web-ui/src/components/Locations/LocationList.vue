<template>
  <div className="container">
    <h1>Locations</h1>

    <LoadingFallback v-if="isLoading" class="col my-4 text-center"></LoadingFallback>
    <div v-else
      v-for="location in locations" :key="location.id"
      class="px-1 text-left align-self-stretch d-flex align-items-stretch text-decoration-none"
    >
        <div class="location-item" @click="onClickLocation(location)">
          <div class="p-3">
            <div class="location-name">{{ location.name }}</div>
            <div>{{ location.address }}</div>
            <div>{{ location.hours }}</div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';

export default {
  name: 'LocationList',
  props: {
    locations: {
      type: Array,
      required: false,
    },
    changeViewport: null
  },
  components: {
    LoadingFallback,
  },
  computed: {
    isLoading() {
      return !this.locations;
    },
  },
  methods: {
    onClickLocation(location) {
      this.changeViewport(location);
    }
  }
};
</script>

<style scoped>
.location-name {
  font-weight: 500;
}
.location-item:hover {
  background-color: #efefef;
}
</style>
