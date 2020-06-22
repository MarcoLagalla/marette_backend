<template>
    <div class="infocard">
        <v-snackbar top v-model="snackbar" :timeout="timeout" :color="color">{{text}}</v-snackbar>
        <div class="namecontainer"><h1>{{name}}</h1></div>
        <div class="divider"></div>
        <v-textarea auto-grow class="descript" :rounded="!admin"
                    :placeholder='admin? "Inserisci una introduzione al locale" : ""' dark :readonly='!admin'
                    @input="edited= true" v-model="activity_description"></v-textarea>
        <v-btn class="pd" v-if="admin" name="edit" :disabled="!edited" color="blue" @click="edit" text>
            Modifica descrizione <v-icon small> fas fa-pencil-alt</v-icon>
        </v-btn>
        <button class="infoicon" v-if="!admin" @click="$refs.orarimodal.open()">
            <i class="far fa-calendar-alt"> </i> <span v-if="$vuetify.breakpoint.mdAndUp">Orari di apertura</span>
        </button>
        <base-add-time-table v-if="admin"></base-add-time-table>

        <sweet-modal ref="orarimodal">
            <base-orari></base-orari>
        </sweet-modal>
        <ul class="orari">
            <li class="infos">
                {{categoryString}}
            </li>
            <li class="infos">
                :
            </li>
            <li class="infos" >
                {{ opened }} <span v-if="opened_now === false && opens_at != false">- {{ opens_at }} </span>
            </li>
        </ul>
    </div>
</template>
<script>
    export default {
        props: {
            opened_now: {
                type: Boolean,
                required: true,
            },
            opens_at: {
                type: String,
                required: true,
            },
            name: {
                type: String,
                required: true,
            },
            category: {
                type: Array,
                required: true,
            },
            description: {
                type: String,
                required: false,
                default: ''
            },
            admin: {
                type: Boolean,
                default: false,
            }
        },
        name: "NameRestCard",
        data: function () {
            return {
                edited: false,
                activity_description: this.description,
                snackbar: false,
                timeout: 4000,
                color: 'green',
                text: 'Descrizione aggiornata con successo'
            }
        },
        methods: {
            edit: function () {
                this.edited = false
                this.snackbar = true
                this.$emit('edited', this.activity_description)
            },
        },
        computed: {
            categoryString() {
                var categories = ''
                this.category.forEach((cat) => {
                    categories += cat.category_name + ', '
                })
                return categories.substring(0, categories.length - 2);
            },
            opened() {
                if (this.opened_now) {
                    return "Aperto";
                } else {
                    return "Chiuso";
                }
            },
        },
    }
</script>
<style scoped>
    .namecontainer {
        width: 80%;
    }
    .divider {
        width: 100px;
        background: var(--ming);
        height: 5px;
        margin: 20px 0;
        filter: blur(2px);
    }

    h1 {
        font-size: 1.5em;
        text-transform: capitalize;
        color: white;
        margin: 1vmax 0;
    }

    .infocard {
        position: relative;
        background: rgba(0, 0, 0, 0.4);
        padding: 1vmax;
        display: block;
        width: 100%;
        height: 400px;
        box-shadow: 0 0 10px black;
    }

    .descript {
        width: 90%;
        font-size: 0.8em;
        overflow: hidden;
        color: white;
    }

    .orari {
        position: absolute;
        bottom: 0;
        left: 0;
        margin: 10px;
        list-style-type: none;
        text-align: left;
        padding: 0;
    }

    .orari li {
        color: white;
        display: inline-block;
        font-size: 15px;
        padding: 10px;
    }

    .infoicon {
        position: absolute;
        top: 0;
        right: 0;
        margin: 10px;
        color: white;
        transition: 0.4s ease-in-out;
    }

    .infoicon:hover {
        color: limegreen;
    }

    i {
        font-size: 30px;
    }
</style>
