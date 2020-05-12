<template>
  <v-card color="mx-auto">
    <v-card-title class="headline" v-text="portata.name"></v-card-title>
    <v-card-subtitle v-text="'Puoi scegliere ' + portata.num_products + ' di questi prodotti:'"> </v-card-subtitle>
    <base-product v-for="product in portata.products" :key="product.id" :product="product"></base-product>
    <v-card-actions class="pos1">
      <v-btn name="delete" v-if="admin" color="red" @click="$emit('removed')">
        Elimina portata<i class="fas fa-times"></i>
      </v-btn>
      <v-btn name="edit" v-if="admin" color="blue" @click="$emit('edited')" class="managebutton">
        Modifica portata<i class="far fa-edit"></i>
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
          admin: {
            type: Boolean,
            required: false,
            default: false
          },
        },
    }
</script>

<style scoped>

</style>