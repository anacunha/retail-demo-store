<template>
  <div :class="{ 'layout--has-nav': showNav, 'layout--has-demo-guide': showDemoGuide }">
    <Navigation v-if="showNav"></Navigation>

    <LoadingFallback v-if="isLoading" class="container mb-4"></LoadingFallback>

    <slot v-if="!isLoading"></slot>

    <Footer v-if="showFooter" class="my-4 container"></Footer>

    <AppModal></AppModal>
  </div>
</template>

<script>
import LoadingFallback from '../LoadingFallback/LoadingFallback';
import Footer from '@/partials/Footer/Footer';
import Navigation from '@/partials/Navigation/Navigation';
import AppModal from '@/partials/AppModal/AppModal';

export default {
  name: 'Layout',
  components: {
    Navigation,
    LoadingFallback,
    Footer,
    AppModal,
  },
  props: {
    showNav: {
      type: Boolean,
      default: true,
    },
    showTextAlerts: {
      type: Boolean,
      default: true,
    },
    showFooter: {
      type: Boolean,
      default: true,
    },
    showDemoGuide: {
      type: Boolean,
      default: true,
    },
    backgroundColor: {
      type: String,
      default: 'var(--white)',
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    updateBackgroundColor(color) {
      document.body.style.setProperty('--background-color', color);
    },
  },
  mounted() {
    this.updateBackgroundColor(this.backgroundColor);
  },
  watch: {
    backgroundColor: {
      handler(newBg) {
        this.updateBackgroundColor(newBg);
      },
    },
  },
  beforeDestroy() {
    document.body.style.removeProperty('--background-color');
  },
};
</script>

<style scoped>
.layout--has-nav {
  padding-top: 250px;
}

@media (min-width: 992px) {
  .layout--has-nav {
    padding-top: 150px;
  }
}
</style>

<style>
body {
  background-color: var(--background-color);
}
</style>
