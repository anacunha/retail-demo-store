<template>
  <div class="card-container">
    <div
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

const PRODUCTS = [
  { id: 1, name: 'Test Product 1', image: '003e4953-d6cb-400c-90f6-9b0216b4603e.jpg', category: 'floral' },
  { id: 2, name: 'Test Product 2', image: '045324c6-7df9-4ce7-9688-d352a6d73e02.jpg', category: 'floral' },
  { id: 3, name: 'Test Product 3', image: '0712d739-d058-414e-b905-703eaaa3d3ca.jpg', category: 'floral' },
  { id: 4, name: 'Test Product 4', image: '08501583-c08b-411b-9ae7-06582e2d8c26.jpg', category: 'floral' },
  { id: 5, name: 'Test Product 5', image: '0c4744e2-b989-4509-a7e2-7d8dc43ff404.jpg', category: 'floral' },
  { id: 6, name: 'Test Product 6', image: '110f2a06-e151-4f79-9acb-8b8ce97ca449.jpg', category: 'floral' },
  { id: 7, name: 'Test Product 7', image: '11b36e89-6771-4cd0-9a3b-e6bb9025b825.jpg', category: 'floral' },
  { id: 8, name: 'Test Product 8', image: '128c6bfd-533a-478e-8e63-bb25deabe186.jpg', category: 'floral' },
];

export default {
  name: 'SwipeCards',
  components: { SwipeCard },
  data() {
    return {
      products: PRODUCTS,
      likedProducts: [],
    };
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
      console.log(this.likedProducts)

      this.$emit('complete');
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
