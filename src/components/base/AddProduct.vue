<template>
  <div>
    <div class="addprod">
    <v-form @submit.prevent="submitProduct">
      <v-text-field v-model='name' type="text" label=" Inserire nome prodotto" id="name" name="name" required></v-text-field>
      <v-text-field v-model='description' type="text" label=" Inserire descrizione" id="description" name="description" required></v-text-field>
      <v-text-field v-model='price' type="number" label=" Inserire prezzo" id="price" name="price" required></v-text-field>
      <a class="btn" @click.prevent="toggleShow">set avatar</a>
      <template class="tags" :v-model="show" >

        <p>Seleziona i tag corrispondenti </p>
        <!--p-check class="p-icon p-round p-jelly" color="primary">
            <i slot="extra" class="icon mdi mdi-check"></i>
            Interested
        </p-check-->

      </template>
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
    PictureInput

  },

  data() {
    return {
        name: '',
        description: '',
        price: '',
        image: '',
        show: false,

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
          };
         const formData = new FormData();
          formData.append('image', this.image);
          formData.append('data', JSON.stringify(data));
          this.addProduct(formData)
        },

      toggleShow() {
        this.show = !this.show;
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
  transition: 0.5s;
  color: blueviolet
}
.addconf:hover {
  box-shadow: 0 0 10px black;
}


</style>
