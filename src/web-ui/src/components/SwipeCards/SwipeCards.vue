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

const PRODUCTS = [
  {
    name: 'Sour',
    description: `Pucker up! You enjoy a beer with acidity, tartness, and complexity, like a Belgian lambic, German gose, or an American wild ale. These brews often involve fruit and they're always refreshing.`,
    id: 'sour-plum-b80ec53c-1efc-48a4-9430-5eb0c77a0964',
  },
  {
    name: 'IPA',
    description:
      'Bring on the hops! You like your beers malty and sweet, but balanced with plenty of hop bitterness. IPAs are a favorite of microbreweries and craft beer aficionados around the world.',
    id: 'ipa-american-3e2c3c68-314c-4da8-a409-02909da91f60',
  },
  {
    name: 'Lager',
    description:
      'Whether an easy-drinking Pilsner or an amber Oktoberfest brew, you like your beers light, smooth, crisp, and cold. These refreshing beers are the most popular in the world for a reason.',
    id: 'lager-pale-72079edd-ef8e-44fa-964e-18a613409023',
  },
  {
    name: 'Wheat',
    description:
      'A classic from Germany, wheat beers are usually low in bitterness with hints of clove, coriander, or even banana. Think hefeweizen, witbier, or American wheat beer, with or without the orange slice.',
    id: 'witbier-17aac130-a63b-424d-9b62-a3c21571e3fe',
  },
  {
    name: 'Stout',
    description:
      'Dark, silky, and creamy, is there anything better than a good stout? These brews are dark in colour, often higher in alcohol, and can remind the drinker of coffee, chocolate, or even licorice.',
    id: 'stout-milk-35ae8bff-7408-4407-9e08-8a8424277bc8',
  },
  {
    name: 'Cider',
    description:
      'Who needs grains? You prefer fruit-based brews like cider (apples) or perry (pears). These can be sweet, tart, dry, or even funky like a barnyard.',
    id: 'cider-dry-6876296f-079e-4288-85b4-85e4c1459224',
  },
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
      PRODUCTS.map(({ id, name, description }) =>
        ProductsRepository.getProduct(id).then(({ data }) => ({ ...data, name, description })),
      ),
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
