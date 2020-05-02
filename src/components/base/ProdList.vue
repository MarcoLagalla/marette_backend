<template>
  <div class="menubody">
    <v-container>
      <v-row dense>
        <v-col v-for="(product, i) in products" :key="i" cols="12">
          <v-card color="#616161" dark>
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant"><div class="">
                <v-avatar class="ma-3" size="100" tile>
                  <v-img :src="product.image"></v-img>
                </v-avatar>     </div>
                <div class="">
                  <v-card-title class="headline" v-text="product.name"></v-card-title>
                  <v-card-subtitle class="pb-0" v-text="product.category"></v-card-subtitle>
                  <div class="description" v-text="product.description"></div>
                </div>
              </div>
              <div class="pos2"
              v-text="product.tags"
              >
            </div>
            <v-card-actions class="pos1">
              <div class="quant">
                <div
                v-text="product.price"
                ></div><v-icon small class="quant"> fas fa-euro-sign</v-icon></div>
                <v-btn color="red"><i class="fas fa-shopping-basket"></i></v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
export default {
  name: 'BaseProdList',
  props: ['products'],
  inheritAttrs: false,
  data: () => ({
    items: [{ //esempio di prodotto
      "id": 3,
      "name": "Insalata di cavolo",
      "description": "insalatina",
      "category": "Antipasto",
      "price": "10.00",
      "tags": [
        {
          "name": "Vegetariano",
          "icon": null,
          "description": "cibo vegano"
        }
      ],
      "discounts": [],
      "final_price": 10.0,
      "image": "media/dema.png",
      "show_image": true
    },
    { //quello che avevi prima
      color: '#952175',
      src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
      title: 'Halcyon Days',
      artist: 'Ellie Goulding',
    }
  ],
}),
}
</script>
<style scoped>
h1 {
  color: white;
  margin-bottom: 10px;
  margin-left: 10px;
}
.pos1 {
  position: absolute;
  bottom: 0!important;
  right: 0;
}
.pos2 {
  position: absolute;
  top: 0!important;
  right: 0;
  padding: 15px;
}
.menubody {
  position: relative;
  left: 0;
  top: 0;
  bottom: 0;
  width: 100%;
  background: #35302D;
}
.quant {
  padding: 5px;
  display: flex;
  align-items: center;
}
.description {
  padding: 15px;
}
</style>
