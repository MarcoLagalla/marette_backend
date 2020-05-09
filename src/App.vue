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
      titleTemplate: '%s | Daedal Multi-Purpose Theme',
      htmlAttrs: { lang: 'en' },
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
  --chilli: #af473c;
  --charcoal: #3c3c3c;
  --whitesmoke: #F5F5F5;
  --emerald: #00916E;
}
html {
  
	scroll-behavior: smooth;
}
</style>
