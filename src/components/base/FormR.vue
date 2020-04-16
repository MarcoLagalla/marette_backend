<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"
    overlay-opacity="0.8"
    max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn text
      class="font-weight-bold"
      min-width="96"
      v-on="on">SIGNUP</v-btn>
    </template>
    <v-card

    class="pa-auto"
    >
    <v-form @submit.prevent="register">
      <div class="cardtitle">
        <h1
        >REGISTRATI</h1></div>
        <v-divider></v-divider>
        <v-card-subtitle>Dammi dei bei dati per registrare un account.</v-card-subtitle>
        <!--template v-if="status === 'error'" v-for="errori in errors">
        <h3 v-for="errore in errori">{{errore}}</h3>
      </template-->

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
              prepend-icon="mdi-account"
              solo filed
              id="username"
              v-model="username"
              label="Username"
              required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
              solo filed
              v-model="first_name"
              label="Nome*" id="first_name" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
              solo filed
              v-model="last_name"
              label="Cognome*"
              id="last_name"
              required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
              prepend-icon="mdi-phone"
              solo filed
              id="phone"
              name="phone"
              label="Phone number"
              v-model="phone"
              type="tel"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
              prepend-icon="mdi-calendar-range"
              solo filed
              id="birth_date"
              label="Birth date"
              v-model="birth_date"
              type="date"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
              prepend-icon="mdi-email"
              solo filed
              v-model="email"
              label="Email*" id="email" type="email" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
              prepend-icon="mdi-key"
              solo filed
              v-model="password"
              label="Password*" id="password" type="password" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
              solo filed
              v-model="password2"
              label="Repeat password" id="password2" type="password" required></v-text-field>
            </v-col>


          </v-row>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
        <v-divider></v-divider>

      <v-card-text>Registrando un account accetti i nostri <router-link to="/termini">Terms & Privacy</router-link>.</v-card-text>
      <v-hover
      v-slot:default="{ hover }"

      >
      <div class="regbtn">


        <v-btn id="register"
        :class="`elevation-${hover ? 24 : 6}`"
        class="ma-auto pa-6 transition-swing "
        type="submit"  >Registrati</v-btn>
      </div>
    </v-hover>


    <v-card-text>Hai già un account? <a href="#">Dillo prima, coglione</a>.</v-card-text>


  </v-form>
</v-card>
</v-dialog>
</v-row>
</template>

<script>
// Mixins
import Heading from '@/mixins/heading'
import { mapActions } from 'vuex'

export default {
  name: 'BaseForm',

  mixins: [Heading],

  data: () => ({
    dialog: false,
    username:'',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    birth_date: '',
    phone: ''
  }),
  methods:
  {
    ...mapActions('userAuthentication', ['registerUser']),
    register: function () {
      if ( !this.first_name && !this.last_name) {
        this.registerUser({
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
          phone: this.phone
        }).then(() => {
          this.$router.push('/profile')
        })
      }
      else{
        this.registerUser({
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
          phone: this.phone,
          first_name: this.first_name,
          last_name: this.last_name,
          birth_date: this.birth_date
        }).then(() => {
          this.$router.push('/profile')
        })
      }
    }
  },
  computed:
  {
    status(){
      return this.$store.getters['userAuthentication/status']
    },
    errors(){
      return this.$store.getters['userAuthentication/errors']
    }
  }
}
</script>

<style scoped>
#register {
  background-image: linear-gradient(to right, red , orange);
  color: white;
  padding: 16px 20px;
  border: none;
  width: 50%;
  border-radius: 8px;
  cursor: pointer;
  opacity: 0.9;
  text-align: center;
}

h1 {
  text-align: center;
}

.cardtitle {
  display: flex;
  align-items: center;
  justify-content: center;
}

.regbtn{
  display: flex;
  align-items: center;
  justify-content: center;
}

.v-card {
  background: rgba(200, 200, 200, 0.9);
}

</style>
