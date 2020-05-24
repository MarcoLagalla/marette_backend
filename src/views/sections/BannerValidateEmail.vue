<template>
  <div v-if="!userActivated">
    <h1 v-show="!submitted">ATTIVARE EMAIL PER ACCEDERE A TUTTE LE FUNZIONALITÀ</h1>
    <h1 v-show="submitted">EMAIL INVIATA CON SUCCESSO</h1>
    <h1 v-show="error">C'è stato un imprevisto, riprova più tardi</h1>
    <p>Indirizzo email: {{userEmail}}</p>
    <v-btn :loading="loading" @click="submitEmail">Invia nuova Email di verifica</v-btn>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

  export default {
    name: "ValidateEmail",
    data() {
      return {
        loading: false,
        submitted: false,
        error: false
      }
    },
    computed: {
      userEmail() {
        return this.$store.getters['userProfile/user'].Email
      },
      userActivated() {
        return this.$store.getters['userProfile/user_private'].email_activated
      },
    },
    methods: {
      ...mapActions('userProfile', ['resendEmailValidation']),
      submitEmail: function () {
        this.loading = true
        this.resendEmailValidation()
          .then(()=>{
            this.loading = false
            this.submitted = true
          })
        .catch(()=>{
          this.loading = false
          this.error = true
        })


      }
    }
  }
</script>

<style scoped>

</style>