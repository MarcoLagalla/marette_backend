<template>

    <div class="body">
        <!-- p>{{this.$route.query.code}}</p -->

        <base-section id="">
            <div class="title-center">
                <h1>Ristoranti</h1>
                <div class="divider"></div>
                <span class="subt"> Ecco la nostra scelta di ristoranti</span></div>

            <v-container>
                <v-row>
                    <v-col v-for="(restaurant, i) in restaurantList" :key="i" cols="12" md="4">
                        <router-link :to="restaurant.url">
                            <v-card v-bind="restaurant" class="restcard" max-width="400" max-height="400">
                                <v-img class="white--text align-end imag" height="200px"
                                       :src="restaurant.image">
                                    <v-card-title><h2>{{ restaurant.activity_name }}</h2></v-card-title>
                                </v-img>

                                <v-card-text >
                                    <div class="description">{{ restaurant.activity_description }}</div>
                                </v-card-text>
                                <v-divider/>
                                <div class="actions">
                                    <button class="share">
                                        Condividi
                                        <v-icon color="var(--ming)"> mdi-share-variant</v-icon>
                                    </button>
                                    <button class="like">
                                        <v-icon color="var(--ming)"> mdi-heart</v-icon>
                                    </button>
                                </div>
                            </v-card>
                        </router-link>
                    </v-col>
                </v-row>
            </v-container>
        </base-section>
    </div>
</template>

<script>
    export default {
        name: 'RestaurantCards',

        data: () => ({}),
        computed: {
            restaurantList() {
                return this.$store.getters['restaurants/restaurantList']
            }
        },
        created() {
            this.$store.dispatch("restaurants/getRestaurants")
        }
    }
</script>
<style scoped>
    .body {
        /*background: linear-gradient(to bottom, #aaffa9, #11ffbd)!important;*/
        background: var(--whitesmoke);
    }

    .divider {
        width: 50px;
        background: var(--ming);
        height: 5px;
        margin: auto;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .title-center {
        padding: 10px;
        margin: 10px;
        display: block;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .actions {
        padding: 10px;
    }

    .like {
        float: right;
        padding: 10px;
        transition: 0.3s ease-in-out;
        opacity: 0.8;
    }

    .share {
        font-weight: bold;
        color: var(--ming);
        border-radius: 25px;
        padding: 10px;
        font-size: 1em;
        transition: 0.3s ease-in-out;
    }

    .share:hover {
        color: var(--ming);
        opacity: 1;
    }

    .shalikere:hover {
        color: var(--ming);
        opacity: 1;
    }

    .restcard {
        box-shadow: 0 0 5px var(--charcoal);
        transition: 0.4s;
        margin: 10px;

    }

    .restcard:hover {
        box-shadow: 0 0 20px var(--charcoal);
    }

    .imag {
        box-shadow: 0 2px 2px var(--charcoal);
        text-shadow: 0 0 2px black;
    }

    a {
        text-decoration: none
    }

    .subt {
        color: var(--darkslate);
        font-weight: bold;
    }

    h1 {
        color: var(--darkslate);
        font-size: 2em;
    }

    h2 {
        text-transform: capitalize;
    }
    .description {
        overflow: hidden!important;
        height: 50px;
    }
</style>
