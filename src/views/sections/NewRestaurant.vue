<template>
    <div v-if="hasPermission" class="background">
        <v-container>
            <button v-if="$vuetify.breakpoint.mdAndUp" class="shownr" @click="show = !show">Aggiungi Ristorante
                <v-icon :class="[ show ? 'rotated' : 'normal']">fas fa-plus</v-icon>
            </button>
            <button v-if="$vuetify.breakpoint.smAndDown" class="shownr" @click="show = !show">
                <v-icon x-large :class="[ show ? 'rotated' : 'normal']">fas fa-plus</v-icon>
            </button>
            <v-row dense>
                <v-col cols="12">
                    <v-expand-transition>
                        <div v-show="show">
                            <v-card>
                                <v-toolbar flat class="profilctool" dark>
                                    <v-toolbar-title>
                                        Nuovo Locale
                                    </v-toolbar-title>
                                </v-toolbar>
                                <div class="body">
                                    <v-row align="center" class="mx-0 pa-8" justify="center">
                                        <v-col cols="12">

                                            <form @submit.prevent="register" class="px-8">
                                                <p class="error" v-if="errors" id="detail">{{errors.detail}}</p>
                                                <v-col class="center">
                                                    <v-row align="center" class="ma-0" justify="center">
                                                        <v-col cols="12">
                                                            <v-row>
                                                                <v-col cols="12" md="6">
                                                                    <div class="picinput">
                                                                <picture-input
                                                                        v-if="show"
                                                                        ref="restImage"
                                                                        @change="onChanged"
                                                                        @remove="onRemoved"
                                                                        :width="200"
                                                                        :height="200"
                                                                        size="3"
                                                                        :zIndex="0"
                                                                        :crop="true"
                                                                        :changeOnClick="false"
                                                                        :removable="true"
                                                                        accept="image/jpeg, image/png, image/gif"
                                                                        buttonClass="ui button primary"
                                                                        :customStrings="{
                                                                            upload: '<h1>Carica immagine</h1>',
                                                                            drag: 'Trascina qui la un immagine del ristorante o clicca per selezionarla',
                                                                            change: 'Cambia foto',
                                                                            remove: 'Elimina foto',
                                                                        }">
                                                                </picture-input>
                                                                    </div>
                                                                </v-col>
                                                                <v-col cols="12" md="6">
                                                                <v-text-field label="Nome del locale*"
                                                                    :error-messages="errors.activity_name"
                                                                    @change="errors.activity_name=''"
                                                                    v-model='activity_name'
                                                                    :rules="rules"
                                                                    counter="30"
                                                                    type="text" id="activity_name"
                                                                    name="activity_name"
                                                                    required></v-text-field>

                                                                <v-combobox
                                                                    :error-messages="errors.restaurant_category"
                                                                    :items="restDataCat"
                                                                    item-text="category_name"
                                                                    item-value="id"
                                                                    @change="errors.restaurant_category=''"
                                                                    v-model='restaurant_category'
                                                                    id="restaurant_category"
                                                                    name="restaurant_category"
                                                                    multiple chips
                                                                    label="Categorie del locale*"

                                                                ></v-combobox>
                                                                </v-col>
                                                            </v-row>

                                                        </v-col>
                                                        <v-textarea outlined
                                                                    label="Fornisci una breve descrizione del locale*"
                                                                    :error-messages="errors.activity_description"
                                                                    @change="errors.activity_description=''"
                                                                    v-model='activity_description'
                                                                    id="activity_description" rows="3"
                                                                    cols="80"
                                                                    name="activity_description" required></v-textarea>
                                                    </v-row>
                                                    <v-row align="center" class="ma-0" justify="center">
                                                        <v-text-field label="Città in cui è locata l'attività*"
                                                                      :error-messages="errors.city"
                                                                      @change="errors.city=''"
                                                                      v-model='city' type="text" id="city" name="psw"
                                                                      required></v-text-field>
                                                        <v-text-field label="Indirizzo del locale*"
                                                                      :error-messages="errors.address"
                                                                      @change="errors.address=''" v-model='address'
                                                                      type="text"
                                                                      id="address" name="address"
                                                                      required></v-text-field>
                                                    </v-row>
                                                    <v-row align="center" class="ma-0" justify="center">
                                                        <v-text-field label="Numero civico*"
                                                                      :error-messages="errors.n_civ"
                                                                      @change="errors.n_civ=''" v-model='n_civ'
                                                                      type="text" id="n_civ"
                                                                      name="n_civ" required></v-text-field>
                                                        <v-text-field label="CAP del locale*"
                                                                      :error-messages="errors.cap"
                                                                      @change="errors.cap=''" v-model='cap'
                                                                      type="number" id="cap"
                                                                      name="cap" required></v-text-field>
                                                    </v-row>
                                                    <v-row align="center" class="ma-0" justify="center">
                                                        <v-text-field label="Numero di Telefono valido del locale*"
                                                                      :error-messages="errors.restaurant_number"
                                                                      @change="errors.restaurant_number=''"
                                                                      v-model='restaurant_number'
                                                                      type="tel" id="restaurant_number"
                                                                      name="restaurant_number"
                                                                      required>
                                                        </v-text-field>
                                                        <v-text-field label="Partita iva associata al locale*"
                                                                      :error-messages="errors.p_iva"
                                                                      @change="errors.p_iva=''"
                                                                      v-model='p_iva' type="number" id="p_iva"
                                                                      name="p_iva"
                                                                      required></v-text-field>
                                                    </v-row>
                                                    <v-row align="center" class="ma-0" justify="center">

                                                    </v-row>
                                                </v-col>
                                                <button type="submit" :disabled="loading" :class="[loading?'loadbtn':'managebutton2']">
                                                    <span v-if="!loading">Conferma</span>
                                                    <span v-if="loading"> <div class="spinner">
                                                        <div class="rect1"></div>
                                                         <div class="rect2"></div>
                                                      <div class="rect3"></div>
                                                      <div class="rect4"></div>
                                                    <div class="rect5"></div>
                                                    </div></span>
                                                </button>
                                            </form>

                                        </v-col>
                                    </v-row>
                                </div>

                            </v-card>
                        </div>
                    </v-expand-transition>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>
<script>
    import {
        mapActions
    } from 'vuex'
    import PictureInput from "vue-picture-input";

    export default {
        name: "NewRestaurant",
        components: {
            PictureInput,
        },
        data() {
            return {
                activity_name: '',
                activity_description: '',
                city: '',
                address: '',
                n_civ: '',
                cap: '',
                restaurant_number: '',
                restaurant_category: '',
                p_iva: '',
                image: '',
                show: false,
                loading: false,
                rules: [v => v.length <= 30 || 'Max 30 characters']
            }
        },
        methods: {
            ...mapActions('restaurants', ['newRestaurant']),
            ...mapActions('restaurantData', ['getRestCategories']),
            register: function () {
                this.loading = true
                const data = {
                    activity_name: this.activity_name,
                    activity_description: this.activity_description,
                    restaurant_category: [],
                    city: this.city,
                    address: this.address,
                    n_civ: this.n_civ,
                    cap: this.cap,
                    restaurant_number: this.restaurant_number,
                    p_iva: this.p_iva
                };

                this.restaurant_category.forEach((category)=>{
                    data.restaurant_category.push(category.id)
                })

                const formData = new FormData();
                formData.append('image', this.image);
                formData.append('data', JSON.stringify(data));


                this.newRestaurant(formData)
                    .then((response) => {
                        this.$router.push('/profile/' + response.id_restaurant + '/' + response.slug)
                        this.loading = false
                    })
                    .catch(error => {
                        console.log('error')
                        console.log(error)
                        var id = Object.keys(error)[0];
                        document.getElementById(id).scrollIntoView(false)
                        document.getElementById(id).focus({
                            preventScroll: true
                        });
                        this.loading = false
                    })

            },

            onChanged() {
                if (this.$refs.restImage.file) {
                    this.image = this.$refs.restImage.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },

            onRemoved() {
                this.image = '';
            },
            checkCategories(){
                if(this.$store.getters["restaurantData/restCategories"]){
                    return this.$store.getters["restaurantData/restCategories"];
                }
                else {
                    setTimeout(this.checkCategories, 200); // check again in a second
                }
            },

        },
        computed: {
            errors() {
                return this.$store.getters['restaurants/errors']
            },
            hasPermission() {
                return this.$store.getters['userProfile/user_private'].email_activated && this.$store.getters['userProfile/isBusiness']
            },
            restDataCat() {
                return this.$store.getters['restaurantData/restCategories']
            }

        },

        created() {
          this.$store.dispatch("restaurantData/getRestCategories")
        }
    }
</script>
<style scoped>

    @media only screen and (min-width: 1000px) {
        .center {
            width: 80%;
            margin: auto;
        }
    }

    .shownr {
        position: fixed;
        right: 0;
        bottom: 0;
        padding: 10px;
        border-radius: 25px;
        border: 4px inset var(--darkslate);
        margin: 10px;
        font-weight: bold;
        z-index: 200;
        color: white;
        background: var(--darkslate);
        transition: ease-in-out 0.3s;
    }

    .background {
        background-color: var(--whitesmoke) !important;
    }

    .body {
        background-color: whitesmoke;
        text-align: center;
        padding: 0;
    }

    h1 {
        color: var(--darkslate)
    }

    .v-text-field {
        padding: 10px;
    }
    /* Add a blue text color to links */
    a {
        color: dodgerblue;
    }

    .profilctool {
        background: var(--ming) !important;
    }

    .normal {
        transition: ease-in-out 0.2s;
        color: white;
    }

    .rotated {
        transition: ease-in-out 0.2s;
        color: white;
        transform: rotate(45deg);
    }

    .picture-input {
        padding: 0;
        border: 1px solid black;
    }
    .picinput {
        width: 200px;
        margin-left: 0;
    }


</style>
