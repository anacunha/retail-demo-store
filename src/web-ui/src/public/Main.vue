<template>
  <Layout>
    <div class="container">
      <section class="mb-5">
        <div v-if="userRecommendationsTitle" class="mb-3 text-left">
          <h2 class="recommendations-heading">
            {{ userRecommendationsTitle }}
          </h2>
        </div>

        <div
          v-if="
            personalizeUserID &&
              ((isLoadingRecommendations && !userRecommendations) || (!isLoadingRecommendations && userRecommendations))
          "
        >
          <LoadingFallback v-if="!userRecommendations" class="col my-4 text-center"></LoadingFallback>

          <div v-else class="user-recommendations">
            <Product v-for="item in userRecommendations" :key="item.product.id" :product="item.product"></Product>
          </div>
        </div>
      </section>

      <RecommendedProductsSection :recommendedProducts="featuredProducts">
        <template #heading>Featured beers</template>
      </RecommendedProductsSection>
    </div>
  </Layout>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

import { RepositoryFactory } from '@/repositories/RepositoryFactory';

import Layout from '@/components/Layout/Layout';
import RecommendedProductsSection from '@/components/RecommendedProductsSection/RecommendedProductsSection';
import Product from '@/components/Product/Product';
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';

const ProductsRepository = RepositoryFactory.get('products');
const RecommendationsRepository = RepositoryFactory.get('recommendations');
const MAX_RECOMMENDATIONS = 12;

export default {
  name: 'Main',
  components: {
    Layout,
    RecommendedProductsSection,
    Product,
    LoadingFallback,
  },
  data() {
    return {
      isLoadingRecommendations: true,
      featuredProducts: null,
      userRecommendations: null,
      userRecommendationsTitle: null,
    };
  },
  computed: {
    ...mapState({ user: (state) => state.user }),
    ...mapGetters(['personalizeUserID', 'personalizeRecommendationsForVisitor']),
  },
  async created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.getFeaturedProducts();
      this.getUserRecommendations();
    },
    async getFeaturedProducts() {
      this.featuredProducts = null;

      const { data: featuredProducts } = await ProductsRepository.getFeatured();

      if (this.personalizeUserID && featuredProducts.length > 0) {
        const { data: rerankedProducts } = await RecommendationsRepository.getRerankedItems(
          this.personalizeUserID,
          featuredProducts,
        );

        this.featuredProducts = rerankedProducts.slice(0, MAX_RECOMMENDATIONS).map((product) => ({ product }));
      } else {
        this.featuredProducts = featuredProducts.slice(0, MAX_RECOMMENDATIONS).map((product) => ({ product }));
      }
    },
    async getUserRecommendations() {
      this.isLoadingRecommendations = true;
      this.userRecommendationsTitle = null;
      this.userRecommendations = null;

      const response = await RecommendationsRepository.getRecommendationsForUser(
        this.personalizeUserID,
        '',
        MAX_RECOMMENDATIONS,
      );

      if (response.headers) {
        const personalizeRecipe = response.headers['x-personalize-recipe'];

        if (personalizeRecipe) {
          this.userRecommendationsTitle = this.personalizeRecommendationsForVisitor
            ? 'Inspired by your beer reviews'
            : 'Trending beers';
        }
      }

      this.userRecommendations = response.data;

      this.isLoadingRecommendations = false;
    },
  },
  watch: {
    user() {
      this.fetchData();
    },
  },
};
</script>

<style scoped>
.recommendations-heading {
  font-size: 1rem;
}

.user-recommendations {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
}

@media (min-width: 768px) {
  .recommendations-heading {
    font-size: 1.4rem;
  }

  .user-recommendations {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}
</style>
