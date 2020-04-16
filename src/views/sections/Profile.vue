<template>
    <div class="container">
        <router-link tag="button" v-if="business" to="newRestaurant">Aggiungi ristorante</router-link>

        <hr>
        <p> Username: {{user.username}}</p>
        <p> Email: {{user.email}}</p>
        <p> Nome: {{user.first_name}}</p>
        <p> Cognome: {{user.last_name}}</p>
        <p> Numero di Telefono: {{user.phone}}</p>
        <p> Data di nascita: {{user.birth_date}}</p>
        <p> Per modificare la password : </p>

     <v-form @submit.prevent="change_psw">

         <v-text-field :error-messages="errors.old_password" @change="errors.old_password=''" label="Vecchia Password" v-model='old_password' type="password" placeholder=" Inserire vecchia password" id="old_password" name="old_password" required></v-text-field>
         <hr><hr>
         <v-text-field label="Nuova Password" v-model='new_password' type="password" placeholder=" Inserire nuova password" id="new_password" name="new_password" required></v-text-field>
         <!--v-text-field label="Ripeti Nuova Password" v-model='new_password2' type="password" placeholder=" Reinserire nuova password" id="new_password2" name="new_password2" required></v-text-field-->

         <button type="submit" class="password_btn" >Modifica Password</button>
        <hr>
     </v-form>

    </div>
</template>

<script>
    import Heading from '@/mixins/heading'
    import { mapActions } from 'vuex'

    export default {
        name: "Profile",

        mixins: [Heading],

        data() {
            return {
                business: true,
                old_password: '',
                new_password: '',
                new_password2: '',
            }
        },
        methods:
            {
                ...mapActions('userProfile', ['changePassword']),
                change_psw: function () {
                    this.changePassword({
                        old_password: this.old_password,
                        new_password: this.new_password,
                       /* new_password2: this.new_password2,*/
                    }).then( messaggio => {
                        alert(messaggio)
                    })

                }
            },
                computed:
                    {
                        user() {
                            return this.$store.getters['userProfile/user']
                        },
                        errors(){
                            return this.$store.getters['userProfile/errors']
                        },
                    },
    }
</script>

<style scoped>
.password_btn {
  background-color: #4CAF50;
  color: white;
  padding: 16px 20px;
  margin: 4px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}
.password_btn:hover {
  opacity:1;
}
</style>
