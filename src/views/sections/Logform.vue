<template>
        <form @submit.prevent="login" class="container">
            <h1>Log in</h1>
            <p>Inserire dati per loggare.</p>
            <h2 v-if="status === 'error'">Hai ciccato qualcosa!</h2>
            <hr>


            <label for="email"><b>Email</b></label>
            <input v-model='email' type="email" placeholder="Inserire Email" id="email" name="email" required>

            <label for="psw"><b>Password</b></label>
            <input v-model='password' type="password" placeholder="Inserire Password" id="psw" name="psw" required>

            <hr>
            <p>Non sei ancora Registrato ?  <router-link to="/registration"> Registrati </router-link></p>
            <button class="loginbtn">Collegati</button>
        </form>

</template>

<script>
    import { mapActions } from 'vuex'
    export default {
        name: "Login",
        data () {
            return {
                    email:'',
                    password:''
            }
        },
        methods:
        {
            ...mapActions('userAuthentication', ['signIn']),
            login: function () {
                this.signIn({
                email: this.email,
                password: this.password,
                }).then(() => {
                   this.$router.push('/profile')
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
