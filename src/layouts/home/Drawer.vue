<template>
  <v-navigation-drawer
    right
    color="transparent"
    fixed
    height="auto"
    overlay-color="secondary"
    overlay-opacity=".8"
    temporary
    v-bind="$attrs"
    v-on="$listeners"
  >
    <v-list
      color="white"
      shaped
    >
    <v-list-item
      v-if="(!isLogged)"
      color="primary"
    >
    <base-form-r/>
    <base-form-l/>
    </v-list-item>
    <v-list-item
      v-if="(isLogged)"
      color="primary"
    > <v-btn text
    @click="Logout()"
    > Logout
  </v-btn> </v-list-item>
      <v-list-item
        v-for="name in items"
        :key="name"
        :to="{ name }"
        :exact="name === 'Home'"
        color="primary"
      >
        <v-list-item-content>
          <v-list-item-title v-text="name" />
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    name: 'HomeDrawer',
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
    props: {
      items: {
        type: Array,
        default: () => ([]),
      },
    },
  }
</script>
