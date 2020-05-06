<template>
  <div>
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
              <v-btn @click="toggleShowTags">Inserisci i tag</v-btn>
        <br>
          <v-card
            v-show="showTags"
            class="mx-auto"
            max-width="500"
          >
            <v-list shaped>
              <v-list-item-group
                v-model="selectedTags"
                multiple
              >
                <template v-for="(item, i) in tags">
                  <v-divider
                    v-if="!item"
                    :key="`divider-${i}`"
                  ></v-divider>

                  <v-list-item
                    v-else
                    :key="`item-${i}`"
                    :value="item.id"
                    active-class="blue--text text--accent-4"
                  >
                    <template v-slot:default="{ active, toggle }">
                      <v-list-item-content>
                        <v-list-item-title v-text="item.name" ></v-list-item-title>
                      </v-list-item-content>

                      <v-list-item-action>
                        <v-checkbox
                          :input-value="active"
                          :true-value="item"
                          color="blue accent-4"
                          @click="toggle"
                        ></v-checkbox>
                      </v-list-item-action>
                    </template>
                  </v-list-item>
                </template>
              </v-list-item-group>
            </v-list>
            </v-card>

        <br><br>
      <v-btn @click="toggleShowDiscounts">Inserisci uno sconto al prodotto</v-btn>
        <br>
          <v-card
            v-show="showDiscounts"
            class="mx-auto"
            max-width="500"
          >
            <v-list shaped>
              <v-list-item-group
                v-model="selectedDiscounts"
                multiple
              >
                <template v-for="(item, i) in discounts">
                  <v-divider
                    v-if="!item"
                    :key="`divider-${i}`"
                  ></v-divider>

                  <v-list-item
                    v-else
                    :key="`item-${i}`"
                    :value="item.id"
                    active-class="blue--text text--accent-4"
                  >
                    <template v-slot:default="{ active, toggle }">
                      <v-list-item-content>
                        <v-list-item-title v-text="item.name" ></v-list-item-title>
                      </v-list-item-content>

                      <v-list-item-action>
                        <v-checkbox
                          :input-value="active"
                          :true-value="item"
                          color="blue accent-4"
                          @click="toggle"
                        ></v-checkbox>
                      </v-list-item-action>
                    </template>
                  </v-list-item>
                </template>
              </v-list-item-group>
            </v-list>
            </v-card>

        <br><br>

      <picture-input
        ref="productImage"
        @change="onChanged"
        :width="300"
        :height="300"
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


     <button type="submit" class="addconf">Aggiungi Prodotto</button>

    </v-form>
                    <!--vue-anka-cropper></vue-anka-cropper-->

    </div>


  </div>
</template>
<script>
  import {mapActions} from "vuex";
  //import vueAnkaCropper from 'vue-anka-cropper';
  import PictureInput from "vue-picture-input";

// DATA URI TO FILE FORSE PUò essere usato per passare da URI a file object


export default {
  name: "AddProduct",
  props: ['category'],

  components: {
    // vueAnkaCropper,
    PictureInput,


  },

  data() {
    return {
        name: '',
        description: '',
        price: '',
        image: '',
        showTags: false,
        showDiscounts: false,
        selectedTags: [],
        selectedDiscounts: [],

    }
  },
  computed: {
    food_category_choice() {
      return this.$store.getters['manageRestaurant/food_category_choice']
    },
    discounts() {
      return this.$store.getters['manageRestaurant/discounts']
    },

    tags() {
      return this.$store.getters['restaurantData/tags']
    },
  },


    created() {
      this.$store.dispatch("restaurantData/getListTag")
      this.$store.dispatch("restaurantData/getListDiscounts")
    },



  methods: {
      ...mapActions('restaurantData', ['addProduct']),
      ...mapActions('restaurantData',['listTag']),
      onChanged() {
        console.log("New picture loaded");
        if (this.$refs.productImage.file) {
          this.image = this.$refs.productImage.file;
        } else {
          console.log("Old browser. No support for Filereader API");
        }
      },
      submitProduct: function() {
          const data = {
              "name": this.name,
              "description": this.description,
              "category": this.category,
              "price": this.price,
              "tags": this.selectedTags

          };
         const formData = new FormData();
          formData.append('image', this.image);
          formData.append('data', JSON.stringify(data));
          this.addProduct(formData)
        },

      toggleShowTags() {
        this.showTags = !this.showTags;
      },

    toggleShowDiscounts() {
        this.showDiscounts = !this.showDiscounts;
      },


  },


}
</script>
<style scoped>
.addprod {
  margin: auto;
  width: 50%;
  padding: 20px;
}
.addconf {
  padding: 10px;
  border-radius: 25px;
  border: inset 2px red;
  background: rgba(255, 0, 0, 0.5);
  transition: ease 0.4s  ;
  color:forestgreen;
}
.addconf:hover {
  box-shadow: 0 0 10px black;
}
</style>
