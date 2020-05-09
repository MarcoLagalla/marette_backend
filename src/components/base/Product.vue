<template>
  <v-card color="#616161" dark class="product">
    <div class="d-flex flex-no-wrap justify-space-between">
      <div class="quant">
        <div class>
          <v-avatar class="ma-3" size="100" tile>
            <v-img :src="product.image"></v-img>
          </v-avatar>
        </div>
        <div class>
          <v-card-title class="headline" v-text="product.name"></v-card-title>
          <v-card-subtitle class="pb-0" v-text="product.category"></v-card-subtitle>
          <div class="description" v-text="product.description"></div>
        </div>
      </div>
      <div class="pos2" v-for="(item, j) in product.tags" :key="j" v-text="item.name"></div>
      <v-card-actions class="pos1">
        <v-btn v-if="this.delete" color="red" @click="$emit('removed')">
          <i class="fas fa-shopping-basket">Elimina</i>
        </v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
    export default {
        name: "Product",
        props:{
          product: {
            type: Object,
            required: true
          },
          delete: {
            type: Boolean,
            required: false,
            default: false
          },
        },
        methods: {

        }
    }
</script>

<style scoped>

</style>