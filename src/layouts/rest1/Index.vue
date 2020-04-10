<template>
  <v-app>
<rest1-view />
  </v-app>


</template>

<script>
  export default {
    name: 'Rest1Layout',

    components: {
      //rest1AppBar: () => import('@/layouts/rest1/AppBar'),
      //rest1Footer: () => import('@/layouts/rest1/Footer'),
      //rest1Settings: () => import('@/layouts/rest1/Settings'),
     // rest1SystemBar: () => import('@/layouts/rest1/SystemBar'),
      Rest1View: () => import('@/layouts/rest1/View'),
    },
  }
</script>
