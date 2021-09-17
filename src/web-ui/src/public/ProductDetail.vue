<template>
  <Layout :isLoading="isLoading">
    <template #default>
      <div class="container">
        <main class="product-container mb-5 text-left">
          <div class="title-and-rating mb-md-3">
            <h1 class="product-name">{{ product.name }}</h1>
            <FiveStars></FiveStars>
          </div>

          <div class="add-to-cart-and-description">
            <ProductPrice :price="product.price" class="mb-1"></ProductPrice>

            <p>{{ product.description }}</p>
          </div>

          <div class="product-img">
            <img :src="productImageUrl" class="img-fluid" :alt="product.name" />
          </div>
        </main>

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
import ProductPrice from '@/components/ProductPrice/ProductPrice';
import FiveStars from '@/components/FiveStars/FiveStars';
import RecommendedProductsSection from '@/components/RecommendedProductsSection/RecommendedProductsSection';

const RecommendationsRepository = RepositoryFactory.get('recommendations');
const MAX_RECOMMENDATIONS = 6;

export default {
  name: 'ProductDetail',
  components: {
    Layout,
    ProductPrice,
    FiveStars,
    RecommendedProductsSection,
  },
  mixins: [product],
  data() {
    return {
      relatedProducts: null,
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
</style>
