<template>
<v-card class="basil" elevation="6">
  <v-card-title class="text-center justify-center py-6">
    <h1 class="font-weight-bold display-3 basil--text">
      <slot />
    </h1>
  </v-card-title>
</v-card>
</template>

<script>
export default {
  name: 'BaseRestH1',


  props: {

  },

}
</script>

<style lang="css" scoped>
/* Helper classes */
.basil {
  background-color: var(--ghostwhite) !important;

}
.basil--text {
  color: var(--emerald) !important;
  text-shadow: 0 0 2px grey;
}
</style>
