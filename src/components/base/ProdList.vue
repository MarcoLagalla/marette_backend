<template>
  <div class="menubody">
    <v-container>
      <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" md="6" lg="4" >
          <base-product :product="product" :discounts_list="discounts_list"  :edit="admin" :discount="admin" :new_discount_add="admin" :delete="admin" :basket="!admin" :price='true' @add_discount_to_product="add_discount_to_product(product,$event)" @removed="del_Product(product)" @new_discount="toggleAddDiscount"></base-product>
        </v-col>
      </v-row>
    </v-container>


      <sweet-modal ref="modal"><br>
            <v-form @submit.prevent="add_discount_to_list">
                <v-text-field outlined
                              v-model="discount_name"
                              type="text"
                              label=" Inserire nome sconto"
                              id="discount_name"
                              name="discount_name"
                              required
                ></v-text-field>
                Tipo di sconto:
                <v-radio-group v-model="discount_type" row>
                    <v-radio
                            :label="'Fisso'"
                            :value="'Fisso'"
                    ></v-radio>
                    <v-radio
                            :label="'Percentuale'"
                            :value="'Percentuale'"
                    ></v-radio>
                </v-radio-group>
                <v-text-field outlined
                              v-model="discount_price"
                              type="number"
                              label=" Inserire sconto in decimale o percentuale"
                              id="discount_price"
                              name="discount_price"
                              required
                ></v-text-field>
                <v-btn type="submit" class="managebutton">Aggiungi Sconto</v-btn>
            </v-form>
        </sweet-modal>
  </div>

</template>
<script>
    import {mapActions} from "vuex";
    import {SweetModal} from "sweet-modal-vue";



export default {
  name: "BaseProdList",
  props: ["products", 'admin'],
  inheritAttrs: false,

  components: {
      SweetModal,
  },


  data() {
      return{
          showAddDiscount: false,
          discount_name: '',
          discount_price: '',
          discount_type: '',
      }

  },

    computed:{

          discounts_list() {
                return this.$store.getters['restaurantData/discounts']
            },
        },


    created() {
        this.$store.dispatch("restaurantData/getListDiscounts")
    },


    methods: {

      ...mapActions('restaurantData', ['removeProduct']),
      ...mapActions('restaurantData', ['addNewDiscount']),
      ...mapActions('restaurantData', ['addDiscountToProduct']),

      add_discount_to_list: function () {
        let data = {
            "title": this.discount_name,
            "type": this.discount_type,
            "value": this.discount_price,
        };
        this.addNewDiscount(data)
      },

      add_discount_to_product: function (prod,selected_discounts) {
          let x = this.products.indexOf(prod);
          let p_id= this.products[x].id;
          let data = {
              'discounts': selected_discounts,
          };
           const formData = new FormData();
          formData.append('data', JSON.stringify(data));

          let payload = {
              'data': formData,
              p_id,
          };
          this.addDiscountToProduct(payload)
      },

      del_Product: function(prod){
        let x = this.products.indexOf(prod);
        let prod_id = this.products[x].id;
        this.removeProduct(
          prod_id
        ).then(resp => {

            this.products.splice(this.products.indexOf(prod), 1);
            alert(resp.message)

        })

        .catch(error => {

          alert(error.error)
        });


      },

      toggleAddDiscount() {
          this.$refs.modal.open()
      },
    },
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



</style>
