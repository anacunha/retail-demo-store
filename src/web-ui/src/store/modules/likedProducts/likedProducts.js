import { AnalyticsHandler } from '@/analytics/AnalyticsHandler';

export const likedProducts = {
  state: () => ({ likedProducts: [] }),
  mutations: {
    setLikedProducts: (state, newLikedProducts) => (state.likedProducts = newLikedProducts),
  },
  actions: {
    likeProduct: ({ commit, state, rootState }, product) => {
      if (!state.likedProducts.includes(product.id)) {
        AnalyticsHandler.productViewed(rootState.user, product);

        commit('setLikedProducts', [...state.likedProducts, product.id])
      }
    },
  },
};
