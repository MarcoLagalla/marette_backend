<template>
<v-navigation-drawer right color="transparent" fixed height="auto" overlay-color="secondary" overlay-opacity=".8" temporary v-bind="$attrs" v-on="$listeners">
  <v-list color="white" shaped>
    <v-list-item v-if="(!isLogged)" color="primary">
      <base-form-ra />
    </v-list-item>
    <v-list-item v-if="(!isLogged)" color="primary">
      <base-form-la />
    </v-list-item>
    <v-list-item v-if="(isLogged)"><button class="btn-6" @click="Logout()"><span>Logout</span>
      </button> </v-list-item>
    <router-view name="restMenuMobile" :items="items"></router-view>
  </v-list>
</v-navigation-drawer>
</template>

<script>
import {
  mapActions
} from 'vuex'

export default {
  name: 'HomeDrawer',
  computed: {
    isLogged() {
      return this.$store.getters['userAuthentication/isAuthenticated']
    }
  },

  methods: {
    ...mapActions('userAuthentication', ['logout']),
    Logout: function() {
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
  props: {
    items: {
      type: Array,
      default: () => ([]),
    },
  },
}
</script>
<style scoped>
.btn-6 {
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

span {
  display: block;
  padding: 5px 20px;
  font-weight: ;
  letter-spacing: 5px;
  text-transform: uppercase;
}

.btn-6::before,
.btn-6::after {
  content: "";
  width: 0;
  height: 2px;
  position: absolute;
  transition: all 0.2s linear;
  background: #2F4F4F;
  filter: blur(2px);
}

span::before,
span::after {
  content: "";
  width: 2px;
  height: 0;
  position: absolute;
  transition: all 0.2s linear;
  background: #2F4F4F;
  filter: blur(2px);
}

.btn-6:hover::before,
.btn-6:hover::after {
  width: 100%;
}

.btn-6:hover span::before,
.btn-6:hover span::after {
  height: 100%;
}

.btn-6::before {
  left: 50%;
  top: 0;
  transition-duration: 0.4s;
}

.btn-6::after {
  left: 50%;
  bottom: 0;
  transition-duration: 0.4s;
}

.btn-6 span::before {
  left: 0;
  top: 50%;
  transition-duration: 0.4s;
}

.btn-6 span::after {
  right: 0;
  top: 50%;
  transition-duration: 0.4s;
}

.btn-6:hover::before,
.btn-6:hover::after {
  left: 0;
}

.btn-6:hover span::before,
.btn-6:hover span::after {
  top: 0;
}
</style>
