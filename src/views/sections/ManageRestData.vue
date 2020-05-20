<template>
    <div class="box">
        <form @submit.prevent="update">
            <v-row dense>
                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Nome del locale'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.activity_name"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show">
                                            <v-text-field solo class="description" v-model='restData.activity_name'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show = !show" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Descrizione del locale'"></v-card-title>
                                    <v-card-subtitle class="pb-0"
                                                     v-text="restData.activity_description"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show0">
                                            <v-text-field solo class="description"
                                                          v-model='restData.activity_description'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show0 = !show0" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Città'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.city"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show1">
                                            <v-text-field solo class="description" v-model='restData.city'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show1 = !show1" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Indirizzo'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.address"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show2">
                                            <v-text-field solo class="description" v-model='restData.address'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show2 = !show2" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Numero civico'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.n_civ"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show3">
                                            <v-text-field solo class="description" v-model='restData.n_civ'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show3 = !show3" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Cap'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.cap"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show4">
                                            <v-text-field solo class="description" v-model='restData.cap'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show4 = !show4" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Numero di telefono'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.restaurant_number"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show5">
                                            <v-text-field solo class="description" v-model='restData.restaurant_number'
                                                          type="tel"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show5 = !show5" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="6">
                    <v-card color="var(--ming)" dark class="product">
                        <div class="d-flex flex-no-wrap justify-space-between">
                            <div class="quant">
                                <div class>
                                    <v-card-title class="headline" v-text="'Partita IVA'"></v-card-title>
                                    <v-card-subtitle class="pb-0" v-text="restData.p_iva"></v-card-subtitle>
                                    <v-expand-transition>
                                        <div v-show="show6">
                                            <v-text-field solo class="description" v-model='restData.p_iva'
                                                          type="text"></v-text-field>
                                        </div>
                                    </v-expand-transition>
                                </div>
                            </div>
                            <v-card-actions class="pos1">
                                <v-btn @click="show6 = !show6" color="red" class="addtocart">
                                    <i class="fas fa-pencil-alt"></i>
                                </v-btn>
                            </v-card-actions>
                        </div>
                    </v-card>
                </v-col>

                <v-col cols="12" md="3">

                        <img class="profimg" ref="restImageOld" :src="restData.image">

                </v-col>
                <v-col cols="12" md="3"></v-col>
                <v-col cols="12" md="6">

                <picture-input
                        ref="restImage"
                        @change="onChanged"
                        :width="300"
                        :height="300"
                        size="5"
                        zIndex="0"
                        :crop="true"
                        :changeOnClick="false"
                        accept="image/jpeg, image/png, image/gif"
                        buttonClass="ui button primary"
                        :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine del ristorante o clicca per selezionarla'}">
                </picture-input>
                </v-col>
            </v-row>
            <div class="center">
                <div class="centerbut">
                    <button type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import {mapActions} from "vuex";
    import PictureInput from "vue-picture-input";

    export default {
        name: "ManageRestData",
        components: {
            PictureInput,
        },
        data() {
            return {
                show: false,
                show0: false,
                show1: false,
                show2: false,
                show3: false,
                show4: false,
                show5: false,
                show6: false,
                id: this.$route.params.id,
                image: ''
            }
        },
        computed: {
            restData() {
                return this.$store.getters["restaurantData/restData"];
            }
        },
        methods: {
            ...mapActions('restaurants', ['updateRestaurant']),
            update: function () {
                const data = {
                    activity_name: this.restData.activity_name,
                    activity_description: this.restData.activity_description,
                    city: this.restData.city,
                    address: this.restData.address,
                    n_civ: this.restData.n_civ,
                    cap: this.restData.cap,
                    restaurant_number: this.restData.restaurant_number,
                    p_iva: this.restData.p_iva,
                };

                if (!this.image) {
                    this.image = this.$refs.restImageOld.file
                }

                const formData = new FormData();
                formData.append('image', this.image);
                formData.append('data', JSON.stringify(data));

                this.updateRestaurant(formData) //TODO: far apparire un banner dati modificati con successo, gestire errori, aggiornare immagine quando cambia e far tornare le cose chiuse dopo aver salvato
            },

            onChanged() {
                if (this.$refs.restImage.file) {
                    this.image = this.$refs.restImage.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },
        },
    };
</script>

<style scoped>
    .box {
        margin: 2vmax;
        padding: 4vmax;
        border: solid var(--charcoal) 1px;
        box-shadow: 0 0 10px inset black;
        border-radius: 25px;
        margin-left: 10vmax;
        margin-right: 10vmax;
        background: var(--whitesmoke);
    }
    @media only screen and (max-width: 768px) {
        /* For mobile phones: */
        .product {
            width: 100%;
            margin: 0;
        }
        .quant {
            margin: 5%;
        }
        .box {
            margin: 5%;
            padding: 5%;
        }
        .headline {
            font-size: 1.1em!important;
            letter-spacing: normal!important;
        }
    }
    .product {
    }
    .profimg {
        margin: auto;
        width: 100%;
        height: auto;
    }
    .center {
        margin: auto;
    }

    .centerbut {
        margin: auto;
        width: auto;
    }

    .save {
        padding: 10px;
        border-radius: 25px;
        background: var(--darkslate);
        margin: auto;
        color: aliceblue;
        font-weight: bold;
        font-size: 1.5em;
        box-shadow: 0 0 4px var(--darkslate);
        transition: ease-in-out 0.5s;
        width: auto;
    }

    .save:hover {
        box-shadow: 0 0 10px var(--darkslate);
    }

    .description {
        padding: 10px;;
    }

    .addtocart {
        background: var(--darkslate) !important;
    }
</style>