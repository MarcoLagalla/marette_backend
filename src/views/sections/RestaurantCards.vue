<template>
<div class="body">
  <base-section id="theme-features">
    <base-section-heading title="Ristoranti" color="red">
      Ecco la nostra scelta di ristoranti
    </base-section-heading>

    <v-container>
      <v-row>
        <v-col v-for="(restaurant, i) in restaurantList" :key="i" cols="12" md="6">
          <router-link :to="restaurant.url">
            <v-card v-bind="restaurant" class="restcard" max-width="400">
              <v-img class="white--text align-end imag" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title><h1>{{ restaurant.activity_name }}</h1></v-card-title>
              </v-img>

              <v-card-text class="text--primary">
                <div>{{ restaurant.activity_description }}</div>
              </v-card-text>
  <v-divider />
              <div class="actions">
                <button class="share">
                  Condividi <v-icon color="orange"> mdi-share-variant </v-icon>
                </button>
                <button class="like">  <v-icon color="orange"> mdi-heart </v-icon></button>
              </div>
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
.actions {
  padding: 10px;
}
.like {
  float: right;
  padding: 10px;
    transition: 0.3s ease-in-out;
  opacity: 0.8;
}
.share {
  font-weight: bold;
  color: orange;
  border-radius: 25px;
  padding: 10px;
  font-size: 1em;
  transition: 0.3s ease-in-out;
}
.share:hover {
  color: darkorange;
  opacity: 1;
}
.shalikere:hover {
  color: darkorange;
  opacity: 1;
}

.restcard {
  box-shadow: 0 0 5px var(--charcoal);
  transition: 0.5s;
}
.restcard:hover {
  box-shadow: 0 0 20px var(--charcoal)
}
.imag {
  box-shadow: 0 2px 2px var(--charcoal);
}
a {
  text-decoration: none
}
</style>
