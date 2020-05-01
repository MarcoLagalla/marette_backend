<template>
  <div>
    <v-form @submit.prevent="submitProduct">
      <v-text-field solo background-color="#486F83" v-model='name' type="text" placeholder=" Inserire nome prodotto" id="name" name="name" required></v-text-field>
      <v-text-field solo background-color="#486F83" v-model='description' type="text" placeholder=" Inserire descrizione" id="description" name="description" required></v-text-field>
      <v-text-field solo background-color="#486F83" v-model='price' type="number" placeholder=" Inserire prezzo" id="price" name="price" required></v-text-field>
      <picture-input
        ref="productImage"
        @change="onChanged"
        :width="300"
        :height="300"
        :crop="true"
        :changeOnClick="false"
        accept="image/jpeg, image/png, image/gif"
        buttonClass="ui button primary"
        :customStrings="{
        upload: '<h1>Carica immagine</h1>',
        drag: 'Trascina qui la tua immagine o clicca per selezionarla'}">
      </picture-input>
      <button type="submit">Aggiungi Prodotto</button>
    </v-form>
  </div>
</template>
<script>
  import PictureInput from 'vue-picture-input'
  import {mapActions} from "vuex";
export default {
  name: "AddProduct",
  props: ['category'],

  components: {
    PictureInput
  },

  data() {
    return {
        name: '',
        description: '',
        price: '',
        image: ''
    }
  },
  computed: {
    food_category_choice() {
      return this.$store.getters['manageRestaurant/food_category_choice']
    }
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
      }

  }
}
</script>
<style scoped>
</style>