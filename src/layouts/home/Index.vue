<template>
<v-app class="main">
  <home-app-bar />
  <home-view />
  <home-settings v-if="(this.isLogged)" />
  <home-footer />
</v-app>
</template>

<script>
export default {
  name: 'HomeLayout',
  components: {
    HomeAppBar: () => import('@/layouts/home/AppBar'),
    HomeFooter: () => import('@/layouts/home/Footer'),
    HomeSettings: () => import('@/layouts/home/Settings'),
    // HomeSystemBar: () => import('@/layouts/home/SystemBar'),
    HomeView: () => import('@/layouts/home/View'),
  },
  computed: {
    isLogged() {
      return this.$store.getters['userAuthentication/isAuthenticated']
    },
  }
}
</script>

<style scoped>
    .main {
        width: 100%;
        height: 100%;
        max-width: 100%!important;
    }
</style>