<template>
    <div class="body">
        <v-container>

            <v-row dense>
                <v-col cols="6">
                    <v-card class="profilc" dark>
                        <v-row>
                            <v-card-title class="profilo">il tuo profilo</v-card-title>
                            <v-avatar class="profimag" size="125" tile>
                                <v-img src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"></v-img>
                            </v-avatar>
                        </v-row>
                        <v-card-subtitle>
                            <p v-for="(campo, i) in user" :key="i">{{i.replace(/_/g , ' ')}} : {{campo}}</p>
                        </v-card-subtitle>
                        <router-link tag="button" class="addrest" v-if="isBusiness" to="newRestaurant">Aggiungi
                            ristorante
                            <v-icon right dark>
                                mdi-food-fork-drink
                            </v-icon>
                        </router-link>
                        <v-card-actions>
                            <v-btn @click="show = !show" text>Modifica password
                                <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                            </v-btn>
                        </v-card-actions>

                        <v-expand-transition>
                            <div v-show="show">
                                <v-divider></v-divider>
                                <v-form @submit.prevent="change_psw">
                                    <v-row align="center" class="ma-0 mt-8" justify="center">
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field light :error-messages="errors.old_password"
                                                          @change="errors.old_password=''" solo
                                                          background-color="#FFF8DC" v-model='old_password'
                                                          type="password" placeholder=" Inserire vecchia password"
                                                          id="old_password"
                                                          name="old_password" required>
                                            </v-text-field>

                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field light :rules="passwordRules" :error-messages="errors.password"
                                                          @change="errors.password=''" solo background-color="#FFF8DC"
                                                          v-model='new_password' type="password"
                                                          placeholder=" Inserire nuova password"
                                                          id="new_password" name="new_password" required>
                                            </v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">

                                            <v-text-field light :rules="password2Rules"
                                                          :error-messages="errors.password" @change="errors.password=''"
                                                          solo background-color="#FFF8DC" v-model='new_password2'
                                                          type="password" placeholder=" Reinserire nuova password"
                                                          id="new_password2" name="new_password2" required>
                                            </v-text-field>
                                        </v-col>

                                    </v-row>
                                    <div class="regbtn2">
                                        <div class="center">
                                            <button type="submit" class="password_btn">Modifica Password</button>
                                        </div>
                                    </div>
                                </v-form>
                            </div>
                        </v-expand-transition>
                    </v-card>
                </v-col>

                <!--v-col v-for="(item, i) in items" :key="i" cols="12">
                <v-card :color="item.color" dark>
                <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                <v-card-title class="headline" v-text="item.title"></v-card-title>

                <v-card-subtitle v-text="item.artist"></v-card-subtitle>
                </div>

                <v-avatar class="ma-3" size="125" tile>
                <v-img :src="item.src"></v-img>
                </v-avatar>
                </div>
                </v-card>
                </v-col-->

                <v-col cols="6">
                    <v-row v-for="(restaurant, i) in userRestaurantList" :key="i">
                        <v-card class="restc" v-bind="restaurant" dark>
                            <div class="d-flex flex-no-wrap justify-space-between">
                                <div>
                                    <v-card-title class="restitle">{{ restaurant.activity_name }}</v-card-title>

                                    <v-card-subtitle class="pb-0">{{ restaurant.activity_description }}
                                    </v-card-subtitle>

                                </div>
                                <v-col>
                                    <router-link tag="button" class="settings" v-if="isBusiness"
                                                 :to="'profile/'+restaurant.url">
                                        <v-icon x-large dark>
                                            fas fa-cogs
                                        </v-icon>
                                    </router-link>
                                    <router-link tag="button" class="settings" v-if="isBusiness"
                                                 :to="'profile/manage/' + restaurant.url">
                                        <v-icon x-large dark>
                                            fas fa-address-card
                                        </v-icon>
                                    </router-link>
                                </v-col>
                                <v-avatar class="ma-3" size="125" tile>
                                    <v-img :src="restaurant.image"></v-img>
                                </v-avatar>
                            </div>


                            <!--router-link :to="restaurant.url">
                            <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                            <v-card-title>{{ restaurant.activity_name }}</v-card-title>
                          </v-img>
                          </router-link>
                          <v-card-subtitle class="pb-0">Descrizione</v-card-subtitle>

                          <v-card-text class="text--primary">
                          <div>{{ restaurant.activity_description }}</div>
                          </v-card-text>

                          <v-card-actions>
                          <router-link :to="'profile/'+restaurant.url">
                          <v-btn color="orange" text>
                          Gestione ristorante
                          </v-btn>
                          </router-link>
                          <v-btn color="orange" text>
                          Modifica ristorante
                          </v-btn>
                          </v-card-actions-->
                        </v-card>
                    </v-row>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
    import Heading from '@/mixins/heading'
    import {
        mapActions
    } from 'vuex'

    export default {
        name: "Profile",

        mixins: [Heading],

        data() {
            return {
                old_password: '',
                new_password: '',
                new_password2: '',
                passwordRules: [
                    v => !!v || 'Campo obbligatorio',
                    v => v !== this.old_password || "La nuova password deve essere diversa dalla vecchia"
                ],
                password2Rules: [
                    v => !!v || 'Campo obbligatorio',
                    v => v === this.new_password || "Le password devono combaciare"
                ],
                show: false,
            }
        },
        methods: {
            ...mapActions('userProfile', ['changePassword']),
            change_psw: function () {
                this.changePassword({
                    old_password: this.old_password,
                    new_password: this.new_password,
                    new_password2: this.new_password2,

                }).then(messaggio => {

                    alert(messaggio)

                })

            }
        },
        computed: {
            user() {
                return this.$store.getters['userProfile/user']
            },
            user_private() {
                return this.$store.getters['userProfile/user_private']
            },
            errors() {
                return this.$store.getters['userProfile/errors']
            },
            isBusiness() {
                return this.$store.getters['userProfile/isBusiness']
            },
            userRestaurantList() {
                return this.$store.getters['restaurants/userList']
            }
        },

        created() {
            this.$store.dispatch("restaurants/getUserRestaurants")
        }
    }
</script>

<style scoped>
    .body {
        /*background: linear-gradient(to bottom, #aaffa9, #11ffbd)!important;*/
        background: var(--whitesmoke);
    }

    .settings {
        background-color: var(--darkslate);
        color: white;
        margin: 5px;
        padding: 10px;
        border-radius: 25px;
        transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
        font-weight: bold;
        border: inset 2px var(--darkslate);
        float: right;
    }

    .profimag {
        position: absolute;
        right: 0;
        margin: 10px;
    }

    .settings:hover {
        box-shadow: 0 0 4px var(--charcoal);
    }

    .restc {
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
        background: var(--ming);
        width: 100%;
        margin-left: 10px;
        margin-bottom: 10px;
        transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
    }

    .restc:hover {
        transform: scale(1.01);
    }

    .restitle {
        text-transform: capitalize;
    }

    .profilc {
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
        background: var(--ming);
    }

    .profilo {
        font-size: 1.6em;
        color: var(--whitesmoke);
        text-transform: capitalize;
    }

    .regbtn2 {
        padding: 10px;
        margin-bottom: 10px;
        display: flex;
        align-items: left;
        justify-content: left;
    }

    .password_btn {
        background-color: var(--darkslate);
        color: white;
        border: inset var(--darkslate) 2px !important;
        padding: 16px 20px;
        margin: 4px 0;
        border: none;
        cursor: pointer;
        width: 100%;
        opacity: 0.8;
        transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
        border-radius: 10px;
    }

    .password_btn:hover {
        opacity: 1;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    }

    .addrest {
        background-color: var(--darkslate);
        color: white;
        padding: 15px;
        border-radius: 25px;
        transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
        margin-left: 10px;
        font-weight: bold;
        border: inset 2px var(--darkslate);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    }

    .addrest:hover {
        box-shadow: 0 10px 12px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    }
</style>
