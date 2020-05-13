<template>
  <v-fade-transition mode="out-in">
    <router-view />
  </v-fade-transition>
</template>

<script>
  export default {
    name: 'App',
    metaInfo: {
      title: 'App',
      titleTemplate: '%s | Marette',
      htmlAttrs: { lang: 'it' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    },
  }
</script>

<style >

:root {
  --palesilver: #CFC0BD;
  --ming: #3C6E71;
  --darkslate: #384D48;
  --charcoal: #272D2D;
  --whitesmoke: #F5F5F5;
  --emerald: #00916E;
}
html {

	scroll-behavior: smooth;
}
</style>
