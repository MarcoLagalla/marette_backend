<template>
     <form @submit.prevent="register">
        <div class="container">
            <h1>Registrati</h1>
            <p>Dammi dei bei dati per registrare un account.</p>

            <hr>

            <label for="username"><b>Username*</b></label>
            <v-text-field :error-messages="errors.username" v-model='username' type="text" placeholder="Inserire Username" id="username" name="username" required></v-text-field>

            <label for="email"><b>Email*</b></label>
            <v-text-field :error-messages="errors.email" v-model='email' type="email" placeholder="Inserire Email" id="email" name="email" required></v-text-field>

            <label for="psw"><b>Password*</b></label>
            <v-text-field :error-messages="errors.password" v-model='password' type="password" placeholder="Inserire Password" id="psw" name="psw" required></v-text-field>

            <label for="psw-repeat"><b>Ripeti la Password*</b></label>
            <v-text-field :error-messages="errors.password2" v-model='password2' type="password" placeholder="Ripetere Password" id="psw-repeat" name="psw-repeat" required></v-text-field>

            <label for="phone"><b>Numero di Telefono valido*</b></label>
            <v-text-field :error-messages="errors.phone" v-model='phone' type="tel" placeholder="Inserire Numero di Telefono" id="phone" name="phone" required></v-text-field>

            <label for="first_name"><b>Nome*</b></label>
            <v-text-field :error-messages="errors.first_name" v-model='first_name' type="text" placeholder="Inserire Nome" id="first_name" name="first_name" required></v-text-field>

            <label for="last_name"><b>Cognome*</b></label>
            <v-text-field :error-messages="errors.last_name" v-model='last_name' type="text" placeholder="Inserire Cognome" id="last_name" name="last_name" required></v-text-field>

            <label for="birth_date"><b>Data di nascita*</b></label>
            <v-text-field :error-messages="errors.birth_date" v-model='birth_date' type="date" placeholder="Inserire Data di Nascita" id="birth_date" name="birth_date" required></v-text-field>

            <label for="last_name"><b>Codice fiscale*</b></label>
            <v-text-field :error-messages="errors.cf" v-model='cf' type="text" placeholder="Inserire CF" id="cf" name="cf" required></v-text-field>

            <label for="last_name"><b>Città di residenza*</b></label>
            <v-text-field :error-messages="errors.city" v-model='city' type="text" placeholder="Inserire residenza" id="city" name="city" required></v-text-field>

            <label for="last_name"><b>Indirizzo con numero civico*</b></label>
            <v-text-field :error-messages="errors.address" v-model='address' type="text" placeholder="Inserire indirizzo" id="address" name="address" required></v-text-field>

            <label for="last_name"><b>CAP*</b></label>
            <v-text-field :error-messages="errors.cap" v-model='cap' type="number" placeholder="Inserire CAP" id="cap" name="cap" required></v-text-field>

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
    import Heading from '@/mixins/heading'

    export default {
        name: "Registration",

        mixins: [Heading],

        data () {
            return {
                username:'',
                email: '',
                password: '',
                password2: '',
                first_name: '',
                last_name: '',
                birth_date: '',
                phone: '',
                cap: '',
                address: '',
                city: '',
                cf: ''
            }
        },
        methods:
        {
            ...mapActions('userAuthentication', ['registerBusiness']),
            register: function () {
                this.registerBusiness({
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    password2: this.password2,
                    phone: this.phone,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    birth_date: this.birth_date,
                    cap: this.cap,
                    address: this.address,
                    city: this.city,
                    cf: this.cf
                }).then(() => {
                    this.$router.push('/profile')
                }).catch(error =>{
                    var id = Object.keys(error)[0];
                    document.getElementById(id).scrollIntoView(false)
                    document.getElementById(id).focus({preventScroll:true});
                })
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
    input[type=text], input[type=password] , input[type=tel] , input[type=date], input[type=number], input[type=email] {
      width: 100%;
      padding: 15px;
      margin: 5px 0 22px 0;
      display: inline-block;
      border: none;
      background: #f1f1f1;
    }
    input[type=text]:focus, input[type=password], input[type=tel] , input[type=date], input[type=number], input[type=email] :focus {
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
