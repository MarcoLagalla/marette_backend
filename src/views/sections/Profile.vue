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
                            <v-img :src="user_private.avatar"></v-img>
                        </v-avatar>
                        <v-divider></v-divider>
                        <v-tabs show-arrows :vertical="$vuetify.breakpoint.mdAndUp">
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
                                            <base-manage-user-data :editing="false"></base-manage-user-data>
                                        </v-card-subtitle>
                                    </div>
                                    <base-change-password></base-change-password>
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


                                                <button class="gestrest" @click="editingRest=!editingRest"><span class="butgest"> Modifica dati  </span></button>
                                            </v-card-actions>
                                        </v-col>
                                        <v-col cols="12" md="6">

                                            <v-avatar class="imgrest" size="125" tile>
                                                <v-img :src="restaurant.image"></v-img>
                                            </v-avatar>
                                        </v-col>

                                    </v-row>
                                    <base-manage-rest-data :id="restaurant.id"
                                    :editing="editingRest"
                                    >

                                    </base-manage-rest-data>
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
    export default {
        name: "Profile",
        mixins: [Heading],

        data() {
            return {
                editingRest:false,
            }
        },
        computed: {
            user() {
                return this.$store.getters['userProfile/user']
            },
            user_private() {
                return this.$store.getters['userProfile/user_private']
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
