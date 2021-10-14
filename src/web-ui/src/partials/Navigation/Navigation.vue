<template>
  <nav class="navigation fixed-top pt-2 pb-3 p-lg-1">
    <div class="nav-contents container d-lg-flex align-items-center">
      <HomeLink class="logo"></HomeLink>
      <ShopDropdown></ShopDropdown>
      <UserDropdown class="user-dropdown"></UserDropdown>
    </div>
  </nav>
</template>

<script>
import HomeLink from './HomeLink/HomeLink';
import UserDropdown from './UserDropdown/UserDropdown';
import ShopDropdown from './ShopDropdown/ShopDropdown';

export default {
  name: 'Navigation',
  components: {
    HomeLink,
    UserDropdown,
    ShopDropdown,
  },
};
</script>

<style scoped>
.navigation {
  background: var(--white);
  border-bottom: 1px solid var(--grey-500);
  box-shadow: 6px 2px 6px var(--grey-200);
}

.logo {
  grid-area: Logo;
  width: 80px;
}

.user-dropdown {
  flex-grow: 4;
  text-align: right;
}

.nav-contents {
  display: flex;
  justify-content: space-between;
}

@media (min-width: 992px) {
  .logo {
    width: 120px;
  }
}
</style>
