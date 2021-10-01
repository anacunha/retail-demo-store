<template>
  <button type="button" :class="{ 'like-button btn': true, liked: isLiked }" @click="onClick" aria-label="like product">
    <i :class="{ 'fa-thumbs-up': true, fas: isLiked, far: !isLiked }"></i>
  </button>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'ProductLikeButton',
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState({
      isLiked(state) {
        return state.likedProducts.likedProducts.includes(this.product.id);
      },
    }),
  },
  methods: {
    ...mapActions(['likeProduct']),
    onClick() {
      this.likeProduct(this.product);
    },
  },
};
</script>

<style .scoped>
.like-button {
  padding: 0;
}

.like-button,
.like-button.liked:hover,
.like-button.liked:focus {
  color: var(--blue-600);
}

.like-button:hover,
.like-button:focus {
  color: var(--blue-500);
}
</style>
