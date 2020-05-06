<template>
  <v-card color="mx-auto" width="800" height="800">
    <v-card-title class="headline" v-text="'Aggiungi menù'"></v-card-title>
    <v-card-subtitle
            v-text="'Puoi creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno'">
    </v-card-subtitle>
    <v-btn @click="show = !show" text>Modifica password<v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "BaseRestVetrinaAddMenu",
  data: () => ({
  }),
}
</script>
<style scoped>

</style>
