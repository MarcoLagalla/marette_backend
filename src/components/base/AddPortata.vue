<template>
  <form>
    <v-text-field v-model='name' type="text" label="Nome della portata" required></v-text-field>
    <v-text-field v-model='num_products' type="number" label="Numero di piatti selezionabili" required></v-text-field>
    <v-btn @click="addProduct" text>Aggiungi prodotto</v-btn>
    <base-add-product-to-portata v-for="product in products" :key="product">{{product}}</base-add-product-to-portata>
  </form>
</template>

<script>
  export default {
    name: "AddPortata",
    data: () => ({
      name: '',
      num_products: 1,
      products: [],
    }),
    methods: {
      addProduct: function() {
        if (this.products.length === 0){
          this.products.push(0)
        }
        else {
          this.products.push( this.products[this.products.length - 1] + 1)
        }
      }
    }
  }
</script>

<style scoped>

</style>