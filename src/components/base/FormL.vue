<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"  max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn text

        class="font-weight-bold"
        min-width="96"
        v-on="on">LOGIN</v-btn>
      </template>
      <v-card
      color="grey"
      >

      <form @submit.prevent="login" class="container">
        <h1>Log in</h1>
        <p>Inserire dati per loggare.</p>
        <h2 v-if="status === 'error'">Hai ciccato qualcosa!</h2>



        <label for="email"><b>Email</b></label>
        <v-text-field solo filled v-model='email' type="email" placeholder="Inserire Email" id="email" name="email" required>
        </v-text-field>
        <label for="psw"><b>Password</b></label>
        <v-text-field solo filled v-model='password' type="password" placeholder="Inserire Password" id="psw" name="psw" required>
        </v-text-field>
        
        <button class="loginbtn">Collegati</button>
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
.container {
  padding: 16px;
}
/* Full-width input fields */
input[type=text], input[type=password] , input[type=tel] , input[type=date] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}
input[type=text]:focus, input[type=password], input[type=tel] , input[type=date] :focus {
  background-color: #ddd;
  outline: none;
}
/* Overwrite default styles of hr */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}
/* Set a style for the submit/register button */
.loginbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}
.loginbtn:hover {
  opacity:1;
}
/* Add a blue text color to links */
a {
  color: dodgerblue;
}
/* Set a grey background color and center the text of the "sign in" section */
.signin {
  background-color: #f1f1f1;
  text-align: center;
}
</style>
