<template>
  <div class="card-container">
    <LoadingFallback v-if="!products"></LoadingFallback>

    <div
      v-else
      class="swipable-card-container"
      v-for="(product, i) in products"
      :key="product.id"
      :style="{ '--card-index': i }"
    >
      <SwipeCard
        :product="product"
        class="swipable-card"
        @swipeLeft="onSwipeLeft(i)"
        @swipeRight="onSwipeRight(i)"
      ></SwipeCard>
    </div>
  </div>
</template>

<script>
import SwipeCard from './SwipeCard.vue';
import { mapState } from 'vuex';
import { RepositoryFactory } from '@/repositories/RepositoryFactory';
import { AnalyticsHandler } from '@/analytics/AnalyticsHandler';
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';

const ProductsRepository = RepositoryFactory.get('products');

const PRODUCT_IDS = [
  '66be3dc0-8d56-43a1-8871-9df892e86f97',
  '8bccac2a-2f85-4cf1-b203-1b05281b6041',
  '85017fa9-20ca-4225-836e-ff43204fae0e',
  '05a84203-72b8-4c61-83ef-2d90d62c08ee',
  '68c8e9e8-b02a-47dc-aa8a-f7ebeb5a1156',
  'a3203d5c-eaab-49c1-9be1-93f22e68e525',
  '414eb6de-c76a-478a-b1db-7329019911e8',
  '3c2d0021-1e75-431d-84fd-511a2ba64746',
  'ceee32d9-161b-4749-939f-8079965433cc',
  '4a6fb15c-9d2b-4d40-8511-53fcd654c9b2',
];

export default {
  name: 'SwipeCards',
  components: { LoadingFallback, SwipeCard },
  data() {
    return {
      products: null,
      likedProducts: [],
    };
  },
  async mounted() {
    this.products = await Promise.all(
      PRODUCT_IDS.map((id) => ProductsRepository.getProduct(id).then(({ data }) => data)),
    );
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    onSwipeLeft(i) {
      this.products.splice(i, 1);
    },
    onSwipeRight(i) {
      const [likedProduct] = this.products.splice(i, 1);

      this.likedProducts.push(likedProduct);
    },
    onCompletion() {
      this.recordLikedProductViews();

      this.$emit('complete');
    },
    recordLikedProductViews() {
      this.likedProducts.forEach((product) => AnalyticsHandler.productLiked(this.user, product));
    },
  },
  watch: {
    products(newProducts) {
      if (newProducts.length === 0) this.onCompletion();
    },
  },
};
</script>

<style scoped>
.card-container {
  position: relative;
  height: 400px;
}

.swipable-card-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transform: translateY(calc(var(--card-index) * 6px)) scale(calc(1 - 0.01 * var(--card-index)));
  transition: transform 150ms ease-in-out;
  z-index: calc(var(--card-index) * -1);
}
</style>
