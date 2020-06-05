<template>
    <v-card class="vetrinacard" width="800" height="auto">
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
            }
        }),
        methods: {
            ...mapActions('restaurantData', ['addMenuEntry', 'deleteMenuEntry', 'editMenuEntry']),
            submitPortata: function (portata) {
                var payload = {
                    data: portata,
                    menuId: this.menu.id
                }
                this.addMenuEntry(payload)
                    .then(
                        this.portataToManage = {
                            name: '',
                            num_products: 1,
                            showAddPortata: false,
                            products: [],
                            edit: false
                        }
                    )//TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore
            },

            deletePortata: function (portata) {
                this.menu.entries.splice(this.menu.entries.indexOf(portata), 1)
                const payload = {menuId: this.menu.id, entryId: portata.id}
                this.deleteMenuEntry(payload) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore
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
                        alert('Portata aggiornata con successo')
                    })
                    .catch((err) => {
                        alert('Errore ' + err)
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

    .addmenu {
        height: auto;
    }
    .addtocart {
        background: var(--ming)!important;
        color: white;
        font-weight: bold;
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
        padding: 5px;
    }
    .euro {
        margin-left: 5px;
    }

</style>