<template>
  <div class="portata">
    <v-card-title class="headline" v-text="portata.name"></v-card-title>
    <v-card-subtitle v-text="'Puoi scegliere ' + portata.num_products + ' di questi prodotti:'"> </v-card-subtitle>
    <div class="portate" v-for="product in portata.products" :key="product.id">
    <base-portata-product :portata="portata.name" :product="product"></base-portata-product>
    </div>
    <div class="actions">
      <button name="delete" v-if="admin" class="manageportata" @click="$emit('removed')" text>
        Elimina portata <i class="fas fa-times"></i>
      </button>
      <button name="edit" v-if="admin" class="manageportata" @click="$emit('edited')" text>
        Modifica portata <i class="far fa-edit"></i>
      </button>
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
  background: var(--ghostwhite)!important;
}
  .portate {
    margin: 10px;
  }
 .manageportata {
   padding: 10px;
   margin: 10px;
   color: var(--ming);
   background: transparent;
 }
</style>