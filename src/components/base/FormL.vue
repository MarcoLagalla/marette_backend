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

      <form @submit.prevent="login" class="container">
        <h1>MEMBER LOGIN</h1>
        <h2 v-if="status === 'error'">Hai ciccato qualcosa!</h2>
        <v-divider></v-divider>


        <div class="regbtn">
          <v-text-field prepend-inner-icon="mdi-account"
          solo v-model='email' type="email" placeholder="Inserire Email" id="email" name="email" required>
        </v-text-field>
      </div>
      <div class="regbtn">
        <v-text-field prepend-inner-icon="mdi-key"
        solo v-model='password' type="password" placeholder="Inserire Password" id="psw" name="psw" required>
      </v-text-field>
    </div>
    <v-divider></v-divider>
    <v-hover
    v-slot:default="{ hover }"

    >
    <div class="regbtn">


      <v-btn id="login"
      :class="`elevation-${hover ? 12 : 4}`"
      class="ma-auto pa-6 transition-swing "
      >LOGIN</v-btn>
    </div>
  </v-hover>
  <v-card-text><a href="#">Hai dimenticato la password? </a></v-card-text>
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
h1 {
  font-family: Work Sans;
  text-align: center;
  margin-bottom: auto;
}
.v-text-field {
  max-width: 60%;
  border-radius: 25px;
  background-color: inherit;
}

/* Overwrite default styles of hr */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}
#login {
  background-image: linear-gradient(to right, red , blue);
  color: white;
  padding: 16px 20px;
  border: none;
  width: 60%;
  border-radius: 25px;
  cursor: pointer;
  opacity: 0.9;
  text-align: center;
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
  background: rgba(200, 200, 200, 0.9);
}

</style>
