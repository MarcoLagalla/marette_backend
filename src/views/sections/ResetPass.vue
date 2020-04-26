<template>
  <div class="body">
        <h1> RESET PASSWORD</h1><br><br>
    <v-row align="center" class="mx-0 pa-8" justify="center">

<div class="rp">



        <v-form v-if="reset_token" @submit.prevent="compare_token" >


            <v-text-field
                    :error-messages="errors.password" @change="errors.password=''"

                    v-model='password'
                    type="password"
                    label=" Inserire nuova password"
                    id="password"
                    name="password" required></v-text-field>

            <v-text-field
                    :rules="passwordRules" :error-messages="errors.password" @change="errors.password=''"

                    v-model='password2'
                    type="password"
                    label=" Ripeti nuova password"
                    id="password2"
                    name="password2" required></v-text-field>
            <button type="submit"  class="password_btn" :disabled="!isDisable"> Invia Richiesta cambio password</button>


        </v-form>

    <v-form v-else @submit.prevent="send_email">
        <template v-if="inviato">
            <h2 id="success">Email inviata con successo!</h2>
            <p>Sono passati 10 minuti e non ti è ancora arrivata?<br>Ritenta, sarai più fortunato!</p>
        </template>


        <v-text-field

                :rules="emailRules" :error-messages="errors.email" @change="errors.email=''"

                v-model='email'
                type="email"
                label=" Inserire email associata all'account"
                id="email"
                name="email"
                required>

        </v-text-field>
        <button type="submit"  class="password_btn">Invia Nuova Richiesta</button>

    </v-form>
</div>
  </v-row>
</div>
</template>

<script>

import Heading from '@/mixins/heading'
import { mapActions } from 'vuex'

    export default {
        name: "ResetPass",

        mixins: [Heading],

        data(){
            return{
                email: '',
                reset_token: this.$route.query.token,
                password:'',
                password2:'',
                valid: true,
                inviato: false,

                emailRules: [
                    v => !!v || 'Campo obbligatorio',
                    v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
                ],
                passwordRules: [
                    v => !!v || 'Campo obbligatorio',
                    v => v === this.password || "Le password devono combaciare",
                ],
            }
        },

        methods:
            {
                ...mapActions('userAuthentication', ['AskPasswordreset']),
                send_email: function(){
                    this.AskPasswordreset({
                        email: this.email,
                    }).then( () => {

                            this.inviato=true;

                        })

                        .catch(error => {

                            alert(error)
                        })

                    },

                    ...mapActions('userAuthentication',['ConfirmPasswordreset']),
                compare_token: function(){
                    this.ConfirmPasswordreset({
                        token: this.reset_token,
                        password: this.password,
                        password2: this.password2,
                    }).then( messaggio => {

                            this.$router.push('/')
                            alert(messaggio)

                        })

                        .catch(error => {

                            alert(error)
                        })
                }

                },



        computed:
            {
                errors(){
                    return this.$store.getters['userProfile/errors']
                },

                isDisable(){
                    if (this.password)
                        return this.password === this.password2
                    else
                        return false
                    }



            },








    }
</script>

<style scoped>
.rp {
  width: 50%;
}
#success {
    color: #1e7e34;
}
.body {
  background: oldlace;
}
h1{
  text-align: center;
  padding: 20px;
  color: var(--chilli);
}
.password_btn {
  background-color: var(--herb);
  color: white;
  border: inset var(--herb) 2px!important;
  padding: 16px 20px;
  margin: 4px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.8;
  transition: 0.5s;
  border-radius: 10px;
}
.password_btn:hover {
  opacity:1;
  box-shadow: 0 0 10px grey;
}

.password_btn:disabled{
        background: grey;
}
</style>
