<template>
    <div>
    <button :class="loading?'loading':'openmodaladdmenu'" :disabled="loading" @click="toggleMenuModal"><span class="btnmod" v-if="!loading">Nuovo Menu <i class="fas fa-plus fa-1x"></i></span><span v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span> </button>
    <sweet-modal ref="addmenu">
    <div id="AddMenu" width="800" max-height="800" class="">
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
            <v-btn class="managebutton"  @click="submitMenu" text><span v-if="!loading">{{submit}}</span><span v-if="loading"><i class="fas fa-cog fa-2x fa-spin"></i></span></v-btn>
            <v-btn class="managebutton" v-if="menu.edit" @click="reset" text>Annulla</v-btn>
        </div>
    </div>
    </sweet-modal>
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
        },
        data: () => ({
            titleNew:'Aggiungi menù',
            titleEdit:'Modifica menù',
            descriptionNew: 'Potrai creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno',
            descriptionEdit: 'Modifica i dati del menù che ti interessano',
            submitNew: 'Aggiungi Menù',
            submitEdit: 'Salva cambiamenti',
            loading: false,
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
                this.loading=true
                if (this.menu.edit)
                    this.$emit('edit_menu', this.menu)
                else
                    this.$emit('new_menu', this.menu);
                this.loading=false
            },
            reset: function () {
                this.menu = {
                    name: '',
                    description: '',
                    price: '',
                    iva: '',
                    edit: false
                }
            },
            toggleMenuModal() {
                this.$refs.addmenu.open()
            },
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
        box-shadow: 0 0 2px lightgrey;
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
