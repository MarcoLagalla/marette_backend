<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    color="lime lighten-5"
    temporary
  >
  <v-system-bar
      color="blue-grey darken-4"
      height="65"
      dark
    ></v-system-bar>
    <v-list>
      <v-list-item>
        <v-chip
      class="ma-2"
      color="success"
      outlined
    >
      <v-icon left>mdi-server-plus</v-icon>
      Server Status
    </v-chip>
  </v-list-item>
  <v-list-item>
    <v-chip
      class="ma-2"
      color="primary"
      outlined
      pill
    >
      <v-icon left>mdi-account-outline</v-icon>
      User Account
    </v-chip>
  </v-list-item>
  <v-list-item>
    <v-chip
      class="ma-2"
      color="deep-purple accent-4"
      outlined
    >
      <v-icon left>mdi-wrench</v-icon>
      Update Settings
    </v-chip>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
  // Utilities
  import {
    mapGetters,
    mapMutations
  } from 'vuex'

  export default {
    name: 'CoreDrawer',

    computed: {
      ...mapGetters(['links']),
      drawer: {
        get () {
          return this.$store.state.drawer
        },
        set (val) {
          this.setDrawer(val)
        }
      }
    },

    methods: {
      ...mapMutations(['setDrawer']),
      onClick (e, item) {
        e.stopPropagation()

        if (item.to === '/') {
          this.$vuetify.goTo(0)
          this.setDrawer(false)
          return
        }

        if (item.to || !item.href) return

        this.$vuetify.goTo(item.href)
        this.setDrawer(false)
      }
    }
  }
</script>
