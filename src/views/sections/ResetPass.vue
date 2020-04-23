<template>
    <v-container>
        <h1> RESET PASSWORD</h1><br><br>


        <v-form v-if="reset_token" @submit.prevent="compare_token" >
            <p> Inserire nuova password: </p>

            <v-text-field
                    :error-messages="errors.password" @change="errors.password=''"
                    solo background-color="#486F83"
                    v-model='password'
                    type="password"
                    placeholder=" Inserire nuova password"
                    id="password"
                    name="password" required></v-text-field>

            <v-text-field
                    :rules="passwordRules" :error-messages="errors.password" @change="errors.password=''"
                    solo background-color="#486F83"
                    v-model='password2'
                    type="password"
                    placeholder=" Ripeti nuova password"
                    id="password2"
                    name="password2" required></v-text-field>
            <button type="submit"  class="password_btn" :disabled="!isDisable"> Invia Richiesta cambio password</button>


        </v-form>

    <v-form v-else @submit.prevent="send_email">
        <p> Inserire Email: </p>

        <v-text-field
                label="Email"
                :rules="emailRules" :error-messages="errors.email" @change="errors.email=''"
                solo background-color="#486F83"
                v-model='email'
                type="email"
                placeholder=" Inserire email associata all'account"
                id="email"
                name="email"
                required>

        </v-text-field>
        <button type="submit"  class="password_btn" > Invia Richiesta</button>

    </v-form>

    </v-container>
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
                    }).then( messaggio => {

                            alert(messaggio)

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

.password_btn {
  background-color: #4CAF50;
  color: white;
  border: inset #4CAF50 2px!important;
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