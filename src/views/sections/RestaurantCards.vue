<template>
  <base-section id="theme-features">
    <base-section-heading title="Ristoranti">
     Ecco la nostra scelta di ristoranti
    </base-section-heading>

    <v-container>
      <v-row>
        <v-col
          v-for="(restaurant, i) in restaurantList"
          :key="i"
          cols="12"
          md="6"
        >
          <base-avatar-card
            v-bind="restaurant"
            align="left"
            horizontal
            size="96"
          >
            {{ restaurant.activity_description}}
          </base-avatar-card>
        </v-col>
      </v-row>
    </v-container>
  </base-section>
</template>

<script>
  export default {
    name: 'RestaurantCards',

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
