<template>
  <Layout :isLoading="isLoading">
    <template #default>
      <main class="container product-container mb-4 text-left">
        <div class="title-and-rating mb-md-3">
          <h1 class="product-name">{{ product.name }}</h1>
        </div>

        <div class="add-to-cart-and-description">
          <p class="mb-0">{{ product.description }}</p>
        </div>

        <div class="product-img">
          <img :src="productImageUrl" class="img-fluid" :alt="product.name" />
        </div>
      </main>

      <div class="container">
        <h2 class="location-heading mb-3">Find this beer</h2>
      </div>
      <MapContext :locations="locations" class="mb-4">
        <LocationMap></LocationMap>
      </MapContext>

      <div class="container">
        <RecommendedProductsSection :recommendedProducts="relatedProducts">
          <template #heading>Compare similar beers</template>
        </RecommendedProductsSection>
      </div>
    </template>
  </Layout>
</template>

<script>
import { mapGetters } from 'vuex';

import { RepositoryFactory } from '@/repositories/RepositoryFactory';

import { product } from '@/mixins/product';

import Layout from '@/components/Layout/Layout';
import RecommendedProductsSection from '@/components/RecommendedProductsSection/RecommendedProductsSection';
import MapContext from '@/components/Locations/MapContext';
import LocationMap from '@/components/Locations/LocationMap';

const LocationsRepository = RepositoryFactory.get('locations');
const RecommendationsRepository = RepositoryFactory.get('recommendations');
const MAX_RECOMMENDATIONS = 6;

export default {
  name: 'ProductDetail',
  components: {
    Layout,
    RecommendedProductsSection,
    MapContext,
    LocationMap,
  },
  mixins: [product],
  data() {
    return {
      relatedProducts: null,
      locations: null,
    };
  },
  computed: {
    ...mapGetters(['personalizeUserID']),
    isLoading() {
      return !this.product;
    },
  },
  watch: {
    $route: {
      immediate: true,
      handler() {
        this.fetchData();
      },
    },
    personalizeUserID() {
      this.getRelatedProducts();
    },
  },
  methods: {
    async fetchData() {
      await this.getProductByID(this.$route.params.id);

      this.getRelatedProducts();
      this.getLocations();
    },
    async getRelatedProducts() {
      // reset in order to trigger recalculation in carousel - carousel UI breaks without this
      this.relatedProducts = null;

      const response = await RecommendationsRepository.getRelatedProducts(
        this.personalizeUserID ?? '',
        this.product.id,
        MAX_RECOMMENDATIONS,
      );

      this.relatedProducts = response.data;
    },
    async getLocations() {
      let locationsResult = await LocationsRepository.getLocationsByBeer(this.product.name);

      this.locations = locationsResult.data;
    },
  },
};
</script>

<style scoped>
.product-container {
  display: grid;
  grid-gap: 15px;
  grid-template-columns: 1fr;
  grid-template-rows: auto;
  grid-template-areas:
    'TitleAndRating'
    'ProductImage';
}

@media (min-width: 768px) {
  .product-container {
    grid-template-columns: 1fr 1fr;
    grid-column-gap: 30px;
    grid-template-rows: auto;
    grid-template-areas:
      'ProductImage TitleAndRating'
      'ProductImage .'
      'ProductImage .';
  }
}

.title-and-rating {
  grid-area: TitleAndRating;
}

.product-name {
  font-size: 1.5rem;
}

.product-img {
  grid-area: ProductImage;
}

.location-heading {
  font-size: 1rem;
  text-align: left;
}
</style>
