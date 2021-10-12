<template>
  <div>
    <div ref="container" class="location-map"></div>
    <div class="distance-container" v-if="this.locationMapContext.getDistance() > 0">
      <div>Walking distance: {{ this.locationMapContext.getDistance() | formatMiles }}</div>
      <div>Time to destination: {{ this.locationMapContext.getDuration() | formatTime }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LocationMap',
  inject: ['locationMapContext'],
  mounted() {
    this.locationMapContext.registerMapContainer(this.$refs.container);
  },
  filters: {
    formatMiles: function (value) {
      if (!value) return ''

      return `${value.toPrecision(3)} miles`
    },
    formatTime: function (value) {
      if (!value) return ''
      if (value > 3600) { // over an hour, show in hours
        return `${(value / 60 / 60).toPrecision(4)} hours`
      }
      return `${(value / 60).toPrecision(4)} minutes`
    }
  }
};
</script>

<style scoped>
.location-map {
  width: 100%;
  height: 40vw;
}

@media (max-width: 768px) {
  .location-map {
    width: 100%;
    height: 100vw;
  }
}
</style>
