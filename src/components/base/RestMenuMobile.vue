<template>
  <div>
    <div v-for="(name , i) in items" :key="i" >
      <v-list-item :href="'#'+ name.name" :exact="name.name === 'HOME'" color="primary">
        <v-list-item-content>
          <div class="list">{{name.name}}</div>
        </v-list-item-content>
      </v-list-item>
    </div>
  </div>
</template>

<script>
export default {
  name: "RestMenuMobile",
  props: ['items']
}
</script>

<style scoped>
.list {
  color: white!important;
  font-weight: bold!important;
}
</style>