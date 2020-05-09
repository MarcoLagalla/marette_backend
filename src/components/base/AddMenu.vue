<template>
    <v-card dark width="800" height="800" class="scrollovf">
        <div class="blutitle">
            <v-card-title class="titlemenu" v-text="'Aggiungi menù'"></v-card-title>
            <v-card-subtitle
                    v-text="'Puoi creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno'">
            </v-card-subtitle>
        </div>
        <div class="addmenu">
            <v-text-field outlined v-model='name' type="text" label="Nome del menu" required></v-text-field>
            <v-text-field outlined v-model='description' type="text" label="Descrizione del menu"></v-text-field>
            <v-text-field outlined v-model='price' type="number" label="Prezzo del menu completo"
                          required></v-text-field>
            <v-text-field outlined v-model='iva' type="number" label="IVA applicata" required></v-text-field>
            <base-portata v-for="portata in portate" :key="portata.id" :portata="portata" :delete="true"
                          @removed="deletePortata(portata)"></base-portata>
            <v-btn @click="showAddPortata = true" text>Aggiungi portata</v-btn>
            <base-add-portata v-show="showAddPortata" @added_portata="submitPortata($event)"></base-add-portata>
            <v-btn @click="submitMenu" :disabled="portate.length===0" text>Salva Menu</v-btn>
        </div>
    </v-card>
</template>

<script>

    import {mapActions} from "vuex";

    export default {
        name: "AddMenu",
        data: () => ({
            portate: [],
            name: '',
            description: '',
            price: '',
            iva: '',
            showAddPortata: false
        }),
        methods: {
            ...mapActions('restaurantData', ['addMenuEntry', 'deleteMenuEntry']),
            submitPortata: function (portata) {
                this.showAddPortata = false
                this.portate.push(portata)
                var payload = {
                    name: portata.name,
                    num_products: portata.num_products,
                    products: []
                }
                portata.products.forEach(function (item) {
                    payload.products.push(item.id)
                });
                var id
                this.addMenuEntry(payload).then(function (resp) {
                    id = resp.id
                }) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore

                this.portate[this.portate.indexOf(portata)].id = id
            },
            deletePortata: function (portata) {
                this.portate.splice(this.portate.indexOf(portata), 1)
                this.deleteMenuEntry(portata.id) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore
            },
            submitMenu: function () {

            }
        }
    }
</script>
<style scoped>
    .addmenu {
        padding: 10px !important;
        background: var(--charcoal);
    }

    .blutitle {
        background: var(--ming);
        color: #FFFFFF;
        box-shadow: 0 0 5px black;
        position: sticky;
        top: 0;
        z-index: 1;
    }

    .scrollovf {
        overflow: scroll;
        box-shadow: 0 0 10px var(--charcoal);
        background: var(--whitesmoke);
    }

    .titlemenu {
        text-transform: uppercase;
        font-size: 1.2em;
    }
</style>
