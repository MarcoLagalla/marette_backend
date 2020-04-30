<template>
  <div>
    <v-form>
      <v-text-field solo background-color="#486F83" v-model='name' type="text" placeholder=" Inserire nome prodotto" id="name" name="name" required></v-text-field>
      <v-text-field solo background-color="#486F83" v-model='description' type="text" placeholder=" Inserire descrizione" id="description" name="description" required></v-text-field>
      <v-text-field solo background-color="#486F83" v-model='price' type="text" placeholder=" Inserire prezzo" id="price" name="price" required></v-text-field>
      <button type="button">Aggiungi Prodotto</button>
    </v-form>
  </div>
</template>
<script>
export default {
  name: "AddProduct",
  props: 'category',
  data() {
    return {
        name: '',
        description: '',
        category: '',
        price: ''
    }
  },
  computed: {
    food_category_choice() {
      return this.$store.getters['manageRestaurant/food_category_choice']
    }
  }
}
</script>
<style scoped>
</style>