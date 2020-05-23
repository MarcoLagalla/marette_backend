<template>
  <v-fade-transition mode="out-in">
    <router-view />
  </v-fade-transition>
</template>

<script>
  export default {
    name: 'Marette',
    metaInfo: {
      title: 'Marette',
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
  --ghostwhite: #FBFFFE;
  --ming: #AF473C;
  --darkslate: #384D48;
  --charcoal: #272D2D;
  --whitesmoke: #F5F5F5;
  --emerald: #00916E;
}
html {

	scroll-behavior: smooth;
}
</style>
