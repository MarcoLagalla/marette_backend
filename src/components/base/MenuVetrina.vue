<template>
  <v-card dark width="800" height="800" class="scrollovf">
    <div class="blutitle">
      <v-card-title class="titlemenu" v-text="menu.name"></v-card-title>
      <v-card-subtitle
              v-text="menu.description">
      </v-card-subtitle>
    </div>
    <div class="addmenu">
      <base-portata v-for="portata in menu.portate" :key="portata.id" :portata="portata" :delete="admin"
                    @removed="deletePortata(portata)"></base-portata>
      <template v-if="admin">
        <v-btn @click="showAddPortata = true" text>Aggiungi portata</v-btn>
        <base-add-portata v-show="showAddPortata" @added_portata="submitPortata($event)"></base-add-portata>
      </template>
    </div>
    <v-card-actions>
      <button v-if="!admin" @click="$emit('added')" class="addtocart">Aggiungi al carrello <i class="fas fa-shopping-basket"></i></button>
    </v-card-actions>
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
            basket: {
              type: Boolean,
              required: false,
              default: true
            },
            admin: {
              type: Boolean,
              required: false,
              default: false
            },
        },
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
        }
    }
</script>

<style scoped>

.addtocart {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: var(--chilli);
  padding: 10px;
  color: white;
  border-radius: 25px;
  border: inset 2px var(--chilli);
  font-weight: bold;
}

</style>