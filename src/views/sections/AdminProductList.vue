<template>
<div>
  <button @click="getRestaurantData(id)">Patata Lessa</button>
</div>
</template>

<script>
import {
  mapActions
} from "vuex";

export default {
  name: "AdminProductList",

  data() {
    return {
      id: this.$route.params.id
    }
  },
  methods: {
    ...mapActions('restaurantData', ['getRestaurantData']),
  },

  computed: {}
}
</script>

<style scoped>

</style>