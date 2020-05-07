<template>
  <form>
    <v-text-field v-model='name' type="text" label="Nome della portata" required></v-text-field>
    <v-text-field v-model='num_products' type="number" label="Numero di piatti selezionabili" required></v-text-field>

    <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" >
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
                <div class="quant">
                  <div v-text="product.price"></div>
                  <v-icon small class="quant">fas fa-euro-sign</v-icon>
                </div>
                <v-btn color="red">
                  <i class="fas fa-shopping-basket">Elimina</i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>
      </v-row>

    <v-btn @click="showAdd=true" text>Aggiungi prodotto</v-btn>
    <base-add-product-to-portata v-show="showAdd" @added_product="addProduct($event)"></base-add-product-to-portata>

  </form>
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
      }
    }
  }
</script>

<style scoped>

</style>