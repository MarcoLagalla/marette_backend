<template>
<div class="menubody">
  <v-container>
    <v-row dense>
      <v-col v-for="(product, i) in products" :key="i" cols="12">
        <v-card color="#616161" dark>
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="headline" v-text="product.name"></v-card-title>
              <v-card-subtitle v-text="product.description"></v-card-subtitle>
            </div>
            <v-card-actions>
              <v-btn color="red">aggiungi al carrello</v-btn>
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
  name: 'BaseMenu',
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
.menubody {
  position: relative;
  left: 0;
  top: 0;
  bottom: 0;
  width: 100%;
  background: #35302D;
}
</style>
