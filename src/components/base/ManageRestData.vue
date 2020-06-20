<template>
<div class="restdatabox">
  <v-snackbar top v-model="snackbar" :timeout="timeout" :color="color" >{{text}}</v-snackbar>
  <div class="restdatafields">
    <form @submit.prevent="update">
      <v-row>
      <v-col cols="12" md="6">
        <v-row>
        <v-text-field light class="field"  outlined label="Nome attività" :disabled="!editing"  v-model='restData.activity_name'></v-text-field>
        </v-row>
        <v-row>
        <v-text-field light class="field"  outlined label="Descrizione" :disabled="!editing"  v-model='restData.activity_description'></v-text-field>
        </v-row>
        <v-row>
        <v-text-field light class="field"  outlined label="Indirizzo" :disabled="!editing"  v-model='restData.address'></v-text-field>
        </v-row>
        <v-row>
        <v-text-field light class="field"  outlined label="Numero civico" :disabled="!editing"  v-model='restData.n_civ'></v-text-field>
        </v-row>
        <v-row>
        <v-combobox
             light class="field"
             outlined
             :disabled="!editing"
            :items="restCategories"
            item-text="category_name"
            item-value="id"
            v-model='restData.restaurant_category'
            id="restaurant_category"
            name="restaurant_category"
            multiple chips
            label="Categorie del locale*"

        ></v-combobox>
        </v-row>


      </v-col>
      <v-col cols="12" md="6">
        <div class="piccnt">
      <newPictureInput
          v-if="editing"
          ref="restImage"
          :prefill="restData.image"
          @change="onChanged"
          :width="200"
          :height="200"
          size="3"
          :zIndex="0"
          :crop="true"
          :changeOnClick="true"
          accept="image/jpeg, image/png, image/gif"
          buttonClass="ui button primary"
          :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine di profilo o clicca per selezionarla',
            change: 'Cambia foto',
          }">
      </newPictureInput>
          <v-img v-else size="3" :src="restData.image"></v-img>
        </div>
      </v-col>
      </v-row>
      <v-row>
      <v-col cols="12" md="6">
        <v-row>
          <v-text-field light class="field"  outlined label="Partita IVA" :disabled="!editing"  v-model='restData.p_iva'></v-text-field>
        </v-row>
        <v-row>
          <v-text-field light class="field"  outlined label="Città" :disabled="!editing"  v-model='restData.city'></v-text-field>
        </v-row>
      </v-col>
        <v-col cols="12" md="6">
        <v-row>
          <v-text-field light class="field"  outlined label="cap" :disabled="!editing"  v-model='restData.cap'></v-text-field>
        </v-row>
        <v-row>
          <v-text-field light class="field"  outlined label="Numero di telefono" :disabled="!editing" v-model='restData.restaurant_number'></v-text-field>
        </v-row>
        </v-col>
      </v-row>
    <button v-if="editing" type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
    </form>

  </div>
</div>
</template>

<script>
  import {
    mapActions
  } from "vuex";


  export default {

    name: 'BaseManageRestData',
    props: ['id','editing'],

    data() {
      return {
        image: '',
        restaurant_category: [],
        snackbar: false,
        timeout: 4000,
        color: 'green',
        text: 'Dati ristorante aggiornati con successo'
      }
    },
    created() {
      this.$store.dispatch("restaurantData/getRestaurantData", this.id)
    },
    computed: {
      restData() {
        return this.$store.getters["restaurantData/restData"];
      },
      restCategories() {
        return this.$store.getters["restaurantData/restCategories"];
      },
    },
    methods: {
      ...mapActions('restaurants', ['updateRestaurant']),
      update: function() {
        const data = {
          activity_name: this.restData.activity_name,
          activity_description: this.restData.activity_description,
          city: this.restData.city,
          address: this.restData.address,
          n_civ: this.restData.n_civ,
          cap: this.restData.cap,
          restaurant_number: this.restData.restaurant_number,
          p_iva: this.restData.p_iva,
          restaurant_category : []
        };

        this.restData.restaurant_category.forEach((category)=>{
            data.restaurant_category.push(category.id)
        })

        const formData = new FormData();

        if (this.image) {
          formData.append('image', this.image);
        }
        formData.append('data', JSON.stringify(data));

        this.updateRestaurant(formData)
          .then(()=>{
            this.snackbar = true;
            this.text = 'Dati ristorante aggiornati con successo';
            this.color = 'green';
            this.$emit('edited')
          })
          .catch(error => {
              var id = Object.keys(error)[0];
              console.log(id)
              this.text = 'Errore: ' + id + ': ' + error[id];
              this.color = 'error';
              this.snackbar = true;

          })


      },
      onChanged() {
        if (this.$refs.restImage.file) {
          this.image = this.$refs.restImage.file;
        } else {
          console.log("Old browser. No support for Filereader API");
        }
      },
    },
  };

</script>

<style lang="css" scoped>
.title {
  font-weight: lighter;
}
.datatit {
 padding: 10px;
  text-transform: capitalize;
  letter-spacing: 2px;
  transition: 0.5s ;
}
.field {
  color: #1a1a1a!important;
  margin: 0 10px;

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
    transform: scale(1.1);
  }
  .picture-input {
    box-shadow: 0 0 2px black;

  }
  .piccnt {
    width: 200px;
    height: 200px!important;
    margin: auto;
  }
  .restdatafields {
    border: 1px solid lightgray;
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
  }
</style>
