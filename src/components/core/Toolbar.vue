<template>
  <v-app-bar
    fixed
    app
    flat
    dark
  >
    <v-app-bar-nav-icon
    absolute
      @click="toggleDrawer"
    />
    <v-container
      mx-auto
      py-0
    >
      <v-layout>
        <v-img
          :src="require('@/assets/logo.png')"
          class="mr-5"
          contain
          height="48"
          width="48"
          max-width="48"
          @click="$vuetify.goTo(0)"
        />
        <router-link
          to="/login">
        <v-btn
          class="ma-2"
          color="success"
          >Login</v-btn></router-link>
        <v-btn rounded
          v-for="(link, i) in links"
          :key="i"
          :to="link.to"
          class="ma-2 hidden-sm-and-down"
          flat
          @click="onClick($event, item)"
        >
          {{ link.text }}
        </v-btn>
        <v-spacer />
        <v-text-field
          append-icon="mdi-magnify"
          flat
          hide-details
          solo-inverted
          style="max-width: 300px;"
        />
      </v-layout>
    </v-container>
  </v-app-bar>
</template>

<script>
  // Utilities
  import {
    mapGetters,
    mapMutations
  } from 'vuex'

  export default {
    data: () => ({
      collapseOnScroll: true,
    }),
    computed: {
      ...mapGetters(['links'])
    },

    methods: {
      ...mapMutations(['toggleDrawer']),
      onClick (e, item) {
        e.stopPropagation()

        if (item.to || !item.href) return

        this.$vuetify.goTo(item.href)
      }
    }
  }
</script>
