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
  --terracotta: #945d60;
  --herb: #626e60;
  --chilli: #af473c;
  --charcoal: #3c3c3c;
}
html {
  
	scroll-behavior: smooth;
}
</style>
