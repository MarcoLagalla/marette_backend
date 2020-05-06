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
        drag: 'Trascina qui la tua immagine o clicca per selezionarla'}"
        ></picture-input>
        <button type="submit" class="addconf">Aggiungi Prodotto</button>
      </v-form>
    </div>
  </div>
</template>
<script>
import PictureInput from "vue-picture-input";
import { mapActions } from "vuex";
export default {
  name: "AddProduct",
  props: ["category"],

  components: {
    PictureInput
  },

  data() {
    return {
      name: "",
      description: "",
      price: "",
      image: ""
    };
  },
  computed: {
    food_category_choice() {
      return this.$store.getters["manageRestaurant/food_category_choice"];
    }
  },
  methods: {
    ...mapActions("restaurantData", ["addProduct"]),
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
        name: this.name,
        description: this.description,
        category: this.category,
        price: this.price
      };
      const formData = new FormData();
      formData.append("image", this.image);
      formData.append("data", JSON.stringify(data));
      this.addProduct(formData);
    }
  }
};
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
