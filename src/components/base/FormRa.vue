<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" overlay-opacity="0.8" max-width="600px" class="dial" scrollable>
            <template v-slot:activator="{ on }">
                <div class="rel">
                    <button class="btn-6" v-on="on"><span>signup</span></button>
                </div>
            </template>
            <v-card class="regcard">
                <vue-custom-scrollbar class="scroll-area" :settings="settings" @ps-scroll-y="scrollHanle">
                    <v-form @submit.prevent="register" v-model="valid">
                        <div class="cardtitle" style="margin-top: 10px;">
                            <h1>REGISTRATI</h1>
                        </div>
                        <v-divider></v-divider>
                        <p class="error" v-if="errors.error" id="error">{{errors.error[0]}}</p>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="12" md="6">
                                        <v-text-field :error-messages="errors.first_name" @change="errors.first_name=''"
                                                      solo filed v-model="first_name" label="Nome"
                                                      prepend-inner-icon="mdi-account-cowboy-hat"
                                                      id="first_name"></v-text-field>

                                        <v-text-field :error-messages="errors.last_name" @change="errors.last_name=''"
                                                      solo prepend-inner-icon="mdi-account-cowboy-hat"
                                                      filed v-model="last_name" label="Cognome"
                                                      id="last_name"></v-text-field>
                                    </v-col>

                                    <v-col cols="12" sm="6" md="6">
                                        <picture-input
                                                ref="avatar"
                                                @change="onChanged"
                                                :width="150"
                                                :height="150"
                                                size="3"
                                                :zIndex="0"
                                                :crop="true"
                                                :changeOnClick="false"
                                                accept="image/jpeg, image/png, image/gif"
                                                buttonClass="ui button primary"
                                                :customStrings="{
                      upload: '<h1>Carica immagine</h1>',
                      drag: 'Trascina qui la un immagine di profilo o clicca per selezionarla'}">
                                        </picture-input>

                                    </v-col>
                                    <v-col cols="12" sm="6" md="6">
                                        <v-text-field :rules="nameRules" :error-messages="errors.username"
                                                      @change="errors.username=''" prepend-inner-icon="mdi-account" solo filed
                                                      id="username" v-model="username" label="Username*"
                                                      required></v-text-field>
                                    </v-col>
                                    <v-col cols="12" md="6">
                                        <v-text-field :rules="emailRules" :error-messages="errors.email"
                                                      @change="errors.email=''" prepend-inner-icon="mdi-email" solo filed
                                                      v-model="email" label="Email*" id="email" type="email"
                                                      required></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6">
                                        <v-text-field :rules="phoneRules" :error-messages="errors.phone"
                                                      @change="errors.phone=''" prepend-inner-icon="mdi-phone" solo filed
                                                      id="phone" name="phone" label="Numero di telefono*"
                                                      v-model="phone"
                                                      type="tel" require></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6">
                                        <v-text-field :error-messages="errors.birth_date" @change="errors.birth_date=''"
                                                      prepend-inner-icon="mdi-calendar-range" solo filed id="birth_date"
                                                      label="Data di nascita" v-model="birth_date"
                                                      type="date"></v-text-field>
                                    </v-col>

                                    <v-col cols="12" sm="6" md="6">
                                        <v-text-field :rules="passwordRules" :error-messages="errorPassword"
                                                      @change="errors.password=''" prepend-inner-icon="mdi-key" solo filed
                                                      v-model="password" label="Password*" id="password" type="password"
                                                      required></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="6">
                                        <v-text-field :rules="password2Rules" :error-messages="errors.password2"
                                                      @change="errors.password2=''" prepend-inner-icon="mdi-key" solo filed v-model="password2"
                                                      label="Repeat password*" id="password2" type="password"
                                                      required></v-text-field>
                                    </v-col>

                                </v-row>
                            </v-container>
                            <small style="color:white">*indica i campi obbligatori</small>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-text style="color:white">Registrando un account accetti i nostri
                            <router-link to="/termini">T&C</router-link>
                            .
                        </v-card-text>
                        <div class="regbtn2">
                            <div class="center">
                                <button class="btn" type="submit" :disabled="!valid || loading">
                                    <svg width="140px" height="40px" viewBox="0 0 140 40" class="border">
                                        <polyline points="139,1 139,39 1,39 1,1 139,1" class="bg-line" />
                                        <polyline points="139,1 139,39 1,39 1,1 139,1" class="hl-line" />
                                    </svg>
                                    <span v-if="!loading" >Invia</span>
                                    <span class="loader" v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span>
                                </button>
                            </div>
                        </div>
                        <v-card-text></v-card-text>
                    </v-form>
                </vue-custom-scrollbar>
            </v-card>
        </v-dialog>
    </v-row>
</template>
<script>
    // Mixins
    import Heading from '@/mixins/heading'
    import {
        mapActions
    } from 'vuex'
    import PictureInput from "vue-picture-input";
    import vueCustomScrollbar from 'vue-custom-scrollbar';

    export default {
        name: 'BaseForm',
        components: {
            PictureInput,
            vueCustomScrollbar,
        },
        mixins: [Heading],
        data: () => ({
            dialog: false,
            loading: false,
            settings: {
                maxScrollbarLength: 60
            },
            username: '',
            email: '',
            password: '',
            password2: '',
            first_name: '',
            last_name: '',
            birth_date: '',
            phone: '',
            image: '',
            valid: true,
            nameRules: [
                v => !!v || 'Campo obbligatorio',
            ],
            emailRules: [
                v => !!v || 'Campo obbligatorio',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            passwordRules: [
                v => !!v || 'Campo obbligatorio',
            ],
            password2Rules: [
                v => !!v || 'Campo obbligatorio',
            ],
            phoneRules: [
                v => !!v || 'Campo obbligatorio',
            ],
        }),
        methods: {
            ...mapActions('userAuthentication', ['registerUser']),
            register: function () {
                this.loading = true
                const data = {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    password2: this.password2,
                    phone: this.phone,
                };
                if(this.first_name)
                    data.first_name = this.first_name
                if(this.last_name)
                    data.last_name = this.last_name
                if(this.birth_date)
                    data.birth_date = this.birth_date

                const formData = new FormData();
                formData.append('avatar', this.image);
                formData.append('data', JSON.stringify(data));
                this.registerUser(formData).then(() => {
                    this.$router.push('/profile')
                    this.loading = false
                })
                    .catch(error => {
                        this.loading = false
                        console.log('error')
                        console.log(error)
                        var id = Object.keys(error)[0];
                        document.getElementById(id).scrollIntoView(false)
                        document.getElementById(id).focus({
                            preventScroll: true
                        });

                    })
            },
            onChanged() {
                if (this.$refs.avatar.file) {
                    this.image = this.$refs.avatar.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },
            scrollHanle() {
                //console.log(evt)
            },
        },
        computed: {
            status() {
                return this.$store.getters['userAuthentication/status']
            },
            errors() {
                return this.$store.getters['userAuthentication/errorsR']
            },
            errorPassword() {
              return this.errors.password? this.errors.password.join('; ') : ''
            }
        }
    }
</script>
<style scoped>
    .rel {
        padding: 10px;
    }

    h1 {
        text-align: center;
        color: white;
    }

    .v-text-field {
        border-radius: 25px;
        background-color: inherit;
    }

    .regbtn2 {
        padding: 10px;
        margin: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .regbtn {
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
        background: var(--charcoal);
        opacity: 0.8
    }

    .center {
        width: 140px;
        height: 40px;
        position: absolute;
    }

    .btn {
        width: 140px;
        height: 40px;
        cursor: pointer;
        background: #626e60!important;
        border: 1px solid white;
        outline: none;
        transition: 1s ease-in-out;
    }

    svg {
        position: absolute;
        left: 0;
        top: 0;
        fill: none;
        stroke: #fff;
        stroke-dasharray: 150 480;
        stroke-dashoffset: 150;
        transition: 1s ease-in-out;
    }

    .btn:hover {
        transition: 1s ease-in-out;
        background: #628e60;
    }

    .btn:hover svg {
        stroke-dashoffset: -480;
    }

    .btn span {
        color: white;
        font-size: 18px;
        font-weight: 600;
    }

    .btn-6 {
        display: inline-block;
        position: relative;
        border-radius: 2px;
        background: none;
        border: none;
        color: #fff;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 0 2px black;
        transition: all 0.2s linear;
        background: #2F4F4F;
    }

    .btn-6:hover {
        color: #666;
        transition: all 0.2s linear;
        background: #C0C0C0;
        box-shadow: 0 0 6px black;
    }

    span {
        display: block;
        padding: 5px 20px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .btn-6::before,
    .btn-6::after {
        content: "";
        width: 0;
        height: 2px;
        position: absolute;
        transition: all 0.2s linear;
        background: #2F4F4F;
        filter: blur(2px);
    }

    span::before,
    span::after {
        content: "";
        width: 2px;
        height: 0;
        position: absolute;
        transition: all 0.2s linear;
        background: #2F4F4F;
        filter: blur(2px);
    }

    .btn-6:hover::before,
    .btn-6:hover::after {
        width: 100%;
    }

    .btn-6:hover span::before,
    .btn-6:hover span::after {
        height: 100%;
    }

    .btn-6::before {
        left: 50%;
        top: 0;
        transition-duration: 0.4s;
    }

    .btn-6::after {
        left: 50%;
        bottom: 0;
        transition-duration: 0.4s;
    }

    .btn-6 span::before {
        left: 0;
        top: 50%;
        transition-duration: 0.4s;
    }

    .btn-6 span::after {
        right: 0;
        top: 50%;
        transition-duration: 0.4s;
    }

    .btn-6:hover::before,
    .btn-6:hover::after {
        left: 0;
    }

    .btn-6:hover span::before,
    .btn-6:hover span::after {
        top: 0;
    }

    .btn:disabled {
        background: grey;
    }
    .regcard {
        overflow: hidden!important;
    }
    .dial {
        overflow: hidden!important;
    }
    body {
        overflow: hidden!important;
    }
</style>
