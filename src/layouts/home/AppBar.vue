<template>
  <div>
    <v-app-bar
      id="home-app-bar"
      app

      color="white"
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
        <v-row
          class="hidden-sm-and-down"
          optional
        ><v-col>
        <v-btn
        v-if="(this.isLogged)"
        dark
        class="mx-2"
        color=""
        @click="Logout()"
        > Logout
      </v-btn></v-col>
      <v-col
      v-if="(!this.isLogged)"

        class="font-weight-bold"
        min-width="96"
        text
        ><base-form-la></base-form-la>
      </v-col>
      <v-col
      v-if="(!this.isLogged)"

        class="font-weight-bold"
        min-width="96"
        text
        ><base-form-ra/>
      </v-col>
      <div class="ul">


          <v-col

          >
          <router-link
          tag="button"
          v-for="(name, i) in items"
          :key="i"
          :to="{ name }"
          :exact="name === 'Home'"
          :ripple="false"
           class="li">

          <div
            class="a"
            :to="{ name }"
            :exact="name === 'Home'"
            :ripple="false"
            min-width="96"

            >
            {{ name }}</div></router-link>
          </v-col></div>
        </v-row>
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

<style scoped>

.ul {
  margin: 0;
  padding: 0;
  display: flex;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ul .li {
  list-style: none;
  margin: 0 15px;
}
@import url('https://fonts.googleapis.com/css2?family=B612&display=swap');
.ul .li .a {
  padding-left: 5px;
  position: relative;
  display: block;
  text-align: center;
  line-height: 45px;
  border: solid rgba(255, 255, 255, 0) 4px ;
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'B612', sans-serif;
  text-transform: ;
  color: #666;
  transition: .4s;
}
.ul .li .a::before {
  content: '';
  position: absolute;
  margin-left: -5px;
  margin-bottom: -5px;
border-color: white;
border-style: solid;
border-width: 3px 0 0 0;
height: 0;
bottom: 0;
width: 0;
transition: .4s;
}
.ul .li .a:hover::before {
  transition: ease .4s;
  content: '';
  position: absolute;
  border-color: red;
  border-style: solid;
border-width: 3px 0 0 0;
height: 0.5em;
bottom: 0;
width: 100%;
filter: blur(2px);
}

.ul .li .a:hover {
  transition: ease .4s;
  text-shadow: 0 0 8px black;
  color: white
}
.v-btn:hover {
  background: #b00c11!important;
  transition: ease .4s;
  box-shadow: 0 2px 6px black;
border: inset 5px #b00c11!important;
}
.v-btn {
  border: inset 5px;
  elevation: 4;
  transition: ease .6s;
  border: inset 5px #3282dd!important;
  background: #3282dd!important;
}
</style>
