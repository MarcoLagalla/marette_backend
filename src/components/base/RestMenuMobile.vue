<template>
<div>
  <v-list-item v-for="name in items" :key="name" :href="'#'+name" :exact="name === 'Home'" color="primary">
    <v-list-item-content>
      <v-list-item-title v-text="name" />
    </v-list-item-content>
  </v-list-item>
</div>
</template>

<script>
export default {
  name: "RestMenuMobile",
  props: ['items']
}
</script>

<style scoped>

</style>