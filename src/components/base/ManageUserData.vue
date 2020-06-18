<template>
  <div>
    <form @submit.prevent="update">
      <v-alert :value="success !== ''" type="success">{{success}}</v-alert>
      <v-alert :value="error !== ''" type="error" >{{error}}</v-alert>
      <template v-for="(campo, i) in user">
        <v-row v-if="fix.includes(i) && campo" :key="i">
          <v-col cols="3" class="dati"><b>{{i.replace(/_/g , ' ')}}:</b></v-col>
          <v-col  cols="9">{{campo}}</v-col>
        </v-row>
      </template>
      <v-row v-if="user.Nome || editing">
        <v-col cols="3" class="dati"><b>Nome:</b></v-col>
        <v-col cols="9"><p v-if="!editing" class="field" >{{user.Nome}}</p><v-text-field v-if="editing" light class="field" type="text" v-model='user.Nome'></v-text-field></v-col>
      </v-row>
      <v-row v-if="user.Cognome || editing">
        <v-col cols="3" class="dati"><b>Cognome:</b></v-col>
        <v-col cols="9"><p v-if="!editing" class="field" >{{user.Cognome}}</p><v-text-field v-if="editing" light class="field" type="text" v-model='user.Cognome'></v-text-field></v-col>
      </v-row>
      <v-row v-if="user.Anno_di_Nascita || editing">
        <v-col cols="3" class="dati"><b>Data di nascita:</b></v-col>
        <v-col cols="9"><p v-if="!editing" class="field">{{user.Anno_di_Nascita}}</p><v-text-field v-if="editing" light class="field" type="date" v-model='user.Anno_di_Nascita'></v-text-field></v-col>
      </v-row>
      <v-row>
        <v-col cols="3" class="dati"><b>Numero di Telefono:</b></v-col>
        <v-col cols="9"><p v-if="!editing" class="field" >{{user.Numero_di_Telefono}}</p><v-text-field v-if="editing" light class="field" type="text" v-model='user.Numero_di_Telefono'></v-text-field></v-col>
      </v-row>
      <template v-if="isBusiness">
        <v-row v-if="!editing">
          <v-col cols="3" class="dati"><b>Indirizzo:</b></v-col>
          <v-col cols="9"><p class="field">{{stringIndirizzo()}}</p></v-col>
        </v-row>
        <template v-else>
          <v-row>
            <v-col cols="3" class="dati"><b>Città:</b></v-col>
            <v-col cols="9"><v-text-field light class="field" type="text" v-model='user.Citta'></v-text-field></v-col>
          </v-row>
          <v-row>
            <v-col cols="3" class="dati"><b>Indirizzo:</b></v-col>
            <v-col cols="9"><v-text-field light class="field" type="text" v-model='user.Indirizzo'></v-text-field></v-col>
          </v-row>
          <v-row>
            <v-col cols="3" class="dati"><b>Numero civico:</b></v-col>
            <v-col cols="9"><v-text-field light class="field" type="text" v-model='user.N_civ'></v-text-field></v-col>
          </v-row>
          <v-row>
            <v-col cols="3" class="dati"><b>Cap:</b></v-col>
            <v-col cols="9"><v-text-field light class="field" type="number" v-model='user.Cap'></v-text-field></v-col>
          </v-row>
        </template>
      </template>

      <newPictureInput
          v-if="editing"
          ref="avatar"
          @change="onChanged"
          @remove="onRemoved"
          :removable="true"
          :prefill="avatar"
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
              remove: 'Elimina foto',
          }"
      >
        </newPictureInput>
      <button v-if="editing" type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
    </form><button class="gestrest" @click="editing=!editing"><span class="butgest">{{butText}}</span></button>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

  export default {
    name: "ManageUserData",
    data() {
      return {
        fix: [
          'Username',
          'Email',
          'Codice_Fiscale'
        ],
        success: '',
        error: '',
        editing: false,
        image: '',
        deletePhoto: false
      }
    },
    methods: {
      ...mapActions('userProfile', ['updateProfile']),
      update: function() {
        var data = {
          phone: this.user.Numero_di_Telefono,
          first_name: this.user.Nome,
          last_name: this.user.Cognome,
          birth_date: this.user.Anno_di_Nascita
        };
        if(this.isBusiness){
          data.city = this.user.Citta
          data.address = this.user.Indirizzo
          data.n_civ = this.user.N_civ
          data.cap = this.user.Cap
        }

        const formData = new FormData();
        if ( this.image !== '' || this.deletePhoto)
          formData.append('avatar', this.image);
        formData.append('data', JSON.stringify(data));

        this.updateProfile(formData)
        .then(() => {
          this.editing = false
          this.success = 'Profilo aggiornato con successo'
          this.error = ''
        })
        .catch(err => {
          this.success = ''
          this.error = err
        })
      },

      onChanged() {
        this.deletePhoto = false;
        if (this.$refs.avatar.file) {
          this.image = this.$refs.avatar.file;
        } else {
          console.log("Old browser. No support for Filereader API");
        }
      },
      onRemoved() {
          this.image = '';
          this.deletePhoto = true;
      },
      stringIndirizzo() {
        return this.user.Indirizzo + ', ' + this.user.N_civ + '; ' + this.user.Citta + '; ' + this.user.Cap
      },
    },
    computed: {
      user() {
        return this.$store.getters['userProfile/user']
      },
      isBusiness() {
        return this.$store.getters['userProfile/isBusiness']
      },
      butText() {
        return this.editing? 'Visualizza dati' : 'Modifica dati'
      },
      avatar() {
          return this.$store.getters['userProfile/user_private'].avatar
      },
    }
  }
</script>

<style scoped>
  .dati {
    background: var(--whitesmoke);
    text-align: center;
  }
  .gestrest {
    background: var(--ming);
    padding: 10px;
    border-radius: 5px;
    transition: ease-in-out 0.3s;
    margin-top: 10px;
  }

  .butgest {
    text-transform: capitalize;
    color: white;
    font-weight: bold;
  }

  .gestrest:hover {
    transform: scale(1.1);
  }
  .gestrest:hover > .wrench {
    transform: rotate(45deg);
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
  .dati {
    background: var(--whitesmoke);
    text-align: center;
  }
</style>