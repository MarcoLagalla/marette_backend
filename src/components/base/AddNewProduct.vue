<template>
    <div>

        <div class="product" @click="toggleCardModal">

            <i class="fas fa-plus fa-5x"></i>

        </div>

    <sweet-modal ref="modal_add">
        <div class="addprod">
            <v-form @submit.prevent="submitProduct">
                <v-text-field outlined
                              v-model="name"
                              type="text"
                              label=" Inserire nome prodotto"
                              id="name"
                              name="name"
                              required
                ></v-text-field>
                <v-text-field outlined
                              v-model="description"
                              type="text"
                              label=" Inserire descrizione"
                              id="description"
                              name="description"
                              required
                ></v-text-field>
                <v-text-field outlined
                              v-model="price"
                              type="number"
                              label=" Inserire prezzo"
                              id="price"
                              name="price"
                              required
                ></v-text-field>


                <multiselect
                      v-model="selectedTags"
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
              <br><br>
                {{selectedTags}}
                <picture-input
                        v-if="showPicture"
                        ref="productImage"
                        @change="onChanged"
                        :width="300"
                        :height="300"
                        :zIndex="0"
                        size="5"
                        :crop="true"
                        :changeOnClick="false"
                        accept="image/jpeg, image/png, image/gif"
                        buttonClass="ui button primary"
                        :customStrings="{
        upload: '<h1>Carica immagine</h1>',
        drag: 'Trascina qui la tua immagine o clicca per selezionarla'}">
                </picture-input>
                <br><br>
                <button type="submit" class="managebutton">Aggiungi Prodotto</button>
            </v-form>
            <br><br>

        </div>
    </sweet-modal>
    <!--v-snackbar
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
    </v-snackbar-->
    </div>
</template>
<script>
    import {mapActions} from "vuex";
    import PictureInput from "vue-picture-input";
    import {SweetModal} from "sweet-modal-vue";
    import Multiselect from 'vue-multiselect'

    export default {
        name: "AddNewProduct",
        props: ['category'],

        components: {
            PictureInput,
            SweetModal,
            Multiselect,


        },

        data() {
            return {
                name: '',
                description: '',
                price: '',
                image: '',
                showTags: false,
                showPicture: false,
                selectedTags: [],

            }
        },
        computed: {
            food_category_choice() {
                return this.$store.getters['manageRestaurant/food_category_choice']
            },

            tags() {
                return this.$store.getters['restaurantData/tags']
            },
        },


        created() {
            this.$store.dispatch("restaurantData/getListTag")
        },


        methods: {
            ...mapActions('restaurantData', ['addProduct']),

            onChanged() {
                console.log("New picture loaded");
                if (this.$refs.productImage.file) {
                    this.image = this.$refs.productImage.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },

            submitProduct: function () {
                let tagsID= [];
                let arrayLength = this.selectedTags.length;
                for (let i = 0; i < arrayLength; i++) {
                    tagsID.push(this.selectedTags[i].id)
                }


                this.$refs.modal_add.close()
                const data = {
                    "name": this.name,
                    "description": this.description,
                    "category": this.category,
                    "price": this.price,
                    "tags": tagsID,

                };
                const formData = new FormData();
                formData.append('image', this.image);
                formData.append('data', JSON.stringify(data));
                this.addProduct(formData)
            },


            toggleShowTags() {
                this.showTags = !this.showTags;
                console.log(this.tags)
            },

            toggleCardModal() {
                this.showPicture = true;
                this.$refs.modal_add.open()
            },

            addTag (newTag) {
                const tag = {
                name: newTag,
                code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
                }
                this.value.push(tag)
            },



        },


    }
</script>
<style scoped>
    i {
        color: grey !important;
        text-shadow: 0 0 1px grey;
        transition: 0.4s ease-in-out;
    }
    .addprod {
        margin: auto;
        width: 50%;
        padding: 20px;
    }
    picture-input {
        z-index: 0!important;
    }
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

    .delete_button {
        z-index: 2;
        top:15px;
        left:335px;
    }



    .product {
        transition: ease-in-out 0.4s;
        margin: 26px -5px;
        background: var(--ghostwhite);
        padding: 15px;
        position: relative;
        z-index: 1;
        height: 110px;
        text-align: center;
    }

    .product:hover {
        box-shadow: 0 2px 10px darkgrey;
        cursor: pointer;
    }
    .product:hover > i {
        transform: scale(1.1);
    }

    .pos2 {
        position: absolute;
        bottom: 0;

        width: 50%;
        left: 50%;
    }
</style>
