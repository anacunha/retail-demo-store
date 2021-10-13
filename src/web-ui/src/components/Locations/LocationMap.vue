<template>
  <div ref="container" class="location-map"></div>
</template>

<script>
export default {
  name: 'LocationMap',
  inject: ['locationMapContext'],
  mounted() {
    this.locationMapContext.registerMapContainer(this.$refs.container);
  },
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
