<template>
  <router-link :to="{ name: 'profile'}">
    <v-card
    id="settings"
    class="profcard"
    color="#ffffff8D"
    dark
    flat
    style="position: fixed; top: 164px; right: -35px;"
    width="100"
    >
    <v-icon
    class="proficon"
    large>
    mdi-account
  </v-icon>
</v-card></router-link>
</template>
<script>
export default {
  name: 'HomeSettings',
  data() {
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
.title1 {
  background: rgba(200, 20, 20, 0.7);
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
.proficon {
  color: var(--darkslate);
}
a {
  text-decoration: none;
}
  .profcard {
    z-index: 999;
    padding: 15px;
    box-shadow: 0 0 6px black!important;
  }
</style>
