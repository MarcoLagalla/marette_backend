<template>
     <form @submit.prevent="register" class="container">
        <h1>Registrati</h1>
        <p class="error" v-if="errors" id="detail">{{errors.detail}}</p>

        <hr>

        <label for="activity_name"><b>Nome del locale*</b></label>
        <v-text-field :error-messages="errors.activity_name" @change="errors.activity_name=''" v-model='activity_name' type="text" placeholder="Inserire nome ristorante" id="activity_name" name="activity_name" required></v-text-field>

        <label for="activity_description"><b>Fornisci una breve descrizione del locale*</b></label>
        <v-textarea  :error-messages="errors.activity_description" @change="errors.activity_description=''" v-model='activity_description' id = "activity_description" rows = "3" cols = "80" name="activity_description" placeholder="Inserire descrizione ristorante" required></v-textarea>

        <label for="city"><b>Città in cui è locata l'attività*</b></label>
        <v-text-field :error-messages="errors.city" @change="errors.city=''" v-model='city' type="text" placeholder="Inserire Città" id="city" name="psw" required></v-text-field>

        <label for="address"><b>Indirizzo del locale con numero civico*</b></label>
        <v-text-field :error-messages="errors.address" @change="errors.address=''" v-model='address' type="text" placeholder="Inserire Indirizzo" id="address" name="address" required></v-text-field>

        <label for="cap"><b>CAP del locale*</b></label>
        <v-text-field :error-messages="errors.cap" @change="errors.cap=''" v-model='cap' type="number" placeholder="Inserire CAP" id="cap" name="cap" required></v-text-field>

        <label for="restaurant_number"><b>Numero di Telefono valido del locale*</b></label>
        <v-text-field :error-messages="errors.restaurant_number" @change="errors.restaurant_number=''" v-model='restaurant_number' type="tel" placeholder="Inserire Numero di Telefono" id="restaurant_number" name="restaurant_number" required></v-text-field>

        <label for="p_iva"><b>Partita iva associata al locale*</b></label>
        <v-text-field :error-messages="errors.p_iva" @change="errors.p_iva=''" v-model='p_iva' type="number" placeholder="Inserire Partita IVA" id="p_iva" name="p_iva" required></v-text-field>

        <hr>
        <button type="submit" class="registerbtn" >Aggiungi ristorante</button>
    </form>
</template>

<script>
    import { mapActions } from 'vuex'
    export default {
        name: "NewRestaurant",
        data () {
            return {
                activity_name:'',
                activity_description: '',
                city: '',
                address: '',
                cap: '',
                restaurant_number: '',
                p_iva: ''
            }
        },
        methods:
        {
            ...mapActions('restaurant', ['newRestaurant']),
            register: function () {
                this.newRestaurant({
                    activity_name: this.activity_name,
                    activity_description: this.activity_description,
                    city: this.city,
                    address: this.address,
                    cap: this.cap,
                    restaurant_number: this.restaurant_number,
                    p_iva: this.p_iva
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
                errors(){
                    return this.$store.getters['restaurant/errors']
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
    input[type=text], input[type=password] , input[type=tel] , input[type=date], input[type=number] {
      width: 100%;
      padding: 15px;
      margin: 5px 0 22px 0;
      display: inline-block;
      border: none;
      background: #f1f1f1;
    }
    input[type=text]:focus, input[type=password], input[type=tel] , input[type=date], input[type=number] :focus {
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
