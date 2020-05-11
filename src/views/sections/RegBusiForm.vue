<template>
<div class="body">
  <v-row align="center" class="ma-0 pa-8" justify="center">
    <v-form @submit.prevent="register" v-model="valid">
      <v-card color="rgba(255,255,255,0.9)" shaped :elevation="8" class="pa-4">
        <h1>Registra il tuo business <v-icon>mdi-account-tie</v-icon>
        </h1>
        <p class="error" v-if="errors.error" id="error">{{errors.error[0]}}</p>
        <hr>
        <v-col>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Username" :rules="required" :error-messages="errors.username" @change="errors.username=''" v-model='username' type="text" id="username" name="username" required></v-text-field>
            <v-text-field label="Email" :rules="emailRules" :error-messages="errors.email" @change="errors.email=''" v-model='email' type="email" id="email" name="email" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Nome" :rules="required" :error-messages="errors.first_name" @change="errors.first_name=''" v-model='first_name' type="text" id="first_name" name="first_name" required></v-text-field>
            <v-text-field label="Cognome" :rules="required" :error-messages="errors.last_name" @change="errors.last_name=''" v-model='last_name' type="text" id="last_name" name="last_name" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Città di residenza" :rules="required" :error-messages="errors.city" @change="errors.city=''" v-model='city' type="text" id="city" name="city" required></v-text-field>
            <v-text-field label="CAP" :rules="required" :error-messages="errors.cap" @change="errors.cap=''" v-model='cap' type="number" id="cap" name="cap" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Indirizzo" :rules="required" :error-messages="errors.address" @change="errors.address=''" v-model='address' type="text" id="address" name="address" required></v-text-field>
            <v-text-field label="Numero civico" :rules="required" :error-messages="errors.n_civ" @change="errors.n_civ=''" v-model='n_civ' type="number" id="n_civ" name="n_civ" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Codice fiscale" :rules="required" :error-messages="errors.cf" @change="errors.cf=''" v-model='cf' type="text" id="cf" name="cf" required></v-text-field>
            <v-text-field label="Data di nascita" :rules="required" :error-messages="errors.birth_date" @change="errors.birth_date=''" v-model='birth_date' type="date" id="birth_date" name="birth_date" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Numero telefonico" :rules="required" :error-messages="errors.phone" @change="errors.phone=''" v-model='phone' type="tel" id="phone" name="phone" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <v-text-field label="Password" :rules="required" :error-messages="errors.password" @change="errors.password=''" v-model='password' type="password" id="psw" name="psw" required></v-text-field>
            <v-text-field label="Ripetere la password" :rules="password2Rules" :error-messages="errors.password2" @change="errors.password2=''" v-model='password2' type="password" id="psw-repeat" name="psw-repeat" required></v-text-field>
          </v-row>
          <v-row align="center" class="ma-0" justify="center">
            <picture-input
              ref="avatar"
              @change="onChanged"
              :width="300"
              :height="300"
              size="5"
              :crop="true"
              :changeOnClick="false"
              accept="image/jpeg, image/png, image/gif"
              buttonClass="ui button primary"
              :customStrings="{
              upload: '<h1>Carica immagine</h1>',
              drag: 'Trascina qui la un immagine di profilo o clicca per selezionarla'}">
            </picture-input>
          </v-row>
        </v-col>
        <hr>
        <v-card-text>Registrando un account accetti i nostri <router-link to="/termini">Terms & Privacy</router-link>.</v-card-text>
        <div class="regbtn2">
          <div class="center">
            <button class="btn" type="submit" :disabled="!valid">
              <svg width="180px" height="60px" viewBox="0 0 180 60" class="border">
                <polyline points="179,1 179,59 1,59 1,1 179,1" class="bg-line" />
                <polyline points="179,1 179,59 1,59 1,1 179,1" class="hl-line" />
              </svg>
              <span>Submit</span>
            </button>
          </div>
        </div>
      </v-card>
    </v-form>
  </v-row>
</div>
</template>
<script>
import {
  mapActions
} from 'vuex'
import PictureInput from "vue-picture-input";

export default {
  name: "Registration",
  components: {
    PictureInput,
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      first_name: '',
      last_name: '',
      birth_date: '',
      phone: '',
      cap: '',
      address: '',
      n_civ: '',
      city: '',
      cf: '',
      image: '',
      valid: true,
      required: [
        v => !!v || 'Campo obbligatorio',
      ],
      emailRules: [
        v => !!v || 'Campo obbligatorio',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      password2Rules: [
        v => !!v || 'Campo obbligatorio',
        v => v === this.password || "Le password devono combaciare"
      ]
    }
  },
  methods: {
    ...mapActions('userAuthentication', ['registerBusiness']),
    register: function() {
      const data = {
        username: this.username,
        email: this.email,
        password: this.password,
        password2: this.password2,
        phone: this.phone,
        first_name: this.first_name,
        last_name: this.last_name,
        n_civ: this.n_civ,
        birth_date: this.birth_date,
        cap: this.cap,
        address: this.address,
        city: this.city,
        cf: this.cf
      };

      const formData = new FormData();
      formData.append('avatar', this.image);
      formData.append('data', JSON.stringify(data));

      this.registerBusiness(formData).then(() => {
        this.$router.push('/profile')
      }).catch(error => {
        var id = Object.keys(error)[0];
        document.getElementById(id).scrollIntoView(false)
        document.getElementById(id).focus({
          preventScroll: true
        });
      })
    },
    onChanged() {
      if (this.$refs.avatar.file) {
        this.image = this.$refs.avatar.file;
      } else {
        console.log("Old browser. No support for Filereader API");
      }
    },
  },
  computed: {
    status() {
      return this.$store.getters['userAuthentication/status']
    },
    errors() {
      return this.$store.getters['userAuthentication/errors']
    }
  }
}
</script>
<style scoped>
.v-text-field {
  padding: 10px;
}
.body {
  margin: 0 !important;
  background: url("https://www.juorno.it/wp-content/uploads/2019/08/IthaaUnderseaRestaurant.jpg") no-repeat center center fixed;
  background-size: 1920px 1080px;
}
.v-card {
  text-align: center;
}
.v-card-text {
  margin: 5%;
}
h1 {
  color: red;
  font-size: 2em;
  text-align: center;
}
h2 {
  color: #1e7e34;
}
h3 {
  color: red;
}
/* Overwrite default styles of hr */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}
/* Set a style for the submit/register button */
.regbtn2 {
  padding: 10px;
  margin: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.center {
  width: 180px;
  height: 60px;
  position: absolute;
}
.btn {
  width: 180px;
  height: 60px;
  cursor: pointer;
  background: transparent;
  border: 1px solid #91C9FF;
  outline: none;
  transition: 1s ease-in-out;
}
svg {
  position: absolute;
  left: 0;
  top: 0;
  fill: none;
  stroke: #fff;
  stroke-dasharray: 150 480;
  stroke-dashoffset: 150;
  transition: 1s ease-in-out;
}
.btn:hover {
  transition: 1s ease-in-out;
  background: dodgerblue;
  color: white;
}
.btn:hover svg {
  stroke-dashoffset: -480;
}
.btn span {
  color: grey;
  font-size: 18px;
  font-weight: 600;
}
.btn:hover span {
  color: white;
  transition: 1s ease-in-out;
}
/* Add a blue text color to links */
a {
  color: dodgerblue;
}
.btn:disabled {
  background: red;
  cursor: not-allowed;
}
</style>
