<template>
  <SecondaryLayout>
    <div class="container">
      <SwipeCards @complete="onComplete"></SwipeCards>
    </div>
  </SecondaryLayout>
</template>

<script>
import SecondaryLayout from '@/components/SecondaryLayout/SecondaryLayout';
import SwipeCards from '@/components/SwipeCards/SwipeCards';

export default {
  name: 'ShopperSelectPage',
  components: { SecondaryLayout, SwipeCards },
  methods: {
    onComplete() {
      this.$router.push('/');
    },
  },
};
</script>
