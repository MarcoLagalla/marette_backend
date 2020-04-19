<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    bottom
    left
    max-width="90%"
    min-width="275"
    offset-x
    offset-y
    origin="top right"
    transition="scale-transition"
  >
    <template v-slot:activator="{ attrs, on }">
      <v-card
        id="settings"
        class="py-2 px-4"
        color="#ffffff8D"
        dark
        flat
        style="position: fixed; top: 164px; right: -35px;"
        width="100"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon
        color="blue"
        large>
          mdi-account
        </v-icon>
      </v-card>
    </template>

    <v-card
     class="py-2">
     <router-link :to="{ name: 'profile'}">
      <div class="text-center">
        <div class="title1"
        >
          Profilo


        </div>
      </div></router-link>
      <v-card-text>
    <!--    <v-item-group
          v-model="$vuetify.theme.themes.light.primary"
          class="d-flex justify-center"
        >
          <v-item
            v-for="color in colors"
            :key="color"
            :value="color"
          >
            <template v-slot="{ active, toggle }">
              <base-avatar
                :color="color"
                :outlined="active"
                class="ma-2"
                size="48"
                style="cursor: pointer;"
                @click.stop="toggle"
              />
            </template>
          </v-item>
        </v-item-group> -->

        <v-divider class="mb-6" />


        <base-btn
          block
          href="#"
          class="mb-6"
          color="accent"
          target="_blank"
        >
          Prenotazioni
        </base-btn>




        <v-divider class="my-6" />



        <div class="text-center">
          <base-btn
            :tile="false"
            :to="{ name: 'Pro' }"
            rounded
            @click="menu = false"
          >
            I tuoi ristoranti

            <v-icon right>
              mdi-food-fork-drink
            </v-icon>
          </base-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
  export default {
    name: 'HomeSettings',

    data () {
      return {
        colors: [
          this.$vuetify.theme.themes.light.primary,
          '#9368e9',
          '#F4511E',
        ],
        menu: false,
      }
    },
  }
</script>

<style scoped>
  .title1{
    background: rgba(200,20,20,0.7);
    color: white;
    text-align: center;
    position: relative;
    padding: 0;
    padding-top: 0;
    font-weight: bold;
    font-size: 2em;
    margin-bottom: 0;
    margin-left: 5%;
    margin-right: 5%;

  }
  .title1::before {
    content: '';
    position: absolute;
  border-color: white;
  border-style: solid;
  border-width: 1em 1em 1em 1em;
  height: 2em;
  top: 0;
  right: 93%;
  width: 0.5em;
  transform: rotate(45deg);
}
.title1::after {
  content: '';
  position: absolute;
border-color: white;
border-style: solid;
border-width: 1em 1em 1em 1em;
height: 2em;
top: 0;
left: 90%;
width: 0.5em;
transform: rotate(45deg);
}

a{
  text-decoration: none;
}
</style>
