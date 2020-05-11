<template>
    <v-card dark width="800" height="800" class="scrollovf">
        <div class="blutitle">
            <v-card-title class="titlemenu" v-text="title"></v-card-title>
            <v-card-subtitle
                    v-text="description">
            </v-card-subtitle>
        </div>
        <div class="addmenu">
            <v-text-field outlined v-model='menu.name' type="text" label="Nome del menu" required></v-text-field>
            <v-text-field outlined v-model='menu.description' type="text" label="Descrizione del menu"></v-text-field>
            <v-text-field outlined v-model='menu.price' type="number" label="Prezzo del menu completo"
                          required></v-text-field>
            <v-text-field outlined v-model='menu.iva' type="number" label="IVA applicata" required></v-text-field>
            <v-btn @click="submitMenu" text>{{submit}}</v-btn>
        </div>
    </v-card>
</template>

<script>

    export default {
        name: "AddMenu",
        props: {
            menu: {
                type: Object,
                required: false,
                default:() => ({
                    name: '',
                    description: '',
                    price: '',
                    iva: '',
                    edit: false
                })
            },
        },
        data: () => ({
            titleNew:'Aggiungi menù',
            titleEdit:'Modifica menù',
            descriptionNew: 'Potrai creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno',
            descriptionEdit: 'Modifica i dati del menù che ti interessano',
            submitNew: 'Aggiungi Menù',
            submitEdit: 'Salva cambiamenti'
        }),
        computed: {
          title() {
              return this.menu.edit? this.titleEdit : this.titleNew
          },
          description() {
              return this.menu.edit? this.descriptionEdit : this.descriptionNew
          },
          submit() {
              return this.menu.edit? this.submitEdit : this.submitNew
          },
        },
        methods: {
            submitMenu: function () {
                this.$emit('new_menu', this.menu)
                this.menu = {
                    name: '',
                    description: '',
                    price: '',
                    iva: '',
                    edit: false
                }
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
