<template>
  <Layout>
    <div class="container">
      <MapContext>
        <LocationMap></LocationMap>
        <LocationList></LocationList>
      </MapContext>
    </div>
  </Layout>
</template>

<script>
import Layout from '@/components/Layout/Layout';
import MapContext from '@/components/Map/MapContext';
import LocationMap from '@/components/Map/LocationMap';
import LocationList from '@/components/Map/LocationList';

export default {
  name: 'Locations',
  components: {
    Layout,
    MapContext,
    LocationMap,
    LocationList,
  },
};
</script>

<style scoped>
@media (max-width: 768px) {
  .layout--has-nav {
    padding-top: 95px;
  }

  .container {
    padding: 0;
    margin: 0;
  }
}
</style>
