<template>
  <v-card
    class="mx-auto"
    max-width="400"
  >
    <v-img
      class="white--text align-end"
      height="200px"
      src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
    >
      <v-card-title>{{ restaurant.activity_name }}</v-card-title>
    </v-img>

    <v-card-subtitle class="pb-0">Category</v-card-subtitle>

    <v-card-text class="text--primary">
      <div>{{ restaurant.activity_description }}</div>


    </v-card-text>

    <v-card-actions>
      <v-btn
        color="orange"
        text
      >
        Share
      </v-btn>

      <v-btn
        color="orange"
        text
      >
        Explore
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    name: 'BaseCardR',

    data: () => ({

    }),
    computed:
    {
      restaurantList(){
        return this.$store.getters['restaurant/restaurantList']
      }
    },
    created() {
      this.$store.dispatch("restaurant/getRestaurants")
    }
  }
</script>
