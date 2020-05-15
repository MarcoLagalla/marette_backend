<template>
  <div class="menubody">
    <v-container>
      <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" >
          <base-product :product="product" :delete="admin" :basket="!admin" :price='true' @removed="removeProduct(product)"></base-product>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
export default {
  name: "BaseProdList",
  props: ["products", 'admin'],
  inheritAttrs: false,
  data: () => ({

  }),
    methods: {
      removeProduct: function(prod){
        this.products.splice(this.products.indexOf(prod), 1); //TODO: rimuoverlo veramente dai prodotti
      }
    }
};
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
  background: var(--whitesmoke);
}
.quant {
  padding: 5px;
  display: flex;
  align-items: center;
}
.description {
  padding: 15px;
}
.managebutton {
  transition: 0.3s ease-in-out;
  background: var(--emerald)!important;
  display: block;
  margin-top: 5px;
}
.managebutton:hover {
  scale: 1.1;
}
.product {
  transition: ease-in-out 0.4s;
  box-shadow: 0 0 2px black;
}
.product:hover{
  box-shadow:0 0 10px black;
}


</style>
