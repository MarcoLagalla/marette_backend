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
        <p class="error" v-if="errors.error">{{errors.error[0]}}</p>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                :error-messages="errors.username"
                @change="errors.username=''"
                prepend-icon="mdi-account"
                solo filed
                id="username"
                v-model="username"
                label="Username*"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                :error-messages="errors.first_name"
                @change="errors.first_name=''"
                solo filed
                v-model="first_name"
                label="Nome"
                id="first_name"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                :error-messages="errors.last_name"
                @change="errors.last_name=''"
                solo filed
                v-model="last_name"
                label="Cognome"
                id="last_name"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                :error-messages="errors.phone"
                @change="errors.phone=''"
                prepend-icon="mdi-phone"
                solo filed
                id="phone"
                name="phone"
                label="Numero di telefono*"
                v-model="phone"
                type="tel"
                require
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                :error-messages="errors.birth_date"
                @change="errors.birth_date=''"
                prepend-icon="mdi-calendar-range"
                solo filed
                id="birth_date"
                label="Data di nascita"
                v-model="birth_date"
                type="date"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                :error-messages="errors.email"
                @change="errors.email=''"
                prepend-icon="mdi-email"
                solo filed
                v-model="email"
                label="Email*"
                id="email"
                type="email"
                required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
                :error-messages="errors.password"
                @change="errors.password=''"
                prepend-icon="mdi-key"
                solo filed
                v-model="password"
                label="Password*"
                id="password"
                type="password"
                required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
                :error-messages="errors.password2"
                @change="errors.password2=''"
                solo filed
                v-model="password2"
                label="Repeat password*"
                id="password2"
                type="password"
                required></v-text-field>
            </v-col>


          </v-row>
        </v-container>
        <small>*indica i campi obbligatori</small>
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


    <v-card-text>Hai già un account? <router-link to="/login">Dillo prima, coglione</router-link>.</v-card-text>


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
