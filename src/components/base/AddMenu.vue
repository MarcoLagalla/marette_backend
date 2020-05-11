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
            <v-btn @click="submitMenu" text>Aggiungi Menù</v-btn>
        </div>
    </v-card>
</template>

<script>

    import {mapActions} from "vuex";

    export default {
        name: "AddMenu",
        data: () => ({
            name: '',
            description: '',
            price: '',
            iva: '',
        }),
        methods: {
            ...mapActions('restaurantData', ['addMenu']),
            submitMenu: function () {
                this.addMenu({
                    name: this.name,
                    description: this.description,
                    price: this.price,
                    iva: this.iva
                }).then(() =>{
                    alert('Menù aggiunto con successo')
                    this.name = ''
                    this.description = ''
                    this.price = ''
                    this.iva = ''
                }).catch((err) =>{
                    alert('Errore ' + err)
                })
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
