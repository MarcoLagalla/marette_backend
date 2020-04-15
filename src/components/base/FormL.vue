<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"  max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn text
        
        class="font-weight-bold"
        min-width="96"
        v-on="on">LOGIN</v-btn>
      </template>
      <v-card
      color="grey"
      >
        <v-card-title>
          <span class="font-italic"

          >DATI</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field solo filled label="Email*" id="email" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field solo filled label="Password*" id="psw" type="password" required></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
// Mixins
import Heading from '@/mixins/heading'

export default {
  name: 'BaseForm',

  mixins: [Heading],

  data: () => ({
    dialog: false,
  }),
}
</script>
