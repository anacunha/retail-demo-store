import { isMobileModalMediaQueryList, APP_MODAL_ID, Modals } from '@/partials/AppModal/config';

export const modal = {
  state: () => ({
    isMobile: isMobileModalMediaQueryList.matches,
    openModal: null, // {name: Modals, ...metadata} | null
  }),
  mutations: {
    setIsMobile: (state, isMobile) => (state.isMobile = isMobile),
    setOpenModal: (state, newOpenModal) => (state.openModal = newOpenModal),
    setSelectedArticle: (state, articleId) => {
      if (state.openModal?.name === Modals.DemoGuide) state.openModal.selectedArticle = articleId;
    },
  },
  actions: {
    toggleIsMobile: ({ commit, state }) => commit('setIsMobile', !state.isMobile),

    openModal: ({ commit }, name) => {
      switch (name) {
        case Modals.DemoWalkthrough:
          commit('setOpenModal', { name, pageIndex: 0 });
          break;

        case Modals.ShopperSelect:
          commit('setOpenModal', { name });
          break;

        default:
          throw new Error('Invalid modal name');
      }

      // show bootstrap modal
      // eslint-disable-next-line no-undef
      setTimeout(() => $(`#${APP_MODAL_ID}`).modal('show'), 0);
    },
    closeModal: ({ commit }) => commit('setOpenModal', null),
    prevTourPage: ({ commit, state }) => {
      if (state.openModal?.name === Modals.DemoWalkthrough && state.openModal.pageIndex > 0)
        commit('setOpenModal', { name: Modals.DemoWalkthrough, pageIndex: state.openModal.pageIndex - 1 });
    },
    nextTourPage: ({ commit, state }) => {
      if (state.openModal?.name === Modals.DemoWalkthrough)
        commit('setOpenModal', { name: Modals.DemoWalkthrough, pageIndex: state.openModal.pageIndex + 1 });
    },
  },
};

export const manageResponsiveModalState = (store) => isMobileModalMediaQueryList.addEventListener('change', () => store.dispatch('toggleIsMobile'));
