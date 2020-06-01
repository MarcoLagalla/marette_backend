<template>
  <div class="portprod">
    <v-select :items="categories" label="Categoria del prodotto:" v-model="category" @change="choosedCategory = true"></v-select>
    <v-select :items="menu[category]" multiple chips item-text="name" item-value="id" label="Selezionare prodotto:" v-model="productIds" :disabled="!choosedCategory"></v-select>
    <button class="managebutton" :disabled="productIds.length===0" @click="added_products">Aggiungi</button>
  </div>
</template>

<script>
  export default {
    name: "AddProductToPortata",
    data: () => ({
      category: "",
      choosedCategory: false,
      productIds: []
    }),
    methods: {
      added_products: function() {
        var prod = []
        this.menu[this.category].forEach( (product) =>{
          if ( this.productIds.includes(product.id))
            prod.push(product)
        });
        this.category = ""
        this.choosedCategory = false
        this.productIds = []
        this.$emit('added_product', prod)
      }
    },
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
.managebutton {
  margin: 10px;
}
</style>