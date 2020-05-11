<template>
  <div class="menubody">
    <v-container>
      <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" >
          <base-product :product="product" :delete="true" :price='true' @removed="removeProduct(product)"></base-product>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
export default {
  name: "BaseProdList",
  props: ["products"],
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


</style>
