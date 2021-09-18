<template>
  <div>
    <div class="banner mb-5 py-2">
      <div class="container d-flex align-items-center">
        <div class='logo-container'><img src="/fmb-logo-white.svg" alt="logo" class="img-fluid" /></div>
        <PoweredByAWS class="powered-by-logo"></PoweredByAWS>
      </div>
    </div>

    <slot></slot>

    <footer class="mt-5 container">
      <TermsAndConditions></TermsAndConditions>
    </footer>
  </div>
</template>

<script>
import PoweredByAWS from '@/components/PoweredByAWS/PoweredByAWS';
import TermsAndConditions from '@/partials/TermsAndConditions/TermsAndConditions.vue';

export default {
  name: 'SecondaryLayout',
  components: { PoweredByAWS, TermsAndConditions },
};
</script>

<style scoped>
.banner {
  background: var(--aws-deep-squid-ink);
}

.powered-by-logo {
  /* fine-tune spacing to make logo appear more centered */
  margin-top: 15px;
  height: 45px;
  fill: var(--white);
}

.logo-container {
  width: 100px;
}
</style>
