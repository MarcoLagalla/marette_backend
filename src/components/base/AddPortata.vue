<template>
  <div class="addportata">
    <v-text-field outlined v-model='name' type="text" label="Nome della portata" required></v-text-field>
    <v-text-field outlined v-model='num_products' type="number" label="Numero di piatti selezionabili" required></v-text-field>

    <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" >
          <base-product :product="product" :delete="true" @removed="removeProduct(product)"></base-product>
        </v-col>
      </v-row>

    <v-btn @click="showAdd=true" text>Aggiungi prodotto</v-btn>
    <base-add-product-to-portata v-show="showAdd" @added_product="addProduct($event)"></base-add-product-to-portata>

    <v-btn @click="submitPortata" :disabled="products.length===0" text>Salva portata</v-btn>
  </div>
</template>

<script>

  export default {
    name: "AddPortata",
      data: () => ({
      name: '',
      num_products: 1,
      showAdd: false,
      products: []
    }),
    methods: {
      addProduct: function(prod) {
        this.products.push(prod);
        this.showAdd =  false
      },
      removeProduct: function(prod){
        this.products.splice(this.products.indexOf(prod), 1);
      },
      submitPortata: function(){
          var portata = {
              name: this.name,
              num_products: this.num_products,
              products: this.products
          }
          this.name = ''
          this.num_products = 1
          this.showAdd = false
          this.products = []
          this.$emit('added_portata', portata)
      }
    }
  }
</script>

<style scoped>
.addportata {

}
</style>