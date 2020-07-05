<template>
  <div class="menubody">
    <v-container>
      <v-row >
        <v-col v-for="(product, i) in products" :key="i" cols="12" md="6" lg="4" >
          <base-product :product="product" :delete="admin" :cart="!admin" :close_discount="admin" :price="true" @open_card="toggleCardModal(product)" @delete_prod_discount="add_discount_to_product($event, product, 0)" @add_to_cart="add_to_cart_action(product)"  @removed="del_Product(product)" ></base-product>
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
          <sweet-modal-tab title="Info" id="info_prodotto" icon="&lt;i class=&quot;fas fa-info&quot;&gt;&lt;i&gt;">
              <v-row>
                <v-col cols="6">
                    <v-img  size="3" :src="modal_product.image"></v-img>
                </v-col>
                <v-col cols="6">
                    <p>Nome : {{modal_product.name}}</p>
                    <p>Descrizione : {{modal_product.description}}</p>
                    <p>Prezzo : <span :class="showSlash?'discount_true':'price_text'" v-text="modal_product.price"></span> <v-icon class="eur" small>fas fa-euro-sign</v-icon></p>
                    <p v-if="showSlash" >Prezzo Scontato : <span class="price_text" v-text="modal_product.final_price"></span> <v-icon class="eur" small>fas fa-euro-sign</v-icon></p>

                </v-col>
              </v-row>
          </sweet-modal-tab>

          <sweet-modal-tab v-if="admin" title="Modifica Prodotto" id="modifica_prodotto" icon="&lt;i class=&quot;fas fa-edit&quot;&gt;&lt;i&gt;">
              <form @submit.prevent="update_Product">
            <v-row>
                <v-col cols="6">
              <picture-input
                        v-if="showPicture"
                        ref="productImage"
                        @change="onChanged"
                        :prefill="modal_product.image"
                        :width="200"
                        :height="200"
                        :zIndex="0"
                        size="5"
                        :crop="true"
                        :changeOnClick="false"
                        accept="image/jpeg, image/png, image/gif"
                        buttonClass="ui button primary"
                          :customStrings="{
                            upload: '<h1>Carica immagine</h1>',
                            drag: 'Trascina qui la un immagine di profilo o clicca per selezionarla',
                            change: 'Cambia foto',
                          }">
                </picture-input>
                </v-col>
                <v-col cols="6">
              <v-text-field light class="field" type="text" outlined label="Nome" :disabled="!admin"  v-model='modal_product.name'></v-text-field>
              <v-text-field light class="field" type="number" outlined label="Prezzo" :disabled="!admin"  v-model='modal_product.price'></v-text-field>
              <v-textarea light class="field" type="text" outlined label="Descrizione" :disabled="!admin"  v-model='modal_product.description'></v-textarea>
                <multiselect
                      v-model="modal_product.tags"
                      track-by="id"
                      label="name"
                      placeholder="Seleziona un Tag"
                      tag-placholder="Aggiungi questo come nuovo Tag"
                      selectLabel="Clicca per selezionare"
                      deselectLabel="Clicca per Rimuovere"
                      selectedLabel="Selezionato"
                      :block-keys="['Tab', 'Enter']"
                      :options="tags"
                      :searchable="false"
                      :internal-search="false"
                      :multiple="true"
                      :taggable="true"
                      @tag="addTag">
              </multiselect>
                </v-col>
                </v-row>
              <button v-if="admin"  type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
          </form>
          </sweet-modal-tab>

          <sweet-modal-tab v-if="admin" title="Aggiungi Sconto" id="sconta_prodotto" icon="&lt;i class=&quot;fas fa-percent&quot;&gt;&lt;i&gt;">
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

              <br><br>

              <v-btn color="var(--ming)" :disabled="selected_discounts.length === 0" @click="add_discount_to_product(selected_discounts, modal_product, 1)" > Aggiungi Sconto al prodotto</v-btn>
              <br><br><br>
              <p>Aggiungi nuovo sconto alla lista</p>
              <br>
              <v-row>
                  <v-col cols="6">
              <v-form  @submit.prevent="add_discount_to_list">
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
              </v-col>
              <v-col cols="6">

              </v-col>
              </v-row>
          </sweet-modal-tab>
        </sweet-modal>
  </div>

</template>
<script>
    import {mapActions} from "vuex";
    import {SweetModal, SweetModalTab} from "sweet-modal-vue";
    import Multiselect from 'vue-multiselect';
    import PictureInput from "vue-picture-input";





export default {
  name: "BaseProdList",
  props: ["products", 'admin',"category"],
  inheritAttrs: false,

  components: {
      SweetModal,
      SweetModalTab,
      Multiselect,
      PictureInput,
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
          image: '',
          showSlash: false,
          toggleSnackbar: false,
          showPicture: false,

      }

  },

    computed:{

        discounts_list() {
                return this.$store.getters['restaurantData/discounts']
            },

        tags() {
                return this.$store.getters['restaurantData/tags']
            },


        },


    created() {
        this.$store.dispatch("restaurantData/getListDiscounts")
    },


    methods: {

      ...mapActions('restaurantData', ['removeProduct', 'addNewDiscount', 'addDiscountToProduct', 'updateProduct']),
      ...mapActions('userProfile', ['addProdCart']),


        add_discount_to_list: function (event) {
            let data = {
                "title": this.discount_name,
                "type": this.discount_type,
                "value": this.discount_price,
            };
            this.addNewDiscount(data);
            this.discount_price = this.discount_type = this.discount_name = '';
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
              this.$refs.modal.close();
              this.addDiscountToProduct(data).then(resp=> {
                  // si esegue solo se sto aggiungendo prodotti e li aggiunge subito a vista controllando che non siano doppioni
                  if (choice===1){
                  for (let i = 0; i < arrayLength; i++) {
                      if (prod.discounts[i]!==selected_discounts[i]) {
                          prod.discounts.push(selected_discounts[i]);
                      }
                  }
                  this.text=resp.message;
                  prod.final_price= resp.final_price;
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
                this.text=resp.message;
                this.toggleSnackbar=true ;


            })

            .catch(error => {

              alert(error.error)
            });
        },

        update_Product: function () {
            let tagsID= [];
            let arrayLength = this.modal_product.tags.length;
            // bisogna fare sto casino perchè devo mandare solo gli ID
            for (let i = 0; i < arrayLength; i++) {
                tagsID.push(this.modal_product.tags[i].id)
            }


            this.$refs.modal.close();
            const data = {
                "name": this.modal_product.name,
                "description": this.modal_product.description,
                "category": this.modal_product.category,
                "price": this.modal_product.price,
                "tags": tagsID,
            };
            const formData = new FormData();
            if(this.image){
            formData.append('image', this.image);
            }
            formData.append('data', JSON.stringify(data));
            let payload = {
                'up_prod': formData,
                'p_id': this.modal_product.id
            };
            this.updateProduct(payload)
        },


        toggleCardModal(prod) {
                  this.modal_product = prod;
                  this.showPicture = true;
                  this.selected_discounts = prod.discounts;
                  this.checkDiscounts();
                  this.$refs.modal.open('modifica_prodotto');
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

        onChanged() {
            console.log("New picture loaded");
            if (this.$refs.productImage.file) {
                this.image = this.$refs.productImage.file;
            } else {
                console.log("Old browser. No support for Filereader API");
            }
        },

        checkDiscounts() {
            let arrayLength = this.modal_product.discounts.length;
            if (arrayLength>0) {
                this.showSlash = true;
            }
            else{
                this.showSlash = false;
            }
        },

        add_to_cart_action(prod){
            this.addProdCart(prod);
        }





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

.price_text{
    width: 30%;
    text-decoration: none;
    justify-content: center;
}

.discount_true{
    width: 30%;
    text-decoration: line-through;
    justify-content: center;

}



  .save {
    padding: 10px;
    background: var(--ming);
    border-radius: 25px;
    margin: 10px auto;
    color: white;
    transition: 0.4s;
    font-weight: bold;
  }
  .save:hover {
    transform: scale(1.05);
  }

</style>
