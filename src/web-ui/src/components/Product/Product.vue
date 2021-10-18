<template>
  <div class="featured-product d-flex flex-column justify-content-between text-left">
    <router-link
      class="link"
      :to="{
        name: 'ProductDetail',
        params: { id: product.id },
      }"
    >
      <div>
        <div><img :src="productImageURL" class="card-img-top" :alt="product.name" /></div>

        <div class="p-3">
          <div class="product-name">{{ product.name }}</div>
          <div class="d-block text-truncate font-italic small">{{ product.style }}</div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { getProductImageUrl } from '@/util/getProductImageUrl';

export default {
  name: 'Product',
  props: {
    product: { type: Object, required: true },
  },

  computed: {
    productImageURL() {
      return getProductImageUrl(this.product);
    },
  },
};
</script>

<style scoped>
.link {
  color: inherit;
}

.link:hover {
  text-decoration: none;
}

.card-img-overlay {
  opacity: 0.75;
}

.featured-product {
  border: 1px solid var(--grey-300);
  text-decoration: none;
  color: inherit;
}

.product-name {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scale-icon {
  color: var(--blue-600);
}
</style>
