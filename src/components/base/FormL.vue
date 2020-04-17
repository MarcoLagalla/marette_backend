<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"  max-width="500px">
      <template v-slot:activator="{ on }">
        <v-btn text
        class="font-weight-bold"
        min-width="96"
        v-on="on">LOGIN</v-btn>
      </template>
      <v-card

      >
      <v-form @submit.prevent="login" class="container">
        <h1>MEMBER LOGIN</h1>
        <p class="error" v-if="errors.error" id="error">{{errors.error[0]}}</p>
        <v-divider></v-divider>
        <div class="regbtn">
          <v-text-field prepend-inner-icon="mdi-account"
          solo v-model='email' :error-messages="errors.email" @change="errors.email=''" type="email" placeholder="Inserire Email" id="email" name="email" required>
        </v-text-field>
      </div>
      <div class="regbtn">
        <v-text-field prepend-inner-icon="mdi-key"
        solo v-model='password' :error-messages="errors.password" @change="errors.password=''" type="password" placeholder="Inserire Password" id="psw" name="psw" required>
      </v-text-field>
    </div>
    <v-divider></v-divider>


<div class="regbtn2">
    <div class="center">
        <button class="btn" type="submit">
          <svg width="180px" height="60px" viewBox="0 0 180 60" class="border">
            <polyline points="179,1 179,59 1,59 1,1 179,1" class="bg-line" />
            <polyline points="179,1 179,59 1,59 1,1 179,1" class="hl-line" />
          </svg>
          <span>Login</span>
        </button>
      </div>
  </div>

  <v-card-text><a style="color:white" href="#">Hai dimenticato la password? </a></v-card-text>
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
    email:'',
    password:''

  }),
  methods:
  {
    ...mapActions('userAuthentication', ['signIn']),
    login: function () {
      this.signIn({
        email: this.email,
        password: this.password,
      }).then(() => {
        this.$router.push('/')
      });
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
{box-sizing: border-box}
/* Add padding to containers */
h1 {
  text-align: center;
  margin-bottom: 5%;
  color: white;
}
.v-text-field {
  max-width: 60%;
  border-radius: 25px;
  background-color: inherit;
}
a:link {
  color: red;
}
#login {
  width: 60%;
  cursor: pointer;
  opacity: 0.9;
  text-align: center;
}
.regbtn2{
    padding: 10px;
    margin: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.regbtn{
  display: flex;
  align-items: center;
  justify-content: center;
}
.v-card-text {
  text-align: center;
}
.v-dialog {
  border-radius: 10px;
}
.v-card {
  background: rgba(100, 100, 100, 0.9);
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
  border: 1px solid white;
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
  background: #b20000;
}

.btn:hover svg {
  stroke-dashoffset: -480;
}

.btn span {
  color: white;
  font-size: 18px;
  font-weight: 600;
}
</style>
