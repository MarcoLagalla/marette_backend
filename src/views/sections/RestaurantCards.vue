<template>
<div class="body">
  <base-section id="theme-features">
    <base-section-heading title="Ristoranti">
      Ecco la nostra scelta di ristoranti
    </base-section-heading>

    <v-container>
      <v-row>
        <v-col v-for="(restaurant, i) in restaurantList" :key="i" cols="12" md="6">
          <router-link :to="restaurant.url">
            <v-card v-bind="restaurant" class="mx-auto" max-width="400">
              <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title>{{ restaurant.activity_name }}</v-card-title>
              </v-img>

              <v-card-subtitle class="pb-0">Category</v-card-subtitle>

              <v-card-text class="text--primary">
                <div>{{ restaurant.activity_description }}</div>


              </v-card-text>

              <v-card-actions>
                <v-btn color="orange" text>
                  Condividi
                </v-btn>
              </v-card-actions>
            </v-card>
          </router-link>
        </v-col>
      </v-row>
    </v-container>
  </base-section>
</div>
</template>

<script>
export default {
  name: 'RestaurantCards',

  data: () => ({

  }),
  computed: {
    restaurantList() {
      return this.$store.getters['restaurants/restaurantList']
    }
  },
  created() {
    this.$store.dispatch("restaurants/getRestaurants")
  }
}
</script>
<style scoped>
.body {
  /*background: linear-gradient(to bottom, #aaffa9, #11ffbd)!important;*/
  background: #f1f1f1;
}

a {
  text-decoration: none
}
</style>
