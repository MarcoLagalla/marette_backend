<template>
    <v-card class="vetrinacard" max-width="500" height="auto">
        <v-snackbar top v-model="snackbar" :timeout="timeout" :color="color" >{{text}}</v-snackbar>
        <div class="blutitle">
            <v-card-title class="titlemenu" v-text="menu.name"></v-card-title>
            <div class="quant">
                <div v-text="menu.price " ></div>
                <v-icon small class="euro" > fas fa-euro-sign</v-icon>
            </div>
            <v-card-subtitle
                    v-text="menu.description">
            </v-card-subtitle>
        </div>
        <div class="addmenu">

            <base-portata v-for="portata in menu.entries" :key="portata.id" :portata="portata" :admin="admin"
                          @removed="deletePortata(portata)" @edited="askEditPortata(portata)"></base-portata>
            <base-add-portata v-if="admin" :portata="portataToManage"
                              @new_portata="submitPortata($event)"
                              @edit_portata="submitEditPortata($event)"></base-add-portata>
        </div>
        <div class="actions">
            <v-btn v-if="!admin" @click="$emit('added')" class="addtocart">
                Aggiungi al carrello <i class="fas fa-shopping-basket"></i>
            </v-btn>
            <button light name="delete" v-if="admin" @click="$emit('removed')" class="managebutton" text>
                Elimina Menù <i class="fas fa-times"></i>
            </button>

            <button light name="edit" v-if="admin" @click="$emit('edited')" class="managebutton" text>
                Modifica Menù <i class="far fa-edit"></i>
            </button>
        </div>
    </v-card>
</template>

<script>
    import {mapActions} from "vuex";

    export default {
        name: "MenuVetrina",
        props: {
            menu: {
                type: Object,
                required: true
            },
            admin: {
                type: Boolean,
                required: false,
                default: false
            },
        },
        data: () => ({
            portataToManage: {
                name: '',
                num_products: 1,
                showAddPortata: false,
                products: [],
                edit: false
            },
            snackbar: false,
            timeout: 4000,
            color: 'green',
            text: 'Menu aggiornato con successo'
        }),
        methods: {
            ...mapActions('restaurantData', ['addMenuEntry', 'deleteMenuEntry', 'editMenuEntry']),
            submitPortata: function (portata) {
                var payload = {
                    data: portata,
                    menuId: this.menu.id
                }
                this.addMenuEntry(payload)
                    .then(() => {
                        this.portataToManage = {
                            name: '',
                            num_products: 1,
                            showAddPortata: false,
                            products: [],
                            edit: false
                        }
                        this.snackbar = true;
                        this.text = 'Portata aggiunta con successo';
                        this.color = 'green';
                    })
                    .catch((errors) => {
                        this.snackbar = true;
                        var errString = ''
                        for (var key in errors) {
                          // eslint-disable-next-line no-prototype-builtins
                          if (!errors.hasOwnProperty(key)) continue;
                          errString += key + ': ' + errors[key].toString() + ' ';
                        }
                        this.text = 'Errore: ' + errString;
                        this.color = 'error';
                    })
            },

            deletePortata: function (portata) {

                const payload = {menuId: this.menu.id, entryId: portata.id}
                this.deleteMenuEntry(payload)
                .then(() => {
                    this.menu.entries.splice(this.menu.entries.indexOf(portata), 1)
                    this.snackbar = true;
                    this.text = 'Portata eliminata con successo';
                    this.color = 'green';
                })
                .catch((errors) => {
                    this.snackbar = true;
                    var errString = ''
                    for (var key in errors) {
                      // eslint-disable-next-line no-prototype-builtins
                      if (!errors.hasOwnProperty(key)) continue;
                      errString += key + ': ' + errors[key].toString() + ' ';
                    }
                    this.text = 'Errore: ' + errString;
                    this.color = 'error';
                })
            },

            askEditPortata: function (portata) {
                portata.showAddPortata = true
                portata.edit = true
                this.portataToManage = portata
                document.getElementById('AddPortata').scrollIntoView(false)
                document.getElementById('AddPortata').focus({
                    preventScroll: true
                });
            },

            submitEditPortata: function (portata) {
                var payload = {
                    menuId: this.menu.id,
                    entryId: portata.id,
                    data: {
                        name: portata.name,
                        num_products: portata.num_products,
                        products: []
                    }
                }
                portata.products.forEach(function (item) {
                    payload.data.products.push(item.id)
                });

                this.editMenuEntry(payload)
                    .then((newPortata) => {
                        this.menu.entries[this.menu.entries.indexOf(portata)] = newPortata
                        this.snackbar = true;
                        this.text = 'Portata aggiornata con successo';
                        this.color = 'green';
                    })
                    .catch((errors) => {
                        this.snackbar = true;
                        var errString = ''
                        for (var key in errors) {
                          // eslint-disable-next-line no-prototype-builtins
                          if (!errors.hasOwnProperty(key)) continue;
                          errString += key + ': ' + errors[key].toString() + ' ';
                        }
                        this.text = 'Errore: ' + errString;
                        this.color = 'error';
                    })

                this.portataToManage = {
                    name: '',
                    num_products: 1,
                    showAddPortata: false,
                    products: [],
                    edit: false
                }
            },
        }
    }
</script>

<style scoped>
    .vetrinacard {
        margin: 0 auto;
    }

    .addmenu {
        height: auto;
    }
    .addtocart {
        background: var(--ming)!important;
        color: white;
        font-weight: bold;
        margin: 10px;
    }

    h1 {
        color: white;
        text-align: center;
        padding-top: 20px;
    }

    .titlemenu {
        text-transform: uppercase;
        font-size: 1.2em;
    }

    .quant {
        font-weight: bold;
        position: absolute;
        right: 0;
        top: 0;
        margin: 10px;
        display: flex;
        padding: 10px;
        background: var(--ghostwhite);
        border-radius: 15px;
        box-shadow: inset 0 0 4px grey;
    }
    .euro {
        margin-left: 5px;
    }

</style>