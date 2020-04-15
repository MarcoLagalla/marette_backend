<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"  max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn text
        class="font-weight-bold"
        min-width="96"
        v-on="on">SIGNUP</v-btn>
      </template>
      <v-card
      color="grey"
      >
        <form @submit.prevent="register">
           <div class="container">
               <h1>Registrati</h1>
               <p>Dammi dei bei dati per registrare un account.</p>
               <!--template v-if="status === 'error'" v-for="errori in errors">
                   <h3 v-for="errore in errori">{{errore}}</h3>
               </template-->
               <v-card-text>
                 <v-container>
                   <v-row>
                     <v-col cols="12" sm="6" md="4">
                       <v-text-field
                       solo filed
                       id="username"
                       v-model="username"
                       label="Username"
                       required
                       ></v-text-field>
                     </v-col>
                     <v-col cols="12" sm="6" md="4">
                       <v-text-field solo filed label="Nome*" id="first_name" required></v-text-field>
                     </v-col>
                     <v-col cols="12" sm="6" md="4">
                       <v-text-field
                       solo filed
                       label="Cognome*"
                       id="last_name"
                       required
                       ></v-text-field>
                     </v-col>
                     <v-col cols="12">
                       <v-text-field solo filed label="Email*" id="email" type="email" required></v-text-field>
                     </v-col>
                     <v-col cols="12">
                       <v-text-field solo filed label="Password*" id="password" type="password" required></v-text-field>
                     </v-col>
                     <v-col cols="12" sm="6">
                       <v-text-field
                       solo filed
                       label="Repeat password" id="password2" type="password" required></v-text-field>
                     </v-col>
                     <v-col cols="12" sm="6">
                       <v-text-field
                       solo filed
                       id="birth_date"
                       label="Birth date"
                       v-model="birth_date"
                       type="date"
                       ></v-text-field>
                     </v-col>
                     <v-col cols="12" sm="6">
                       <v-text-field
                       solo filed
                       id="phone"
                       name="phone"
                       label="Phone number"
                       v-model="phone"
                       type="tel"
                       ></v-text-field>
                     </v-col>
                   </v-row>
                 </v-container>
                 <small>*indicates required field</small>
               </v-card-text>

               <p>Registrando un account accetti i nostri <router-link to="/termini">Terms & Privacy</router-link>.</p>
               <button type="submit" class="registerbtn" >Registrati</button>
           </div>

           <div class="container signin">
               <p>Hai già un account? <a href="#">Dillo prima, coglione</a>.</p>
           </div>
       </form>
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
                  this.$router.push('/')
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
                  this.$router.push('/')
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

<style>

.registerbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}
.registerbtn:hover {
  opacity:1;
}

</style>
