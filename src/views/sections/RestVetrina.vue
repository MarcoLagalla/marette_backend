<template>
  <div class="body" id="Vetrina">
    <h1>Vetrina</h1>
    <v-container>
    <v-row >
      <v-col
        v-for="(item, i) in items2"
        :key="i"
        cols="6"
        md="6"
      >
      <v-card
        color="mx-auto"
        width="800"
        height="800"
      >

          <v-card-title
            class="headline"
            v-text="item.title"
          ></v-card-title>

          <v-card-subtitle v-text="item.artist"></v-card-subtitle>


        <v-card-actions>
          <v-btn color="red">add to cart</v-btn>
        </v-card-actions>

      </v-card>
      </v-col>
    </v-row></v-container>
</div>
</template>

<script>

export default {
  name: "restvetrina",
  data: () => ({

        items2: [
          {
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
  margin: 0!important;
  background: #35302D;
}
h1 {
  color: white;
  text-align: center;
  padding-top: 20px;

}


</style>
