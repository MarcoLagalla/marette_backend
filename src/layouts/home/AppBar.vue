<template>
  <div>
    <v-app-bar
      id="home-app-bar"
      app
      color="white"
      elevation="1"
      height="80"
    >
      <router-link to="/">
        <base-img
          :src="require('@/assets/marette-logo.png')"
          contain
          max-width="180"
          width="100%"
        />
      </router-link>

      <v-spacer />

      <div>
        <v-tabs
          class="hidden-sm-and-down"
          optional
        >
        <v-tab
        v-if="(this.isLogged)"
        @click="Logout()"

        class="font-weight-bold"
        min-width="96"
        text
        > Logout
      </v-tab>
      <v-tab
      v-if="(!this.isLogged)"

        class="font-weight-bold"
        min-width="96"
        text
        ><base-form-l/>
      </v-tab>
      <v-tab
      v-if="(!this.isLogged)"

        class="font-weight-bold"
        min-width="96"
        text
        ><base-form-r/>
      </v-tab>
          <v-tab
            v-for="(name, i) in items"
            :key="i"
            :to="{ name }"
            :exact="name === 'Home'"
            :ripple="false"
            active-class="text--primary"
            class="font-weight-bold"
            min-width="96"
            text
          >
            {{ name }}
          </v-tab>
        </v-tabs>
        <v-snackbar
          v-model="snackbar"
          :timeout="timeout"
          color="cyan darken-2"
        >
          {{ text }}
        </v-snackbar>

      </div>

      <v-app-bar-nav-icon
        class="hidden-md-and-up"
        @click="drawer = !drawer"
      />
    </v-app-bar>

    <home-drawer
      v-model="drawer"
      :items="items"
    />
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    name: 'HomeAppBar',

    components: {
      HomeDrawer: () => import('./Drawer'),
    },

    computed: {
      isLogged () {
        return this.$store.getters['userAuthentication/isAuthenticated']
      }
    },

    methods : {
      ...mapActions('userAuthentication', ['logout']),
       Logout: function () {
               return this.logout().then(() => {
                  this.snackbar = true;
                  this.$router.push('/')
              }).catch(() => {
                  this.text = 'Logout eseguito con qualche difficoltà'
                  this.snackbar = true;
                  this.$router.push('/')
               });
      },
    },
    data: () => ({
      drawer: null,
      items: [
        'Home',
        'About',
        'Contact',
      ],
      snackbar: false,
      text: 'Logout eseguito con successo',
      timeout: 2000,
    }),
  }
</script>

<style lang="sass">
  #home-app-bar
    .v-tabs-slider
      max-width: 24px
      margin: 0 auto

    .v-tab
      &::before
        display: none
</style>
