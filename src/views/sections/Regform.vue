<template>
     <form @submit.prevent="register">
        <div class="container">
            <h1>Registrati</h1>
            <p>Dammi dei bei dati per registrare un account.</p>
            <!--template v-if="status === 'error'" v-for="errori in errors">
                <h3 v-for="errore in errori">{{errore}}</h3>
            </template-->
            <hr>

            <label for="username"><b>Username*</b></label>
            <input v-model='username' type="text" placeholder="Inserire Username" id="username" name="username" required>

            <label for="email"><b>Email*</b></label>
            <input v-model='email' type="email" placeholder="Inserire Email" id="email" name="email" required>

            <label for="psw"><b>Password*</b></label>
            <input v-model='password' type="password" placeholder="Inserire Password" id="psw" name="psw" required>

            <label for="psw-repeat"><b>Ripeti la Password*</b></label>
            <input v-model='password2' type="password" placeholder="Ripetere Password" id="psw-repeat" name="psw-repeat" required>

            <label for="phone"><b>Numero di Telefono valido*</b></label>
            <input v-model='phone' type="tel" placeholder="Inserire Numero di Telefono" id="phone" name="phone" required>

            <label for="first_name"><b>Nome</b></label>
            <input v-model='first_name' type="text" placeholder="Inserire Nome" id="first_name" name="first_name" >

            <label for="last_name"><b>Cognome</b></label>
            <input v-model='last_name' type="text" placeholder="Inserire Cognome" id="last_name" name="last_name" >

            <label for="birth_date"><b>Data di nascita</b></label>
            <input v-model='birth_date' type="date" placeholder="Inserire Data di Nascita" id="birth_date" name="birth_date" >

            <hr>

            <p>Registrando un account accetti i nostri <router-link to="/termini">Terms & Privacy</router-link>.</p>
            <button type="submit" class="registerbtn" >Registrati</button>
        </div>

        <div class="container signin">
            <p>Hai già un account? <a href="#">Dillo prima, coglione</a>.</p>
        </div>
    </form>
</template>

<script>
    import { mapActions } from 'vuex'
    export default {
        name: "Registration",
        data () {
            return {
                username:'',
                email: '',
                password: '',
                password2: '',
                first_name: '',
                last_name: '',
                birth_date: '',
                phone: ''
            }
        },
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

<style scoped>
     {box-sizing: border-box}
    /* Add padding to containers */
    .container {
      padding: 16px;
    }
     h2{
         color: #1e7e34;
     }
     h3{
         color: red;
     }
    /* Full-width input fields */
    input[type=text], input[type=password] , input[type=tel] , input[type=date], input[type=email] {
      width: 100%;
      padding: 15px;
      margin: 5px 0 22px 0;
      display: inline-block;
      border: none;
      background: #f1f1f1;
    }
    input[type=text]:focus, input[type=password], input[type=tel] , input[type=date], input[type=email] :focus {
      background-color: #ddd;
      outline: none;
    }
    /* Overwrite default styles of hr */
    hr {
      border: 1px solid #f1f1f1;
      margin-bottom: 25px;
    }
    /* Set a style for the submit/register button */
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
