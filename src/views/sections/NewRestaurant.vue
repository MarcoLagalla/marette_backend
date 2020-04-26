<template>
  <div class="background">
      <v-row align="center" class="mx-0 pa-8" justify="center">

  <div class="body">
     <form @submit.prevent="register" class="px-8">
        <h1>Nuovo Locale <v-icon class="icfood">
          mdi-food-fork-drink
        </v-icon></h1>
        <p class="error" v-if="errors" id="detail">{{errors.detail}}</p>

        <v-col >
          <v-row align="center" class="ma-0" justify="center" >
        <v-text-field label="Nome del locale*" :error-messages="errors.activity_name" @change="errors.activity_name=''" v-model='activity_name' type="text" id="activity_name" name="activity_name" required></v-text-field>

        <v-textarea label="Fornisci una breve descrizione del locale*" :error-messages="errors.activity_description" @change="errors.activity_description=''" v-model='activity_description' id = "activity_description" rows = "3" cols = "80" name="activity_description"  required></v-textarea>
  </v-row><v-row align="center" class="ma-0" justify="center" >
        <v-text-field label="Città in cui è locata l'attività*" :error-messages="errors.city" @change="errors.city=''" v-model='city' type="text" id="city" name="psw" required></v-text-field>

        <v-text-field label="Indirizzo del locale*" :error-messages="errors.address" @change="errors.address=''" v-model='address' type="text" id="address" name="address" required></v-text-field>
  </v-row><v-row align="center" class="ma-0" justify="center" >
        <v-text-field label="Numero civico*" :error-messages="errors.n_civ" @change="errors.n_civ=''" v-model='n_civ' type="text" id="n_civ" name="n_civ" required></v-text-field>

        <v-text-field label="CAP del locale*" :error-messages="errors.cap" @change="errors.cap=''" v-model='cap' type="number" id="cap" name="cap" required></v-text-field>
  </v-row><v-row align="center" class="ma-0" justify="center" >
        <v-text-field label="Numero di Telefono valido del locale*" :error-messages="errors.restaurant_number" @change="errors.restaurant_number=''" v-model='restaurant_number' type="tel"  id="restaurant_number" name="restaurant_number" required></v-text-field>

        <v-text-field label="Partita iva associata al locale*" :error-messages="errors.p_iva" @change="errors.p_iva=''" v-model='p_iva' type="number"  id="p_iva" name="p_iva" required></v-text-field>

      </v-row></v-col>

        <button type="submit" class="registerbtn" >Aggiungi ristorante</button>
    </form>  </div>  </v-row>   </div>
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
                n_civ: '',
                cap: '',
                restaurant_number: '',
                p_iva: ''
            }
        },
        methods:
        {
            ...mapActions('restaurants', ['newRestaurant']),
            register: function () {
                this.newRestaurant({
                    activity_name: this.activity_name,
                    activity_description: this.activity_description,
                    city: this.city,
                    address: this.address,
                    n_civ: this.n_civ,
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
                    return this.$store.getters['restaurants/errors']
                }
            }
    }
</script>

<style scoped>
.icfood {
  color: var(--chilli)
}
.background{
  background-color: whitesmoke;
}
.body {
  background-color: white;
  text-align: center;
  width: 60%;
  box-shadow: inset 0 0 10px #000;
  padding: 20px;
  border-radius: 25px;
}

h1{
  color: var(--chilli)
}
.v-text-field {
  padding: 10px;
}
    .registerbtn {
      background-color: var(--chilli);
      color: white;
      padding: 16px 20px;
      margin: 8px 0;
      font-weight: bold;
      border: none;
      cursor: pointer;
      width: 100%;
      opacity: 0.9;
      transition: 0.6s;
      border-radius: 25px;
      box-shadow: 0 0 2px black;
    }
    .registerbtn:hover {
      opacity:1;
      box-shadow: 0 0 10px black;
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
