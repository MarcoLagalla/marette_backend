<template>
  <v-card color="mx-auto">
    <v-card-title class="headline" v-text="portata.name"></v-card-title>
    <v-card-subtitle v-text="'Puoi scegliere ' + portata.num_products + ' di questi prodotti:'"> </v-card-subtitle>
    <base-product v-for="product in portata.products" :key="product.id" :product="product"></base-product>
    <v-card-actions class="pos1">
      <v-btn v-if="this.delete" color="red" @click="$emit('removed')">
        <i class="fas fa-shopping-basket">Elimina</i>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
    export default {
        name: "Portata",
        props:{
          portata: {
            type: Object,
            required: true
          },
          delete: {
            type: Boolean,
            required: false,
            default: false
          },
        },
    }
</script>

<style scoped>

</style>