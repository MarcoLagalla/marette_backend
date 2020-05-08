<template>
  <div class="body" id="VETRINA">
    <base-rest-h1> Vetrina </base-rest-h1>
    <v-container>
      <v-row>
        <v-col  cols="6" md="6">
          <base-add-menu></base-add-menu>
        </v-col>
        <v-col v-for="(item, i) in items2" :key="i" cols="6" md="6">
          <v-card  color="vetrinacard" width="800" height="800">
            <v-card-title class="headline" v-text="item.title"></v-card-title>
            <v-card-subtitle v-text="item.artist"></v-card-subtitle>
            <v-card-actions>
              <v-btn color="red" class="addtocart">add to cart</v-btn>
            </v-card-actions>
          </v-card>

        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "restvetrina",
  data: () => ({
        items2: [{
              color: '#1F7087',
              src: 'https://cdn.vuetifyjs.com/images/cards/foster.jpg',
              title: 'Supermodel',
              artist: 'Foster the People',
            },
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
            },
        ],
    }),

}
</script>

<style scoped>
.body {
  margin: 0 !important;
  background: var(--whitesmoke);
}
h1 {
  color: white;
  text-align: center;
  padding-top: 20px;
}
.addtocart {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
  .vetrinacard {
    box-shadow: 0 0 10px var(--charcoal);

  }
</style>
