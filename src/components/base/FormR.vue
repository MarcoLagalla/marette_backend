<template>
  <v-row justify="center">
    <v-dialog v-model="dialog"  max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn text
        class="font-weight-bold"
        min-width="96"
        v-on="on">SIGNUP</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">User Profile</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                id="username"
                v-model="username"
                label="Username"
                required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Legal first name*" id="first_name" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                label="Legal last name*"
                hint="example of persistent helper text"
                persistent-hint
                id="last_name"
                required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Email*" id="email" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Password*" id="password" type="password" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                label="Repeat password" id="password2" type="password" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                id="birth_date"
                label="Birth date"
                v-model="birth_date"
                type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                id="phone"
                name="phone"
                label="Phone number"
                v-model="phone"
                type="tel"
                ></v-text-field>
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
