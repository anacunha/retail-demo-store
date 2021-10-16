<template>
  <div>
    <div ref="container" class="location-map"></div>
    <div class="distance-container" v-if="this.locationMapContext.getDistance() > 0">
      <div>{{ this.locationMapContext.getDuration() | formatTime }} ({{ this.locationMapContext.getDistance() | formatMiles }})</div>
      <div class="btn-group" role="group" aria-label="Basic example">
        <button @click="changeTravelMode('Walking')" type="button" v-bind:class="[isWalking() ? 'btn-primary' : 'btn-outline-primary', 'btn', 'btn-sm']"><i class="fas fa-walking"></i> Walking</button>
        <button @click="changeTravelMode('Car')" type="button" v-bind:class="[!isWalking() ? 'btn-primary' : 'btn-outline-primary', 'btn', 'btn-sm']"><i class="fas fa-car"></i> Driving</button>
      </div>
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
  methods: {
    changeTravelMode(travelMode) {
      this.locationMapContext.changeTravelMode(travelMode);
    },
    isWalking() {
      return this.locationMapContext.getTravelMode() === 'Walking';
    }
  },
  filters: {
    formatMiles: function (value) {
      if (!value) return ''

      return `${Number(value).toFixed(2)} miles`
    },
    formatTime: function (value) {
      if (!value) return ''
      if (value > 3600) { // over an hour, show in hours
        return `${Number(value / 60 / 60).toFixed(2)} hours`
      }
      return `${Number(value / 60).toFixed(2)} minutes`
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
