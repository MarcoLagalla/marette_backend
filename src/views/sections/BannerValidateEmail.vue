<template>
  <div class="body">
  <div class="banner" v-if="!userActivated">
    <h1 v-show="!submitted">ATTIVARE EMAIL PER ACCEDERE A TUTTE LE FUNZIONALITÀ</h1>
    <h1 v-show="submitted">EMAIL INVIATA CON SUCCESSO</h1>
    <h1 v-show="error">C'è stato un imprevisto, riprova più tardi</h1>
    <p><span class="spanmail">Indirizzo email:</span> {{userEmail}}</p>
    <button class="managebutton3" :disabled="loading" @click="submitEmail"><span v-if="!loading">Invia nuova Email di verifica</span><span v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span></button>
  </div>
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
  .body {
    background: var(--whitesmoke);
  }
.banner {
  padding: 20px;
margin: 0 5vmax;

  border-radius: 25px;
}
.banner h1 {
  font-weight: lighter;
  color: var(--ming);
 }
  .loading {
    padding: 10px;
    color: var(--darkslate)!important;
    font-weight: bold!important;
    background: transparent!important;
    border: transparent!important;
    opacity: 1;
    transition: 0.5s cubic-bezier(0.1, 0.7, 1.0, 0.1);
    margin: 0 10px;
  }
  .spanmail {
    font-weight: bold;
    text-transform: capitalize;
  }
</style>