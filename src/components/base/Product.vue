<template>

    <div class="product">
        <div class="cardpos">
            <v-avatar class="imag" size="100" tile>
                <v-img :src="product.image"></v-img>
            </v-avatar>
            <span class="title" v-text="product.name"></span>
            <p class="description" v-text="product.description"></p>
            <div class="pos2">tag tag tag</div>
            <v-row v-if="this.price" class="quant">
                <div v-text="product.price"></div>
                <v-icon small class="eur">fas fa-euro-sign</v-icon>
            </v-row>
        </div>
    </div>
  <!--
                                                   pulsanti vecchi della card
  <div v-if="this.price" class="quant">
          <div v-text="product.price" ></div>
          <v-icon small class="quant">fas fa-euro-sign</v-icon>
        </div>
        <div class="mngbtn">
        <v-btn name="basket" v-if="this.basket" @click="$emit('added')" class="managebutton">
          <i class="fas fa-shopping-basket"></i>
        </v-btn>
        <v-btn name="edit" v-if="this.edit" @click="$emit('edited')" class="managebutton">
          <i class="far fa-edit"></i>
        </v-btn>
        <v-btn name="discount" v-if="this.discount" @click="toggleShowDiscounts"  class="managebutton">
          <i class="fas fa-percent"></i>
        </v-btn>
        <v-btn name="delete" v-if="this.delete" @click="$emit('removed')" class="managebutton">
          <i class="fas fa-times"></i>
        </v-btn>
        </div>
                                          expand transition
  <v-expand-transition>
    <div v-show="showDiscounts" :style="{width:'300px',margin:'0 auto'}">
      <p>Lista sconti disponibili:</p>

            <v-list shaped >
                <v-list-item-group
                        v-model="selected_discounts"
                        multiple
                >
                    <template v-for="(campo, i) in discounts_list" >
                        <v-divider
                                v-if="!campo"
                                :key="`divider-${i}`"
                        ></v-divider>
                        <v-list-item
                                v-else
                                :key="`item-${i}`"
                                :value="campo.id"
                                active-class="green--text text--accent-2"
                        >
                            <template v-slot:default="{ active, toggle }" >
                                <v-list-item-content>
                                    <v-list-item-title v-text="campo.title"></v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-action>
                                    <v-checkbox
                                            :input-value="active"
                                            :true-value="campo"
                                            color="green accent-2"
                                            @click="toggle"
                                    ></v-checkbox>
                                </v-list-item-action>
                            </template>
                        </v-list-item>
                    </template>
                </v-list-item-group>
            </v-list>
        <br>
        <v-expand-transition>
        <div v-if="selected_discounts.length !== 0">
            <v-btn class="managebutton" @click="$emit('add_discount_to_product', selected_discounts)" > Aggiungi sconto al prodotto</v-btn>
        </div>
        </v-expand-transition>
        <v-btn class="managebutton" name="new_discount_add" v-if="this.new_discount_add" @click="$emit('new_discount')" > Inserisci nuovo sconto</v-btn>
    </div>
    </v-expand-transition>

    -->

</template>

<script>
    // eslint-disable-next-line no-unused-vars
      import {mapActions} from "vuex";



    export default {
        name: "Product",



        data () {
          return {
           show: false,
           showDiscounts: false,
           selected_discounts: [],

         }
        },

        props:{
          product: {
            type: Object,
            required: true
          },

          discounts_list: {
              type: Array,
              required: true,
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
          discount: {
            type: Boolean,
            required: false,
            default: false
          },
          new_discount_add: {
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

          toggleShowDiscounts() {
                this.showDiscounts = !this.showDiscounts;
                if (this.showAddDiscount === true){
                  this.showAddDiscount = false;
                }

            },

        }
    }
</script>

<style scoped>
    .imag {
        border-radius: 10px;
        box-shadow: 0 0 2px black;
    }

    h1 {
        color: white;
        margin-bottom: 10px;
        margin-left: 10px;
    }

    .eur {
        padding-left: 5px;
        padding-right: 10px;
    }

    .title {
        font-size: 1.3em !important;
        position: absolute;
        top: 0;
        left: 100px;
        padding: 8px;
        text-transform: capitalize;
        font-weight: normal !important;
    }

    .description {
        position: absolute;
        color: darkslategrey;
        letter-spacing: 2px;
        font-size: 0.9em;
        top: 35px;
        left: 100px;
        padding: 10px;
        width: 50%;
        height: 50px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    .quant {
        position: absolute;
        top: 30px;
        right: 0px;
        padding: 10px;
    }

    .cardpos {
        position: relative;

    }

    .managebutton {
        transition: 0.3s ease-in-out;
        background: var(--emerald) !important;
        display: block;
        margin-top: 5px;
    }

    .managebutton:hover {
        scale: 1.1;
    }

    .cartbutton {
        transition: 0.3s ease-in-out;
        background: var(--emerald) !important;
        display: block;
        margin-top: 5px;
    }

    .cartbutton:hover {
        scale: 1.1;
    }

    .product {
        transition: ease-in-out 0.4s;
        margin: -5px;
        background: var(--ghostwhite);
        padding: 5px;

    }

    .product:hover {
        box-shadow: 0 2px 10px #828282;

    }

    .pos2 {
        position: absolute;
        bottom: 0;

        width: 50%;
        left: 50%;
    }
</style>