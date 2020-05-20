<template>
  <div>
    <h2 :style="'color:'+ color + ';'">{{response}}</h2>
    <router-link to="/profile"><v-btn>Se non vieni reindirizzato dopo 5 secondi clicca qui</v-btn></router-link>
  </div>
</template>
<script>
  import {mapActions} from "vuex";

  export default {
    name: "ValidateEmail",
    data() {
      return {
        restID: this.$route.params.id,
        token: this.$route.params.token,
        success: false
      }
    },
    created() {
      this.validateEmail({
        id: this.$route.params.id,
        token: this.$route.params.token
      })
      .then(() => {
        this.success = true
      }

      )
      .catch(() => {
        this.success = false
      }

      )

      window.setTimeout(function(){

        window.location.href = "/profile";

    }, 5000);
    },
    methods: {
      ...mapActions('userProfile', ['validateEmail']),
    },
    computed: {
      response() {
        return this.success? 'Account attivato con successo' : 'Errore, ritenta'
      },
      color() {
        return this.success? 'green' : 'red'
      },
    }
  }
</script>

<style scoped>

</style>