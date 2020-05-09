<template>
  <div class="portprod">
    <v-select :items="categories" label="Categoria del prodotto:" v-model="category" @change="choosedCategory = true"></v-select>
    <v-select :items="menu[category]" multiple chips item-text="name" item-value="id" label="Selezionare prodotto:" v-model="productId" :disabled="!choosedCategory"></v-select>
    <v-btn :disabled="productId===''" @click="added_product">Aggiungi</v-btn>
  </div>
</template>

<script>
  export default {
    name: "AddProductToPortata",
    data: () => ({
      category: "",
      choosedCategory: false,
      productId: ''
    }),
    methods: {
      added_product: function() {
        var prod = {}
        const prodId = this.productId
        this.menu[this.category].forEach(function (product) {
          if (product.id === prodId)
            prod = product
        });
        this.category = ""
        this.choosedCategory = false,
        this.productId = ''
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
.portprod {
  ;
}
</style>