<template>
  <div>
    <select v-model="prova">
      <option v-for="category in categories" :key="category" >{{category}}</option>
    </select>
  </div>
</template>

<script>
  export default {
    name: "AddProductToPortata",
    data: () => ({
      prova: ""
    }),
    computed: {
      menu() {
        return this.$store.getters['restaurantData/productList']
      },
      categories() {
        var cat = []
        var men = this.$store.getters['restaurantData/productList']
        Object.keys(men).forEach(function(key) {
          if(men[key].length!==0){
            cat.push(key)
          }
        });
        return cat
      }
    }
  }
</script>

<style scoped>

</style>