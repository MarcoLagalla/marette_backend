<template>
<div class="restdatabox">
  <div class="restdatafields">
    <form @submit.prevent="update">
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field outlined placeholder="Nome del locale" v-text="restData.activity_name"></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Descrizione del locale'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.activity_description"></v-card-subtitle>
      </v-col>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Città'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.city"></v-card-subtitle>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Indirizzo'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.address"></v-card-subtitle>
      </v-col>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Numero civico'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.n_civ"></v-card-subtitle>
      </v-col>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Cap'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.cap"></v-card-subtitle>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Numero di telefono'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.restaurant_number"></v-card-subtitle>
      </v-col>
      <v-col cols="12" md="4">
        <p class="title" v-text="'Partita IVA'"></p>
        <v-card-subtitle class="pb-0" v-text="restData.p_iva"></v-card-subtitle>
      </v-col>
      <v-col cols="12" md="4">
        <picture-input ref="restImage" @change="onChanged" :width="200" :height="200" size="3" :zIndex="0" :crop="true" :changeOnClick="false" accept="image/jpeg, image/png, image/gif" buttonClass="ui button primary" :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine del ristorante o clicca per selezionarla'}">
        </picture-input>
      </v-col>
    </v-row>
    <button type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
    </form>
  </div>
</div>
</template>

<script>
  import {
    mapActions
  } from "vuex";
  import PictureInput from "vue-picture-input";

  export default {

    name: 'BaseManageRestData',
    props: ['id'],
    components: {
      PictureInput,
    },
    data() {
      return {
        image: ''
      }
    },
    created() {
      this.$store.dispatch("restaurantData/getRestaurantData", this.id)
    },
    computed: {
      restData() {
        return this.$store.getters["restaurantData/restData"];
      }
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
        };

        if (!this.image) {
          this.image = this.$refs.restImageOld.file
        }

        const formData = new FormData();
        formData.append('image', this.image);
        formData.append('data', JSON.stringify(data));

        this.updateRestaurant(formData) //TODO: far apparire un banner dati modificati con successo, gestire errori, aggiornare immagine quando cambia e far tornare le cose chiuse dopo aver salvato
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
</style>
