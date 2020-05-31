<template>
  <form @submit.prevent="update">
    <template v-for="(campo, i) in user">
      <v-row v-if="fix.includes(i) && campo" :key="i">
        <v-col cols="3" class="dati"><b>{{i.replace(/_/g , ' ')}}:</b></v-col>
        <v-col  cols="9">{{campo}}</v-col>
      </v-row>
    </template>
    <v-row>
      <v-col cols="3" class="dati"><b>Numero di Telefono:</b></v-col>
      <v-col cols="9"><v-text-field light class="field" :disabled="!editing" type="tel" v-model='user.Numero_di_Telefono'></v-text-field></v-col>
    </v-row>
    <template v-if="isBusiness">
      <v-row v-if="!editing">
        <v-col cols="3" class="dati"><b>Indirizzo:</b></v-col>
        <v-col cols="9"><v-text-field light class="field" type="text" :disabled="true" v-model='stringIndirizzo'></v-text-field></v-col>
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
    <button v-if="editing" type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
  </form>
</template>

<script>
  export default {
    name: "ManageUserData",
    props: ['editing'],
    data() {
      return {
        fix: [
          'Username',
          'Email',
          'Nome',
          'Cognome',
          'Anno_di_Nascita',
          'Codice_Fiscale'
        ],


      }
    },
    computed: {
      user() {
        return this.$store.getters['userProfile/user']
      },
      isBusiness() {
        return this.$store.getters['userProfile/isBusiness']
      },
      stringIndirizzo() {
        return this.user.Indirizzo + ', ' + this.user.N_civ + '; ' + this.user.Citta + '; ' + this.user.Cap
      },
    }
  }
</script>

<style scoped>

</style>