<template>
  <div class="menubody">
    <v-container>
      <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" md="6" lg="4" >
          <base-product :product="product" :delete="admin" :price="true" @open_card="toggleCardModal(product)" @delete_prod_discount="add_discount_to_product($event, product, 0)"  @removed="del_Product(product)" ></base-product>
        </v-col>
          <v-col cols="12" md="6" lg="4">
              <base-add-new-product :category='category' v-if="admin" :admin="admin"></base-add-new-product>
          </v-col>
      </v-row>
    </v-container>
      <v-snackbar
      v-model="toggleSnackbar"
      :timeout="3000"
      >
      {{text}}
      <v-btn
        color="blue"
        text
        @click="toggleSnackbar = false"
      >
        Chiudi
      </v-btn>
      </v-snackbar>

      <!--
        Per inserire un icona presa da fontawesome come icona della tab bisogna passar l'i tag come stringa, quindi come ho fatto
        sotto basta prendere il tag in questione e sostituire :


        < con &lt
        > con &gt
        " con &quot
                  <base-product :product="product" :discounts_list="discounts_list"  :edit="admin" :discount="admin" :new_discount_add="admin" :delete="admin" :basket="!admin" :price='true' @open_card="toggleCardModal" @add_discount_to_product="add_discount_to_product(product,$event)" @removed="del_Product(product)" @new_discount="toggleAddDiscount"></base-product>

      -->
      <sweet-modal ref="modal"><br>
          <sweet-modal-tab  title="Aggiungi Sconto" id="sconta_prodotto" icon="&lt;i class=&quot;fas fa-percent&quot;&gt;&lt;i&gt;">
                <label>Aggiungi sconto/i</label>
              <multiselect
                      v-model="selected_discounts"
                      track-by="id"
                      :custom-label="customLabel"
                      placeholder="Seleziona uno Sconto"
                      tag-placholder="Aggiungi questo come nuovo sconto"
                      selectLabel="Clicca per selezionare"
                      deselectLabel="Clicca per Rimuovere"
                      selectedLabel="Selezionato"
                      :block-keys="['Tab', 'Enter']"
                      :options="discounts_list"
                      :searchable="false"
                      :internal-search="false"
                      :multiple="true"
                      :taggable="true"
                      @tag="addTag">
              </multiselect>
              <!--{{modal_product}}-->
              <br><br>

              <v-btn color="var(--ming)" :disabled="selected_discounts.length === 0" @click="add_discount_to_product(selected_discounts, modal_product, 1)" > Aggiungi Sconto al prodotto</v-btn>
              <br><br><br><br><br>

              <!--v-btn name="discount"  @click="toggleShowDiscounts"  class="managebutton">
              Mostra sconti Disponibili
          </v-btn>
              <v-expand-transition>
                <div v-show="showDiscounts" :style="{width:'200px'}">
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
                                    active-class="blue--text text--accent-2"
                                >
                                <template v-slot:default="{ active, toggle }" >
                                    <v-list-item-content>
                                        <v-list-item-title v-text="campo.title"></v-list-item-title>
                                    </v-list-item-content>
                                    <v-list-item-action>

                                        <v-checkbox
                                            :input-value="active"
                                            :true-value="campo"
                                            color="blue accent-2"
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
                <v-btn class="managebutton" @click="add_discount_to_product(selected_discounts)" > Aggiungi Sconto al prodotto</v-btn>
                </div>
                </v-expand-transition>
                </div>
              </v-expand-transition-->

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
                <v-btn dark color="var(--ming)" type="submit" >Aggiungi Sconto</v-btn>
            </v-form>
          </sweet-modal-tab>
          <sweet-modal-tab title="Modifica Prodotto" id="tab2" icon="&lt;i class=&quot;fas fa-edit&quot;&gt;&lt;i&gt;"></sweet-modal-tab>
        </sweet-modal>
  </div>

</template>
<script>
    import {mapActions} from "vuex";
    import {SweetModal, SweetModalTab} from "sweet-modal-vue";
    import Multiselect from 'vue-multiselect'




export default {
  name: "BaseProdList",
  props: ["products", 'admin',"category"],
  inheritAttrs: false,

  components: {
      SweetModal,
      SweetModalTab,
      Multiselect,
  },


  data() {
      return{
          showAddDiscount: false,
          discount_name: '',
          discount_price: '',
          discount_type: '',
          showDiscounts: false,
          selected_discounts: [],
          value:[],
          modal_product:{},
          text: '',
          toggleSnackbar: false,
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

      add_discount_to_list: function (event) {
        let data = {
            "title": this.discount_name,
            "type": this.discount_type,
            "value": this.discount_price,
        };
        this.addNewDiscount(data);
        event.target.reset();
      },

        /*
        add discount to product viene utilizzato per eliminare o aggiungere sconti a un determinato prodotto, se entra nell'if
        vuol dire che sta cercando di eliminare lo sconto, quindi in quel caso selected_discounts è lo sconto, una volta fuori dall'if all'interno
        di selected mi ritrovo gli sconti del prodotto - quello eliminato. mentre nel caso di aggiunta è tutto quello fuori if e selected discounts contiene
        gli sconti da aggiungere
         */

      add_discount_to_product: function (selected_discounts, prod, choice) {
          let discountsId = [];

          if (choice===0){

              let arrayLength = prod.discounts.length;
              for(let i=0; i< arrayLength; i++){
                  if(prod.discounts[i]===selected_discounts){

                    prod.discounts.splice(i,1);
                    selected_discounts= prod.discounts;
                  }
              }

          }
          let arrayLength = selected_discounts.length;
          for (let i = 0; i < arrayLength; i++) {
              discountsId.push(selected_discounts[i].id)
          }

          let x = this.products.indexOf(prod);

          let p_id= this.products[x].id;

          let discounts = {
              'discounts': discountsId,
          };

          let data = {
              discounts,
              'id':p_id,
          };
          this.$refs.modal.close()
          this.addDiscountToProduct(data).then(resp=> {
              // si esegue solo se sto aggiungendo prodotti e li aggiunge subito a vista controllando che non siano doppioni
              if (choice===1){
              for (let i = 0; i < arrayLength; i++) {
                  if (prod.discounts[i]!==selected_discounts[i]) {
                      prod.discounts.push(selected_discounts[i]);
                  }
              }
              this.text=resp.message;
              }
              else {
              this.text='Sconto eliminato'
              }
              this.toggleSnackbar=true ;

          })

              .catch(error => {
                  alert(error.error)
              });


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


      toggleCardModal(prod) {
        this.modal_product=prod;
        this.selected_discounts=prod.discounts;
        this.$refs.modal.open()
      },

      toggleShowDiscounts() {
        this.showDiscounts = !this.showDiscounts;
        if (this.showAddDiscount === true){
          this.showAddDiscount = false;
        }
      },

    addTag (newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
      }
      this.value.push(tag)
    },

    customLabel (option) {
          if(option.type==='Fisso') {
              return `${option.title} - Sconto di ${option.value} €`
          }else{
              return `${option.title} - Sconto del ${option.value} %`
          }


    },

    },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

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
  background: var(--ming)!important;
  display: block;
  margin-top: 5px;
  color:white;
}
.managebutton:hover {
  scale: 1.1;
}

.product {
    transition: ease-in-out 0.4s;
    background: var(--ghostwhite);
    width: 365.5px;
    height: 110px;
    margin: 6.5px;
    padding: 5px;
    position: relative;

}

.product:hover {
    box-shadow: 0 2px 10px #828282;
    cursor: pointer;

}


</style>
