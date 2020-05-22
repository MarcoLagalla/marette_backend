<template>

    <div class="body">
      <v-theme-provider dark>
        <div id="info-alt">
          <v-responsive class="mx-auto" max-width="1400">
            <v-container fluid>
              <v-row>
                <v-col cols="12" md="3">
                  <base-info />
                </v-col>
                <v-col cols="12" md="3">
                  <base-info-card title="Contact" />
                  <base-business-contact dense />
                </v-col>
                <v-col cols="12" md="3">
                </v-col>
                <v-col cols="12" md="3">
                </v-col>
              </v-row>
            </v-container>
          </v-responsive>
        </div>
      </v-theme-provider>
    </div>

</template>
<script>
export default {
  name: 'HomeFooter',
  data: () => ({

  }),
}
</script>
  <style scoped>
    #home-footer a {
      text-decoration: none;
    }
    .footer {
      background: var(--charcoal);
    }
    a {
      text-decoration: none;
    }
    .body {
      background: var(--charcoal) !important;
    }
      </style>
