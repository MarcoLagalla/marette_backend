<template>
    <div class="body">
        <v-container>
            <v-row dense>
                <v-col cols="12">
                    <v-card>
                        <v-toolbar flat class="profilctool" dark>
                            <v-toolbar-title>Il Tuo Profilo</v-toolbar-title>
                        </v-toolbar>
                        <v-avatar class="profimag" size="155" tile>
                            <v-img :src="user.avatar"></v-img>
                        </v-avatar>
                        <v-divider></v-divider>
                        <v-tabs vertical>
                            <v-tab>
                                <v-icon left>mdi-account</v-icon>
                                Profilo
                            </v-tab>
                            <v-tab v-for="(restaurant, i) in userRestaurantList" :key="i">
                                <v-icon left>fas fa-utensils</v-icon>
                                {{ restaurant.activity_name }}
                            </v-tab>

                            <v-tab-item>
                                <v-card flat>
                                    <div class="bodyprofile">


                                        <v-card-subtitle>
                                            <v-row v-for="(campo, i) in user" :key="i">
                                                <v-col cols="3" class="dati"><b>{{i.replace(/_/g , ' ')}}:</b></v-col>
                                                <v-col cols="4">{{campo}}</v-col>
                                            </v-row>
                                        </v-card-subtitle>
                                    </div>
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
                                                                      type="password"
                                                                      placeholder=" Inserire vecchia password"
                                                                      id="old_password"
                                                                      name="old_password" required>
                                                        </v-text-field>
                                                    </v-col>
                                                    <v-col cols="12" sm="6" md="4">
                                                        <v-text-field light :rules="passwordRules"
                                                                      :error-messages="errors.password"
                                                                      @change="errors.password=''" solo
                                                                      background-color="#FFF8DC" v-model='new_password'
                                                                      type="password"
                                                                      placeholder=" Inserire nuova password"
                                                                      id="new_password" name="new_password" required>
                                                        </v-text-field>
                                                    </v-col>
                                                    <v-col cols="12" sm="6" md="4">
                                                        <v-text-field light :rules="password2Rules"
                                                                      :error-messages="errors.password"
                                                                      @change="errors.password=''" solo
                                                                      background-color="#FFF8DC" v-model='new_password2'
                                                                      type="password"
                                                                      placeholder=" Reinserire nuova password"
                                                                      id="new_password2" name="new_password2" required>
                                                        </v-text-field>
                                                    </v-col>
                                                </v-row>
                                                <div class="regbtn2">
                                                    <div class="center">
                                                        <button type="submit" class="password_btn">Modifica Password
                                                        </button>
                                                    </div>
                                                </div>
                                            </v-form>
                                        </div>
                                    </v-expand-transition>
                                </v-card>
                            </v-tab-item>
                            <v-tab-item v-for="(restaurant, i) in userRestaurantList" :key="i">
                                <v-card flat class="restc" dark v-bind="restaurant" min-height="150" >
                                    <v-row>
                                        <v-col cols="12" md="6">
                                            <v-card-title class="restitle">{{ restaurant.activity_name }}</v-card-title>
                                            <div class="divider"></div>
                                            <v-card-subtitle class="description">{{ restaurant.activity_description }}
                                            </v-card-subtitle>
                                            <v-card-actions>
                                                <router-link tag="button" class="gestrest"
                                                             :to="'profile/'+restaurant.url">
                                                    <span class="butgest"> gestisci ristorante  </span>
                                                    <v-icon class="wrench" medium>fas fa-wrench</v-icon>
                                                </router-link>

                                                <router-link tag="button" class="gestrest"
                                                             :to="'profile/manage/' + restaurant.url">
                                                    <span class="butgest"> gestisci dati  </span>
                                                    <v-icon class="edit" medium>far fa-edit</v-icon>
                                                </router-link>
                                            </v-card-actions>
                                        </v-col>
                                        <v-col cols="12" md="6">

                                            <v-avatar class="imgrest" size="125" tile>
                                                <v-img :src="restaurant.image"></v-img>
                                            </v-avatar>
                                        </v-col>
                                    </v-row>
                                </v-card>
                            </v-tab-item>
                        </v-tabs>
                    </v-card>
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

    .profimag {

        margin: 10px;
        border-radius: 15px 50px;
        box-shadow: 0 0 2px black;
    }

    .profilctool {
        background: var(--ming) !important;
    }


    .restc {
    //box-shadow: 0 14 px 28 px rgba(0, 0, 0, 0.25), 0 10 px 10 px rgba(0, 0, 0, 0.22);
        background: white;
        width: 100%;
        transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
        color: #1a1a1a;
    }

    .restitle {
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

    .imgrest {
        right: 0;
        top: 0;
        margin: 10px;
        position: absolute;
    }

    .description {
        color: #1a1a1a !important;
        overflow: hidden;
        height: 150px!important;

    }

    .dati {
        background: var(--whitesmoke);
        text-align: center;
    }

    .divider {
        width: 100%;
        background: var(--ming);
        height: 2px;

    }

    .gestrest {
        background: var(--ming);
        padding: 10px;
        border-radius: 25px;
        transition: ease-in-out 0.3s;
        margin-right: 10px;
    }

    .butgest {
        text-transform: capitalize;
        color: white;
        font-weight: bold;
    }

    .gestrest:hover {
        transform: scale(1.1);
    }
    .gestrest:hover > .wrench {
        transform: rotate(45deg);
    }

</style>
