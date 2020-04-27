<template>
  <div>
    <v-app-bar
      id="home-app-bar"
      app
      color="#FFF8DC"
      height="80"
    >
      <router-link to="/">
        <base-img
          :src="require('@/assets/logo_small.png')"
          contain
          max-width="80"
        />
      </router-link>

      <v-spacer />

      <div>
        <v-row
          class="hidden-sm-and-down"
          optional
        ><v-col>
        <button
        v-if="(this.isLogged)"
        class="btn-6"
        @click="Logout()"
        ><span>Logout</span>
      </button></v-col>
      <v-col
      v-if="(!this.isLogged)"


        min-width="96"
        text
        ><base-form-la></base-form-la>
      </v-col>
      <v-col
      v-if="(!this.isLogged)"
        min-width="96"
        text
        ><base-form-ra/>
      </v-col>
      <div class="ul">

          <v-col

          >
            <router-view  name="restMenu" :items="activeComponents"></router-view>

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
      :items="activeComponents"
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
      activeComponents() {
                return this.$store.getters['restaurantData/components']
            },
      isLogged () {
        return this.$store.getters['userAuthentication/isAuthenticated']
      }
    },

    methods : {
      ...mapActions('userAuthentication', ['logout']),
       Logout: function () {
               return this.logout().then(() => {
                  this.snackbar = true;
                  location.reload()
              }).catch(() => {
                  this.text = 'Logout eseguito con qualche difficoltà'
                  this.snackbar = true;
                  location.reload()
               });
      },
    },
    data: () => ({
      drawer: null,
      snackbar: false,
      text: 'Logout eseguito con successo',
      timeout: 2000,
    }),
  }
</script>

<style scoped>
a {
  text-decoration: none;
  scroll-behavior: smooth;
}
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
.ul .li a {
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
.ul .li a::before {
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
.ul .li a:hover::before {
  transition: ease .4s;
  content: '';
  position: absolute;
  border-color: #af473c;
  border-style: solid;
border-width: 3px 0 0 0;
height: 0.5em;
bottom: 0;
width: 100%;
filter: blur(2px);
}

.ul .li a:hover {
  transition: ease .4s;
  text-shadow: 0 0 8px black;
  color: white
}
.btn-6{
  display: inline-block;
  position: relative;
  margin-top: 10px;
  border-radius: 2px;
  background: none;
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 0 2px black;
  transition: all 0.2s linear;
  background: #2F4F4F;
}
.btn-6:hover {
  color: #666;
  transition: all 0.2s linear;
  background: #C0C0C0;
  box-shadow: 0 0 6px black;
}
span{
  display: block;
  padding: 5px 20px;
  font-weight: ;
  letter-spacing: 5px;
  text-transform: uppercase;
}
.btn-6::before, .btn-6::after{
  content:"";
  width: 0;
  height: 2px;
  position: absolute;
  transition: all 0.2s linear;
  background: #2F4F4F;
  filter: blur(2px);
}

span::before, span::after{
  content:"";
  width:2px;
  height:0;
  position: absolute;
  transition: all 0.2s linear;
  background: #2F4F4F;
  filter: blur(2px);
}
.btn-6:hover::before, .btn-6:hover::after{
  width: 100%;
}
.btn-6:hover span::before, .btn-6:hover span::after{
  height: 100%;
}

.btn-6::before{
  left: 50%;
  top: 0;
  transition-duration: 0.4s;
}
.btn-6::after{
  left: 50%;
  bottom: 0;
  transition-duration: 0.4s;
}
.btn-6 span::before{
  left: 0;
  top: 50%;
  transition-duration: 0.4s;
}
.btn-6 span::after{
  right: 0;
  top: 50%;
  transition-duration: 0.4s;
}
.btn-6:hover::before, .btn-6:hover::after{
  left: 0;
}
.btn-6:hover span::before, .btn-6:hover span::after{
  top: 0;
}
</style>
