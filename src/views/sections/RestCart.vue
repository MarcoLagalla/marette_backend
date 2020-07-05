<template>
    <div>
        <v-btn
                class="basket_button"
                depressed
                @click="showCart = !showCart"
                color="var(--whitesmoke)" >
            <!--span style="color: var(--darkslate); font-size: 1em">{{ selected_items.length + (selected_items.length > 1 || selected_items.length === 0 ? " Prodotti" : " Prodotto") }}</span--><i style="color: var(--darkslate)" class="fas fa-shopping-basket fa-lg"></i>
        </v-btn>
      <v-scroll-x-reverse-transition>
        <div class="basket_div" v-if="showCart" >
            <div v-if="(selected_items.length > 0 || selected_menus.length > 0 ) && !verified">
                <div>
                <v-row v-for="(item,i) in selected_items" v-bind:key="i"  >
                    <v-col style="padding: 8px" cols="8">
                        <p style="font-size: 0.9em; text-align: left; margin-bottom: auto"><strong>{{ item.quantity }}</strong> - {{ item.product.name }} - {{(item.product.final_price*item.quantity).toFixed(2)}} <i class="fa fa-euro-sign"></i></p>
                    </v-col>
                    <v-col style="padding: 8px" cols="4">
                        <button @click="removeProdFromCart(item)"><i class="fa fa-trash"></i></button>
                    </v-col>
                </v-row>
                </div>
                <div>
                <v-row v-for="(menu,j) in selected_menus" v-bind:key="j"  >
                    <v-col style="padding: 8px" cols="8">
                        <p style="font-size: 0.9em; text-align: left; margin-bottom: auto"><strong>{{ menu.quantity }}</strong> - {{ menu.menu.name }} - {{(menu.menu.price*menu.quantity).toFixed(2)}} <i class="fa fa-euro-sign"></i></p>
                    </v-col>
                    <v-col style="padding: 8px" cols="4">
                        <button @click="removeMenuFromCart(menu)"><i class="fa fa-trash"></i></button>
                    </v-col>
                </v-row>
                </div>
            <v-divider style="margin-bottom: 5px"></v-divider>
            <p>Totale : {{total}} <i class="fa fa-euro-sign"></i></p>
              <v-btn
                      class="btn_in_cart"
                      @click="checkOut">
                            Check out
              </v-btn>

            </div>

            <div v-if="selected_items.length === 0 && selected_menus.length === 0">
              <p>Il Carrello è vuoto!</p>
            </div>
            <div v-if="verified">
                <p>Ordine Inviato!</p>
                <v-btn class="btn_in_cart" @click="resetCart()"> Fai un altro ordine </v-btn>
            </div>
        </div>
      </v-scroll-x-reverse-transition>
        </div>
</template>

<script>
        import {mapActions} from "vuex";

    export default {
        name: "RestCart",

        data () {
            return{

              showCart: false,
              verified: false,

            }
        },

        computed:{
            total() {
              let total = 0.00;
              let arrayLength = this.selected_items.length;
              for(let i = 0; i < arrayLength; i++) {

                total += +(this.selected_items[i].product.final_price*this.selected_items[i].quantity);
              }
              arrayLength = this.selected_menus.length;
              for(let i = 0; i < arrayLength; i++) {

                total += +(this.selected_menus[i].menu.price*this.selected_menus[i].quantity);
              }

              return total.toFixed(2);
            },

            selected_items() {
                return this.$store.getters['userProfile/cart'].selected_items

            },

            selected_menus() {
                return this.$store.getters['userProfile/cart'].selected_menus

            },


        },

        methods:{
                  ...mapActions('restaurantData', ['addOrderToRestaurant']),
                    ...mapActions('userProfile', ['deleteProdCart','deleteMenuCart','resetItemInCart']),

        checkOut(){
            this.verified = true;
            let itemsCheckout = [];
            let menusCheckout = [];
            if(this.selected_items.length>0) {
                let arrayLength = this.selected_items.length;
                for (let i = 0; i < arrayLength; i++) {
                    let element = {
                        'product': this.selected_items[i].product.id,
                        'quantity': this.selected_items[i].quantity,
                    };
                    itemsCheckout.push(element)
                }
            }

            if(this.selected_menus.length>0) {
                let arrayLength = this.selected_menus.length;
                for (let i = 0; i < arrayLength; i++) {
                    let element = {
                        'menu': this.selected_menus[i].menu.id,
                        'quantity': this.selected_menus[i].quantity,
                    };
                    menusCheckout.push(element)
                }
            }
            
        let payload = {
            'items' : itemsCheckout,
            'menus_items': menusCheckout,
         };

          this.addOrderToRestaurant(payload);

        },

        removeProdFromCart(item) {
            this.deleteProdCart(item)

        },

        removeMenuFromCart(item) {
            this.deleteMenuCart(item)

        },

        resetCart() {
            this.resetItemInCart();
            this.verified = false;
        }


        }
    }
</script>

<style scoped>

    .basket_div{
      position: fixed;
      padding: 20px 15px !important;
      top:45%;
      left:85%;
      width: 230px;
      background-color: var(--whitesmoke);
      right: 20px !important;
      z-index: 2;
      box-shadow: 0 0 4px black !important;
      text-align: center;
    }


  .basket_button{
      position: fixed;
      padding: 15px !important;
      top:38%;
      left:96%;
      width: 65px !important;
      height: 50px !important;
      z-index: 2;
      display: block;
      box-shadow: 0 0 4px black !important;
  }

  .btn_in_cart{
      position: relative;
      font-size: 0.7em !important;
      margin-top: 5px;
      padding: 5px !important;
      box-shadow: 0 0 2px black !important;
  }

</style>