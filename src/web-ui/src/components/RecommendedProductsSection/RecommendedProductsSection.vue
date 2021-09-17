<template>
  <section class="mb-5">
    <div class="mb-3 text-left">
      <h2 class="recommendations-heading"><slot name="heading"></slot></h2>
    </div>

    <div class="row">
      <LoadingFallback v-if="isLoading" class="col my-4 text-center"></LoadingFallback>

      <ProductCarousel
        v-else
        :recommendedProducts="recommendedProducts"
        class="col"
      ></ProductCarousel>
    </div>
  </section>
</template>

<script>
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';
import ProductCarousel from './ProductCarousel/ProductCarousel';

export default {
  name: 'RecommendedProductsSection',
  props: {
    recommendedProducts: {
      type: Array,
      required: false,
    },
  },
  components: {
    LoadingFallback,
    ProductCarousel,
  },
  computed: {
    isLoading() {
      return !this.recommendedProducts;
    },
  },
};
</script>

<style scoped>
.recommendations-heading {
  font-size: 1rem;
}

.recommendation-explanation {
  font-style: italic;
}

@media (min-width: 768px) {
  .recommendations-heading {
    font-size: 1.4rem;
  }
}
</style>
