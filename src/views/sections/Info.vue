<template>
  <div class="body">


  <v-theme-provider dark>
    <base-section
      id="info-alt"
      
    >
      <v-responsive
        class="mx-auto"
        max-width="1400"
      >
        <v-container fluid>
          <v-row>
            <v-col
              cols="12"
              md="3"
            >
              <base-info />
            </v-col>

            <v-col
              cols="12"
              md="3"
            >
              <base-info-card title="Contact" />

              <base-business-contact dense />
            </v-col>

            <v-col
              cols="12"
              md="3"
            >

            </v-col>

            <v-col
              cols="12"
              md="3"
            >

            </v-col>
          </v-row>
        </v-container>
      </v-responsive>
    </base-section>
  </v-theme-provider>  </div>
</template>

<script>
  export default {
    name: 'SectionBusinessInfo',

    components: {
    },
  }
</script>

<style scoped>
a {
  text-decoration: none;
}
.body {
  background: #3c3c3c!important;
}
</style>
