<template>
<div class="restdatabox">
  <div class="restdatafields">
    <form @submit.prevent="update">
      <v-row>
      <v-col cols="12" md="4">
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.activity_name}}</span>
        <v-text-field light class="field"  outlined label="Nome attività" v-if="editing" v-model='restData.activity_name'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.activity_description}}</span>
        <v-text-field light class="field"  outlined label="Descrizione" v-if="editing" v-model='restData.activity_description'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.address}}</span>
        <v-text-field light class="field"  outlined label="Indirizzo" v-if="editing" v-model='restData.address'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.n_civ}}</span>
        <v-text-field light class="field"  outlined label="Numero civico" v-if="editing" v-model='restData.n_civ'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.cap}}</span>
        <v-text-field light class="field"  outlined label="cap" v-if="editing" v-model='restData.cap'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.restaurant_number}}</span>
        <v-text-field light class="field"  outlined label="Numero di telefono" v-if="editing" v-model='restData.restaurant_number'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.p_iva}}</span>
        <v-text-field light class="field"  outlined label="Partita IVA" v-if="editing" v-model='restData.p_iva'></v-text-field>
        </v-row>
        <v-row>
        <span class="datatit" v-if="!editing" >{{restData.city}}</span>
        <v-text-field light class="field"  outlined label="Città" v-if="editing" v-model='restData.city'></v-text-field>
        </v-row>
      </v-col>
      <v-col cols="12" md="4">
      <picture-input ref="restImage" @change="onChanged" :width="200" :height="200" size="3" :zIndex="0" :crop="true" :changeOnClick="false" accept="image/jpeg, image/png, image/gif" buttonClass="ui button primary" :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine del ristorante o clicca per selezionarla'}">
      </picture-input>
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
  import PictureInput from "vue-picture-input";

  export default {

    name: 'BaseManageRestData',
    props: ['id'],
    components: {
      PictureInput,
    },
    data() {
      return {
        image: '',
        editing:true
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
.datatit {
 padding: 10px;
  text-transform: capitalize;
}
.field {
  color: #1a1a1a!important;
  z-index: 100;
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
</style>
