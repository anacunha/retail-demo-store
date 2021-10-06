<template>
  <div>
    <router-link v-if="!user" to="/auth" class="user-dropdown-button login-button btn">Sign In</router-link>

    <button
      v-if="user"
      id="navbarDropdown"
      :class="{ 'user-dropdown-button btn text-left text-lg-right': true, username: !user.persona }"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <div class="shopper">My Account</div>
    </button>

    <div v-if="user" class="dropdown-menu px-3" aria-labelledby="navbarDropdown">
      <button class="dropdown-item dropdown-item-title" @click="signOut">Sign Out</button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { AmplifyEventBus } from 'aws-amplify-vue';
import { Auth } from 'aws-amplify';
import swal from 'sweetalert';

export default {
  name: 'UserDropdown',
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
  methods: {
    signOut() {
      Auth.signOut({ global: true })
        .then(() => {
          AmplifyEventBus.$emit('authState', 'signedOut');
          swal('You have been logged out!');
        })
        .catch(swal);
    },
  },
};
</script>

<style scoped>
.user-dropdown-button {
  border: none;
  background: none;
  font-size: 0.85rem;
  line-height: 1.15rem;
}

.login-button {
  border-color: var(--grey-600);
  font-size: 1rem;
}

.shopper {
  font-weight: bold;
  color: var(--blue-600);
}

.username {
  font-size: 1rem;
}

.dropdown-menu {
  max-width: 350px;
}

.dropdown-item {
  white-space: normal;
}

.dropdown-item-title {
  color: var(--blue-600);
}

.dropdown-item:active .dropdown-item-title,
.dropdown-item-title:active {
  color: var(--white);
}
</style>
