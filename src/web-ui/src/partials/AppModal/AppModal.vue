<template>
  <component v-if="component" :is="component"></component>
</template>

<script>
import { mapState } from 'vuex';

import ShopperSelectModal from './ShopperSelectModal/ShopperSelectModal';
import { Modals } from './config';

export default {
  name: 'AppModal',
  computed: {
    ...mapState({
      component: (state) => {
        if (!state.modal.openModal) return null;

        switch (state.modal.openModal.name) {
          case Modals.ShopperSelect:
            return ShopperSelectModal;
          default:
            throw new Error('Invalid modal name');
        }
      },
    }),
  },
};
</script>
