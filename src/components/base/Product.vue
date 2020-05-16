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

            <v-tooltip v-model="show" left color="var(--emerald)">
              <template v-slot:activator="{ on }">
                <div class="description" >
                  <span v-text="product.description" v-on="on"></span>
                </div>
              </template>
              <span v-text="product.description"></span>
            </v-tooltip>

        </div>
      </div>
      <div class="pos2" v-for="(item, j) in product.tags" :key="j" v-text="item.name"></div>
      <v-card-actions class="pos1">
        <div v-if="this.price" class="quant">
          <div v-text="product.price"></div>
          <v-icon small class="quant">fas fa-euro-sign</v-icon>
        </div>
        <div class="mngbtn">
        <v-btn name="basket" v-if="this.basket" @click="$emit('added')" class="cartbutton">
          <i class="fas fa-shopping-basket"></i>
        </v-btn>
        <v-btn class="managebutton">
          <i class="fas fa-percent"></i>
        </v-btn>
        <v-btn name="delete" v-if="this.delete" @click="$emit('removed')" class="managebutton">
          <i class="fas fa-times"></i>
        </v-btn>
        <v-btn name="edit" v-if="this.edit" @click="$emit('edited')" class="managebutton">
          <i class="far fa-edit"></i>
        </v-btn>
        </div>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
    export default {
        name: "Product",
        data () {
          return {
           show: false,
         }
        },
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
          edit: {
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
    overflow: hidden!important;
    width: 20vmax;
    height: 50px;
    transition: ease-in-out 0.3s;
    margin-bottom: 10px;
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
  .cartbutton {
    transition: 0.3s ease-in-out;
    background: var(--emerald)!important;
    display: block;
    margin-top: 5px;
  }
  .cartbutton:hover {
    scale: 1.1;
  }
  .product {
    transition: ease-in-out 0.4s;
    box-shadow: 0 0 2px black;
    margin: -5px;
  }
  .product:hover{
    box-shadow:0 0 10px black;
  }
.pos1 {
  position: absolute;
  right: 0;
  height: 100%;
}
</style>