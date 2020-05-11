<template>
  <v-card color="var(--ming)" dark class="product">
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
        <div v-if="this.price" class="quant">
          <div v-text="product.price"></div>
          <v-icon small class="quant">fas fa-euro-sign</v-icon>
        </div>
        <div class="mngbtn">
        <v-btn name="basket" v-if="this.basket" @click="$emit('added')" class="managebutton">
          <i class="fas fa-shopping-basket"></i>
        </v-btn>
        <v-btn class="managebutton">
          <i class="fas fa-percent"></i>
        </v-btn>
        <v-btn name="delete" v-if="this.delete" @click="$emit('removed')" class="managebutton">
          <i class="fas fa-times"></i>
        </v-btn>
        </div>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
    export default {
        name: "Product",
        props:{
          product: {
            type: Object,
            required: true
          },
          delete: {
            type: Boolean,
            required: false,
            default: false
          },
          basket: {
            type: Boolean,
            required: false,
            default: false
          },
          price: {
            type: Boolean,
            required: false,
            default: false
          },
        },
        methods: {

        }
    }
</script>

<style scoped>
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
  background: var(--chilli)!important;
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
.pos1 {
  position: absolute;
  bottom: 0 !important;
  right: 0;
}
.pos2 {
  position: relative;
  top: 0 !important;
  right: 0;
  padding: 15px;
}

</style>