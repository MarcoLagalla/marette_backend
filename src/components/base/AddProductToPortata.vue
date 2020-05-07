<template>
  <div>
    <v-select :items="categories" label="Categoria del prodotto:" v-model="category" @change="choosedCategory = true"></v-select>
    <v-select :items="menu[category]" item-text="name" item-value="id" label="Selezionare prodotto:" v-model="product" :disabled="!choosedCategory"></v-select>
    <v-btn :disabled="product===''" @click="$emit('addProduct', product)">Aggiungi</v-btn>
  </div>
</template>

<script>
  export default {
    name: "AddProductToPortata",
    data: () => ({
      category: "",
      choosedCategory: false,
      product: ''
    }),
    computed: {
      menu() {
        return this.$store.getters['restaurantData/productList']
      },
      categories() {
        var cat = []
        var men = this.$store.getters['restaurantData/productList']
        Object.keys(men).forEach(function(key) {
          if(men[key].length!==0){
            cat.push(key)
          }
        });
        return cat
      }
    }
  }
</script>

<style scoped>

</style>