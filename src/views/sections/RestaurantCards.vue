<template>

    <div class="body">
        <!-- p>{{this.$route.query.code}}</p -->
        <div class="searchbarcontainer">
        <v-row class="my-2 py-0">
            <v-col cols="12" md="6">

                    <v-row class="py-0" style="padding: 20px;">
                        <v-combobox
                                :items="autocomplete.names"
                                @keydown.enter="search()"
                                @click:append-outer="search"
                                hint="Cerca ristorante per caratteristiche"
                                rounded clearable background-color="#E0E0E0" dense append-outer-icon="fas fa-search" append-icon="" solo filled
                                label="Cerca un ristorante"
                                v-model="query"
                                @update:search-input="query = $event"
                        ></v-combobox>
                    </v-row>
                    <v-row class="py-0">
                        <div class="advquery" v-if="showAdvancedQuery">
                            <v-row>
                                <v-col cols="12" md="5" class="mt-3">
                                    <v-autocomplete
                                            :items="autocomplete.cities"
                                            @keydown.enter="search()"
                                            solo filled rounded background-color="#E0E0E0" dense
                                            :loading="loadingGeo"
                                            label="Città"
                                            :placeholder="city"
                                            v-model="city"
                                            no-data-text="Nessun ristorante ancora presente in questa città"
                                            @click:append-outer="getLocation()"
                                            append-outer-icon="mdi-crosshairs-gps"
                                            append-icon=""
                                    ></v-autocomplete>
                                </v-col>
                                <v-col cols="12" md="7">
                                    <v-row >
                                        <v-col cols="12" md="6">
                                            <v-combobox
                                                    solo filled dense background-color="#E0E0E0" rounded
                                                    :items="restDataCat"
                                                    item-text="category_name"
                                                    item-value="id"
                                                    v-model='restaurant_category'
                                                    id="restaurant_category"
                                                    name="restaurant_category"
                                                    label="Categoria"
                                                    @keydown.enter="search()"
                                            ></v-combobox>
                                        </v-col>
                                        <v-col cols="12" md="6" style="padding: 0px 15px;">
                                            <v-switch v-model="aperto_ora" label="Aperto ora"></v-switch>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                        </div>
                    </v-row>
            </v-col>
        </v-row>
            <v-row class="my-0 py-0">
                    <v-col class="my-0 py-0" cols="12" md="6">
                        <div class="ml-4 p-0" v-if="showAdvancedQuery">
                            <v-slider
                                    height="60"
                                    step="5"
                                    label="Ristoranti per pagina:"
                                    min="10"
                                    max="40"
                                    v-model="restaurantListData.page_size"
                                    thumb-label="always"
                            ></v-slider>
                        </div>
                    </v-col>
            </v-row>
            <v-row>
                <v-btn v-if="!showAdvancedQuery" class="managebutton" @click="showAdvancedQuery = !showAdvancedQuery" text>Ricerca avanzata
                    <v-icon right class="mdi mdi-card-search-outline"></v-icon>
                </v-btn>
                <v-btn v-if="showAdvancedQuery" class="managebutton" @click="showAdvancedQuery = !showAdvancedQuery" text>Ricerca semplice
                    <v-icon right class="mdi mdi-card-search-outline"></v-icon>
                </v-btn>
                <v-btn class="managebutton" text @click="search()">Cerca</v-btn>
        </v-row>
        </div>
        <v-alert :value="error" type="error" dismissible icon="far fa-frown">
            La tua ricerca non ti ha condotto a nulla di utile
        </v-alert>
        <div class="containerrestcards">
            <div class="title-center">
                <h1>Ristoranti</h1>
                <div class="divider"></div>
                <span class="subt"> Ecco la nostra scelta di ristoranti</span>
            </div>

            <v-skeleton-loader
              :loading="loading"
              transition-group="scale-transition"
              type="table-thead@4"
            >
                <div>
                    <v-row>
                        <v-col v-for="(restaurant, i) in restaurantListData.results" :key="i" cols="12" sm="6" md="4" lg="3">
                            <router-link :to="restaurant.url">
                                <div v-bind="restaurant" >
                                    <div>
                                        <div class="example-2 card">
                                            <div class="wrapper" :style="image(restaurant.image)" >
                                                <div class="header">
                                                    <div class="date">
                                                        <span class="author">{{categoryString(restaurant.restaurant_category)}}</span>
                                                    </div>
                                                    <ul class="menu-content">
                                                            <!--li><a class="fas fa-heart"><span>18</span></a></li-->
                                                    </ul>
                                                </div>
                                                <div class="data">
                                                    <div class="content">
                                                        <h1 class="title"><a>{{restaurant.activity_name}}</a></h1>
                                                        <p class="text">{{restaurant.activity_description}}</p>
                                                        <a class="button">Entra nel negozio</a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </router-link>
                        </v-col>
                    </v-row>
                </div>
            </v-skeleton-loader>
            <v-pagination v-model="pageNumber" total-visible="5" :length="restaurantListData.last" @next="nextPage" @previous="previousPage" @input="goToPage($event)"></v-pagination>
        </div>
    </div>
</template>

<script>
    import {mapActions} from "vuex";
    import axios from 'axios'

    export default {
        name: 'RestaurantCards',

        data: () => ({
            loading: false,
            city: '',
            aperto_ora: false,
            loadingGeo: false,
            query: '',
            restaurant_category: '',
            showAdvancedQuery: false,
            error: false,
        }),
        computed: {
            restaurantListData() {
                return this.$store.getters['restaurants/restaurantList']
            },
            restData() {
                return this.$store.getters['restaurantData/restData']
            },
            pageNumber: {
                get() {return parseInt(this.restaurantListData.page_number, 10);},
                set(value) { this.restaurantListData.page_number =  value}
            },
            restDataCat() {
                return this.$store.getters['restaurantData/restCategories']
            },
            autocomplete() {
                return this.$store.getters['restaurants/autocomplete']
            }
        },
        methods:{
            ...mapActions('restaurants', ['getRestaurants', 'searchRestaurants']),
            categoryString (restaurant_category){
                var categories = ''
                restaurant_category.forEach((cat)=>{
                  categories += cat.category_name + ', '
                })
                return categories.substring(0, categories.length-2);
            },
            image(imgUrl) {
                return {backgroundImage: "url(" + imgUrl + ") "}
            },
            nextPage() {
                if(this.restaurantListData.next) {
                    var payload = {
                        page_number: this.restaurantListData.next,
                        page_size: this.restaurantListData.page_size
                    }
                    this.submit(payload)
                }
            },
            previousPage() {
                if(this.restaurantListData.previous) {
                    var payload = {
                        page_number: this.restaurantListData.previous,
                        page_size: this.restaurantListData.page_size
                    }
                    this.submit(payload)
                }
            },
            goToPage(page) {
                var payload = {
                    page_number: page,
                    page_size: this.restaurantListData.page_size
                }
                this.submit(payload)
            },
            search(){
                var payload = {
                    page_number: this.restaurantListData.page_number,
                    page_size: this.restaurantListData.page_size,
                }
                this.submit(payload)
            },
            submit(payload) {
                this.loading = true

                payload.query= this.query
                payload.city= this.city
                payload.restaurant_category= this.restaurant_category.category_name

                if(this.aperto_ora)
                    payload.aperto_ora = 1

                this.searchRestaurants(payload)
                .then(()=> {
                    this.loading = false
                    this.error = false
                })
                .catch(()=>{
                    this.error = true
                    this.loading = false
                })
            },
            getLocation() {
                this.loadingGeo = true
                var options = { enableHighAccuracy: true, maximumAge: 100, timeout: 10000 };
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(this.getCity,this.locError,options);
                }
                else {
                    console.log("Geolocation is not supported by this browser.")
                    this.loadingGeo = false
                }
            },
            getCity (coordinates) {
                axios
                  .get('https://api.opencagedata.com/geocode/v1/json', {
                      params: {
                          key: '9f6a7dc1ef664052825c045470a06937',
                          language: 'it',
                          q: coordinates.coords.latitude + ',' + coordinates.coords.longitude
                      }
                  })
                  .then((response) => {
                      this.city = response.data.results[0].components.county
                      this.loadingGeo = false
                  }).catch((error)=>{
                      console.log('error')
                      console.log(error)
                      this.loadingGeo = false
                  })
            },
            locError(error){
                console.log('error')
                console.log(error)
                this.loadingGeo = false
            }
        },
        created() {
            this.$store.dispatch("restaurants/getRestaurants", {})
            this.$store.dispatch("restaurantData/getRestCategories")
            this.$store.dispatch("restaurants/getAutocomplete")
        },
    }
</script>
<style scoped>
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        box-sizing: border-box;
    }
    .body {
        /*background: linear-gradient(to bottom, #aaffa9, #11ffbd)!important;*/
        background: var(--whitesmoke);
    }
    .advquery{
        padding: 0px 20px;
    }
    .searchbarcontainer {

        padding: 20px;

    }
    @media screen and (max-width: 992px) {

    }
    .divider {
        width: 50px;
        background: var(--ming);
        height: 5px;
        margin: 10px auto;
        filter: blur(2px);
    }

    .slider {
        width: 50%;
        min-width: 350px;
        align-self: center;
        justify-content: center;
        text-align: center;
    }

    .title-center {
        padding: 10px;
        margin: 10px;
        display: block;
        align-items: center;
        justify-content: center;
        text-align: center;
    }


    .restcard {
        width: 80%;
        max-width: 350px;
        transition: 0.4s;
        margin: auto;
        background: rgba(250,250,250,0) !important;
    }



    .imag {
        box-shadow: 0 10px 4px grey;
        text-shadow: 0 0 2px black;
        border-radius:15px;
        transition: 0.3s ease-in-out;
        opacity: 0.9;
        border: solid 1px darkgrey;
    }
    .restcard:hover > .imag {
        transform: scale(1.05);
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
        font-size: 3em;
        font-weight: 400!important;
    }

    h2 {
        text-transform: capitalize;
        word-break: keep-all;
        font-size: 1.1rem;
        letter-spacing: 1px;

    }
    .description {
        overflow: hidden!important;
        height: 50px;
    }
    .containerrestcards {
        margin-top: 0;
    }


    .card {
        float: left;
        padding: 0 1.7rem;
        width: 100%;
    }
    .card .menu-content {
        margin: 0;
        padding: 0;
        list-style-type: none;
    }
    .card .menu-content::before, .card .menu-content::after {
        content: '';
        display: table;
    }
    .card .menu-content::after {
        clear: both;
    }
    .card .menu-content li {
        display: inline-block;
    }
    .card .menu-content a {
        color: #fff;
    }
    .card .menu-content span {
        position: absolute;
        left: 50%;
        top: 0;
        font-size: 10px;
        font-weight: 700;
        font-family: 'Open Sans';
        -webkit-transform: translate(-50%, 0);
        transform: translate(-50%, 0);
    }
    .card .wrapper {
        background-color: #fff;
        min-height: 380px;
        max-width: 300px;
        position: relative;
        overflow: hidden;
        margin: auto;
        box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3), 0 15px 12px rgba(0, 0, 0, 0.2);
    }
    .card .wrapper:hover .data {
        -webkit-transform: translateY(0);
        transform: translateY(0);
    }
    .card .data {
        position: absolute;
        bottom: 0;
        width: 100%;
        -webkit-transform: translateY(calc(70px + 1em));
        transform: translateY(calc(70px + 1em));
        -webkit-transition: -webkit-transform 0.3s;
        transition: -webkit-transform 0.3s;
        transition: transform 0.3s;
        transition: transform 0.3s, -webkit-transform 0.3s;
    }
    .card .data .content {
        padding: 1em;
        position: relative;
        z-index: 1;
    }
    .card .author {
        font-size: 16px;
        text-transform: capitalize;

    }
    .card .title {
        margin-top: 10px;
        margin-bottom: 5px;
        font-weight: 400;
        font-size: 2rem!important;
        text-shadow:
                0.07em 0 darkslategrey,
                0 0.07em darkslategrey,
                -0.07em 0 darkslategrey,
                0 -0.07em darkslategrey;
    }
    .card .text {
        height: 70px;
        margin: 0;
        background: rgba(0,0,0,0.0);
    }
    .card .header {
        background: rgba(0,0,0,0.3);
    }
    .card input[type='checkbox'] {
        display: none;
    }
    .card input[type='checkbox']:checked + .menu-content {
        -webkit-transform: translateY(-60px);
        transform: translateY(-60px);
    }
    .example-2 .wrapper {
        background: center/cover no-repeat;
    }
    .example-2 .wrapper:hover .menu-content span {
        -webkit-transform: translate(-50%, -10px);
        transform: translate(-50%, -10px);
        opacity: 1;
    }
    .example-2 .wrapper:hover .data div {
        background: rgba(0,0,0,0.5);
        transition: 0.4s ease-in-out;
    }
    .example-2 .wrapper .data div {
        transition: 0.4s ease-in-out;
    }
    .example-2 .header {
        color: #fff;
        padding: 1em;
    }
    .example-2 .header::before, .example-2 .header::after {
        content: '';
        display: table;
    }
    .example-2 .header::after {
        clear: both;
    }
    .example-2 .header .date {
        float: left;
        font-size: 12px;
    }
    .example-2 .menu-content {
        float: right;
    }
    .example-2 .menu-content li {
        margin: 0 5px;
        position: relative;
    }
    .example-2 .menu-content span {
        -webkit-transition: all 0.3s;
        transition: all 0.3s;
        opacity: 0;
    }
    .example-2 .data {
        color: #fff;
        -webkit-transform: translateY(calc(70px + 4.5em));
        transform: translateY(calc(70px + 4.5em));
    }
    .example-2 .title a {
        color: #fff;
    }
    .example-2 .button {
        display: block;
        width: 100px;
        margin: 2em auto 1em;
        text-align: center;
        font-size: 12px;
        color: #fff;
        line-height: 1;
        position: relative;
        font-weight: 700;
    }
    .example-2 .button::after {
        content: '\2192';
        opacity: 0;
        position: absolute;
        right: 0;
        top: 50%;
        -webkit-transform: translate(0, -50%);
        transform: translate(0, -50%);
        -webkit-transition: all 0.3s;
        transition: all 0.3s;
    }
    .example-2 .button:hover::after {
        -webkit-transform: translate(5px, -50%);
        transform: translate(5px, -50%);
        opacity: 1;
    }
</style>
