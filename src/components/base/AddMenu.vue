<template>
    <div>
    <button v-if="!editOnly" :class="loading?'loading':'openmodaladdmenu'" :disabled="loading" @click="open = !open"><span class="btnmod" v-if="!loading">Nuovo Menu <i class="fas fa-plus fa-1x"></i></span><span v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span> </button>
    <v-dialog ref="addmenu" v-model="open" max-width="500">
    <div id="AddMenu" >
        <div class="blutitle">
            <v-card-title class="titlemenu" v-text="title"></v-card-title>
            <v-card-subtitle
                    v-text="description">
            </v-card-subtitle>
        </div>
        <div class="addmenu">
            <v-text-field outlined v-model='newMenu.name' type="text" label="Nome del menu" required></v-text-field>
            <v-text-field outlined v-model='newMenu.description' type="text" label="Descrizione del menu"></v-text-field>
            <v-text-field outlined v-model='newMenu.price' type="number" label="Prezzo del menu completo"
                          required></v-text-field>
            <v-text-field outlined v-model='newMenu.iva' type="number" label="IVA applicata" required></v-text-field>
            <v-btn class="managebutton"  @click="submitMenu" text><span v-if="!loading">{{submit}}</span><span v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span></v-btn>
            <v-btn class="managebutton" v-if="newMenu.edit" @click="reset" text>Annulla</v-btn>
        </div>
    </div>
    </v-dialog>
    </div>
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
                    edit: false,
                })
            },
            edit: {
                type: Boolean,
                required: false,
                default: false
            },
            editOnly: {
                type: Boolean,
                required: false,
                default: false
            },
        },
        data() {
            return {
                titleNew:'Aggiungi menù',
                titleEdit:'Modifica menù',
                descriptionNew: 'Potrai creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno',
                descriptionEdit: 'Modifica i dati del menù che ti interessano',
                submitNew: 'Aggiungi Menù',
                submitEdit: 'Salva cambiamenti',
                loading: false,
                open: this.menu.edit,
                newMenu: this.menu
            }
        },
        computed: {
          title() {
              return this.newMenu.edit? this.titleEdit : this.titleNew
          },
          description() {
              return this.newMenu.edit? this.descriptionEdit : this.descriptionNew
          },
          submit() {
              return this.newMenu.edit? this.submitEdit : this.submitNew
          },
        },
        methods: {
            submitMenu: function () {
                this.loading=true
                if (this.newMenu.edit)
                    this.$emit('edit_menu', this.newMenu)
                else
                    this.$emit('new_menu', this.newMenu);
                this.loading=false
                this.open = false
                this.reset()
            },
            reset: function () {
                this.newMenu = {
                    name: '',
                    description: '',
                    price: '',
                    iva: '',
                    edit: false
                }
                this.open = false
            },
        },
        updated() {
            if(this.newMenu.edit === true && this.open === false)
                this.reset()
        }
    }
</script>
<style scoped>
    .addmenu {
        padding: 10px !important;
        background: var(--ghostwhite);
    }

    .titlemenu {
        text-transform: uppercase;
        font-size: 1.2em;
    }
    .managebutton {
        color: var(--darkslate);
        font-weight: bold;
    }
    .openmodaladdmenu {
        background: var(--darkslate);
        border-radius: 25px;
        box-shadow: 0 0 4px grey;
        padding: 10px;
        margin: 10px auto;
        transition: 0.3s ease-in-out;
    }
    .openmodaladdmenu:hover {
        transform: scale(1.1);
    }
    .btnmod {
        color: white;
        font-weight: bold;
    }
    .loading {
        background: transparent;
        box-shadow: transparent;
    }
</style>
