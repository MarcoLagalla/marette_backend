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
  export default {
    name: 'HomeDrawer',

    props: {
      items: {
        type: Array,
        default: () => ([]),
      },
    },
  }
</script>
