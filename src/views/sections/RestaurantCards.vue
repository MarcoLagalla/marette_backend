<template>

    <div class="body">
        <!-- p>{{this.$route.query.code}}</p -->

        <base-section id="">
            <div class="title-center">
                <h1>Ristoranti</h1>
                <div class="divider"></div>
                <span class="subt"> Ecco la nostra scelta di ristoranti</span></div>
                <v-slider class="slider" height="60" label="Ristoranti per pagina:" min="1" max="40" v-model="restaurantListData.page_size" thumb-label="always" @end="changePageSize($event)"></v-slider>
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
                                                        <li><a class="fas fa-heart"><span>18</span></a></li>
                                                </ul>
                                            </div>
                                            <div class="data">
                                                <div class="content">
                                                    <h1 class="title"><a href="#">{{restaurant.activity_name}}</a></h1>
                                                    <p class="text">{{restaurant.activity_description}}</p>
                                                    <a href="#" class="button">Entra nel negozio</a>
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
            <v-pagination v-model="pageNumber" total-visible="5" :length="restaurantListData.last" @next="nextPage" @previous="previousPage" @input="goToPage($event)"></v-pagination>
        </base-section>
    </div>
</template>

<script>
    import {mapActions} from "vuex";

    export default {
        name: 'RestaurantCards',

        data: () => ({
        }),
        computed: {
            restaurantListData() {
                return this.$store.getters['restaurants/restaurantList']
            },
            restData() {
                return this.$store.getters['restaurantData/restData']
            },
            pageNumber() {
                return parseInt(this.restaurantListData.page_number, 10)
            },
        },
        methods:{
            ...mapActions('restaurants', ['getRestaurants']),
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
                if(this.restaurantListData.next)
                    this.getRestaurants({page_number: this.restaurantListData.next, page_size: this.restaurantListData.page_size}) //TODO: aggiungere loading per tutte queste richieste
            },
            previousPage() {
                if(this.restaurantListData.previous)
                    this.getRestaurants({page_number: this.restaurantListData.previous, page_size: this.restaurantListData.page_size})
            },
            goToPage(page) {
                this.getRestaurants({page_number: page, page_size: this.restaurantListData.page_size})
            },
            changePageSize(page_size) {
                this.getRestaurants({page_number: this.restaurantListData.page_number, page_size: page_size})
            },
        },
        created() {
            this.$store.dispatch("restaurants/getRestaurants", {})
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
        font-size: 2em;
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
        font-size: 12px;
        text-transform: capitalize;
        text-shadow: 0 0 1px black;
    }
    .card .title {
        margin-top: 10px;
        margin-bottom: 5px;
        font-weight: 300;
        font-size: 1.6rem!important;
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
