<template>

    <div class="body">
      <v-theme-provider dark>
        <div id="info-alt">
          <v-responsive class="mx-auto" max-width="1400">
            <v-container fluid>
              <v-row>
                <v-col cols="12" md="6">
                  <base-info />
                </v-col>
                <v-col cols="12" md="6">
                  <base-info-card title="Contatti" />
                  <base-business-contact dense />
                </v-col>
              </v-row>
            </v-container>
          </v-responsive>
        </div>
      </v-theme-provider>
      <footer>
        <cookie-law theme="dark-lime" buttonText="Accetta">
            <div slot="message">
              <p>
                Questo sito usa i biscotti come Hänsel e Gretel per seguirti.<br>
                Non ti devi preoccupare, qui non ci sono le streghe.
              </p>
            </div>
        </cookie-law>
      </footer>
    </div>

</template>
<script>
  import CookieLaw from 'vue-cookie-law'

export default {
  name: 'HomeFooter',
  components: { CookieLaw },
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
