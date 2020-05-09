<template>
<v-card color="basil">
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
  background-color: #FFFBE6 !important;
}
.basil--text {
  color: #356859 !important;
}
</style>
