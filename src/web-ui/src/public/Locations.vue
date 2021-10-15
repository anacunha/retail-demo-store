<template>
  <Layout>
    <MapContext :locations="locations">
      <LocationMap class="mb-4"></LocationMap>
      <LocationList></LocationList>
    </MapContext>
  </Layout>
</template>

<script>
import Layout from '@/components/Layout/Layout';
import MapContext from '@/components/Locations/MapContext';
import LocationMap from '@/components/Locations/LocationMap';
import LocationList from '@/components/Locations/LocationList';

import { RepositoryFactory } from '@/repositories/RepositoryFactory';
const LocationsRepository = RepositoryFactory.get('locations');

export default {
  name: 'Locations',
  components: {
    Layout,
    MapContext,
    LocationMap,
    LocationList,
  },
  data() {
    return { locations: null };
  },
  async mounted() {
    await this.getLocations();
  },
  methods: {
    async getLocations() {
      let locationsResult = await LocationsRepository.get();

      this.locations = locationsResult.data;
    },
  },
};
</script>
