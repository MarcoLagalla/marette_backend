<template>
  <div class="portata">
    <v-card-title class="headline" v-text="portata.name"></v-card-title>
    <v-card-subtitle v-text="'Puoi scegliere ' + portata.num_products + ' di questi prodotti:'"> </v-card-subtitle>
    <div class="portate" v-for="product in portata.products" :key="product.id">
    <base-portata-product :product="product"></base-portata-product>
    </div>
    <div class="actions">
      <v-btn name="delete" v-if="admin" color="white" @click="$emit('removed')" class="managebutton">
        Elimina portata<i class="fas fa-times"></i>
      </v-btn>
      <v-btn name="edit" v-if="admin" color="white" @click="$emit('edited')" class="managebutton">
        Modifica portata<i class="far fa-edit"></i>
      </v-btn>
    </div>
  </div>
</template>

<script>
    export default {
        name: "Portata",
        props:{
          portata: {
            type: Object,
            required: true
          },
          admin: {
            type: Boolean,
            required: false,
            default: false
          },
        },
    }
</script>

<style scoped>
.portata {
  background: var(--darkslate)!important;
}
  .portate {
    margin: 10px;
  }
  .managebutton {
    color: #1a1a1a!important;
    background: aliceblue!important;
    margin: 5px;
  }
</style>