<template>

    <div >
        <v-btn
                class="delete_button"
                name="delete"
                v-if="this.delete"
                @click="$emit('removed')"
                depressed
                bottom
                fab
                dark
                x-small
                color="var(--ming)" >
            <i class="fas fa-times"></i>
        </v-btn>
        <div class="product" @click="$emit('open_card')">
            <v-avatar class="imag" size="100" tile>
                <v-img :src="product.image"></v-img>
            </v-avatar>

            <span class="title" v-text="product.name"></span>
            <p class="description" v-text="product.description"></p>

            <v-row class="tags_class" v-if="product.tags.length>0" justify="center">
                <div v-if="check_tags('GlutenFree',product)" class="tooltip" >
                <span class="fa-stack fa-xs" >
                <i class="fas fa-bread-slice fa-stack-1x" title="Gluten Free" style="color: peru"></i>
                <i class="fas fa-ban fa-stack-2x" style="color: red; opacity: 0.7;"></i>
                </span>
                <span class="tooltiptext">Gluten Free</span>
                </div>
                <div v-if="check_tags('Vegetariano',product)" class="tooltip"><i class="fas fa-carrot" style="color: orange"></i><span class="tooltiptext">Vegetariano</span></div>
                <div v-if="check_tags('Piccante',product)" class="tooltip"><i class="fas fa-pepper-hot" style="color: red"></i><span class="tooltiptext">Piccante</span></div>
                <div v-if="check_tags('Vegano',product)" class="tooltip"><i class="fas fa-seedling" style="color: green"></i><span class="tooltiptext">Vegano</span></div>

            </v-row>

            <div class="quant">
                <v-row>
                <div :class="product.discounts.length>0?'discount_true':'price_text'" v-text="product.price"></div>
                <v-icon class="eur" small>fas fa-euro-sign</v-icon>
                </v-row>
                <v-row v-if="product.discounts.length>0">
                <div  class="price_text" v-text="product.final_price"></div>
                <v-icon class="eur" small>fas fa-euro-sign</v-icon>
                </v-row>
            </div>
        </div>
        <!-- Potrebbe essere un loop infinito il for dei discount, se ci sono tantissimi sconti, bisogna decidere se controllare la cosa o meno -->
        <div v-if="product.discounts.length>0">
            <v-chip  v-for="(discount, i) in product.discounts" :key="i" :v-if="product.discounts.length<6" class="discount_banner" @click:close="$emit('delete_prod_discount', discount)" label :close="close_discount" x-small color="var(--ming)" text-color="white">{{check_type(discount)}}</v-chip>
        </div>
    </div>


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
           discount_type: '',

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
          close_discount: {
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

            check_type(discount) {
                let mystring = discount.value;
              if (discount.type==='Fisso'){
                  this.discount_type=' €'
              }
              else {
                  mystring = mystring.replace('.00','');
                  this.discount_type=' %'
              }
                return mystring + this.discount_type;

            },

            check_tags(textTag, prod) {
              let arrayLength = prod.tags.length;
              for(let i=0; i< arrayLength; i++){
              if (prod.tags[i].name===textTag){
                return true;
              }
              }
            }

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
        font-size: 1em !important;
        position: absolute;
        top: 0;
        left: 100px;
        padding: 2% 3% 3% !important;
        line-height: 0.6cm !important;
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
        padding: 2% 3% 3%;
        margin-top:2%;
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

    .delete_button {
        z-index: 2;
        top:15px;
        left:97%;
    }



    .product {
        transition: ease-in-out 0.4s;
        margin: -5px;
        background: var(--ghostwhite);
        padding: 5px;
        position: relative;
        z-index: 1;


    }

    .product:hover {
        box-shadow: 0 2px 10px #828282;
        cursor: pointer;

    }

    .price_text{
        width: 50px;
        text-decoration: none;
    }

    .discount_true{
        width: 50px;
        text-decoration: line-through;
    }

    .tags_class{
        position: absolute;
        top: 50%;
        /*left: 25%;*/
        width: 60%;
        height: 50px;
        padding: 15px 6%;
        margin-left: 30%;
    }

    .discount_banner{
        box-shadow: 0 0 2px black;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        padding: 3% 3%;
    }

    .tooltip .tooltiptext {
      visibility: hidden;
      width: 80px;
      color: #fff;
      background-color: var(--charcoal);
      text-align: center;
      border-radius: 6px;
      padding: 5px 0;
      position: absolute;
      z-index: 2 !important;
      bottom: 100%;
      left: 50%;
      margin-left: -40px;
      font-size: 0.8em;
      opacity: 0;
      transition: opacity 1s;
    }

    .tooltip .tooltiptext::after {
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: var(--charcoal) transparent transparent  transparent;

    }

    .tooltip:hover .tooltiptext {
      visibility: visible;
        opacity: 1;

    }


    .pos2 {
        position: absolute;
        bottom: 0;

        width: 50%;
        left: 50%;
    }
</style>
