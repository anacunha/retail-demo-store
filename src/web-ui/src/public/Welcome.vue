<template>
  <Layout :showNav="false" :showFooter="false" backgroundColor="var(--aws-squid-ink)">
    <div class="container mb-2 text-left">
      <h1 class="heading my-5 text-center">Welcome to the Find My Brew App!</h1>

      <div class="mt-2 mb-4 my-sm-5 d-flex flex-column align-items-center align-items-sm-end">
        <div class="d-flex flex-column flex-sm-row align-items-center">
          <div class="login-cta d-flex justify-content-center align-items-center">
            Have an account?<router-link to="/auth" class="sign-in btn btn-link">Sign in</router-link>
          </div>
          <router-link to="/auth?signup=true" class="create-account mt-3 mt-sm-0 ml-sm-3 btn btn-primary"
            >Create an account</router-link
          >
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '@/components/Layout/Layout';

export default {
  name: 'Welcome',
  components: {
    Layout,
  },
};
</script>

<style scoped>
.container {
  margin-top: 10vh;
  color: var(--white);
}

.sign-in {
  color: var(--amazon-orange);
}

.create-account {
  border-color: var(--amazon-orange);
  border-radius: 4px;
  background: var(--amazon-orange);
}

.create-account:hover,
.create-account:focus {
  background: var(--amazon-orange-light);
  border-color: var(--amazon-orange-light);
}
</style>
