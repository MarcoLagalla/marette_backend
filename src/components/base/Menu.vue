<template>
  <div class="menubody">
  <h1>Menu</h1>
  <v-row dense>
          <v-col
            v-for="(item, i) in items"
            :key="i"
            cols="12"
          >
            <v-card
              color="#616161"
              dark
            >
              <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                  <v-card-title
                    class="headline"
                    v-text="item.title"
                  ></v-card-title>

                  <v-card-subtitle v-text="item.artist"></v-card-subtitle>
                </div>

                <v-card-actions>
                  <v-btn color="red">add to cart</v-btn>
                </v-card-actions>
              </div>

            </v-card>
          </v-col>
        </v-row>
          </div>
</template>

<script>
  export default {
    name: 'BaseMenu',

    inheritAttrs: false,

    data: () => ({
          items: [
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
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
            },
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
            },
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
            },
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
            },
            {
              color: '#952175',
              src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
              title: 'Halcyon Days',
              artist: 'Ellie Goulding',
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
h1 {
  color: white;
  margin-bottom:  10px;
  margin-left: 10px;
  
}
.menubody {
  position: relative;
  left: 0;
  top: 0;
  bottom: 0;
  width: 100%;

background: #35302D;
}

</style>
