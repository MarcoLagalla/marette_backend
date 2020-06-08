<template>
  <div>
    <button @click="activated">Aggiungi orari di apertura</button>
    <v-dialog v-model="active" max-width="815" >
      <v-card max-width="800">
        <v-select :items="remainingDays" multiple chips item-text="name" item-value="id" label="Aggiungi giorni di apertura:" v-model="newDays"></v-select>
        <button @click="submitNewDays">Aggiungi</button>
        <v-card v-for="day in openingDays" :key="day.day">
          <h2>{{day.day}}:</h2>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>Aggiungi fascia oraria</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-label for="start">Inizio</v-label><br>
                     <v-time-picker
                         id="start"
                        v-model="newStart"
                        :allowed-minutes="allowedMinutes"
                        class="mt-4"
                        format="24hr"
                      ></v-time-picker>
                  </v-col>

                  <v-col cols="12" md="6">
                     <v-label for="end">Fine</v-label><br>
                     <v-time-picker
                         id="end"
                        v-model="newEnd"
                        :allowed-minutes="allowedMinutes"
                        class="mt-4"
                        format="24hr"
                      ></v-time-picker>
                  </v-col>
                </v-row>

              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

  export default {
    name: "AddTimeTable",
    data: () => ({
      active: false,
      days: ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica'],
      newDays: [],
      newStart: '',
      newEnd: '',
    }),
    methods: {
      ...mapActions('restaurantData', ['addOpeningDays', 'addTimeTable']),
      activated: function () {
        this.active = !this.active
        this.addTimeTable()
      },

      submitNewDays: function () {
        this.addOpeningDays(this.newDays)
        this.newDays = []
      },

      allowedMinutes: m => m % 30 === 0,

    },
    computed: {
      remainingDays() {
        return this.days
      },
      openingDaysCheNonVa() {
        return this.$store.getters['restaurantData/openingDays']
      },

      openingDays() {
        return this.$store.getters["restaurantData/restData"].openingDays;
      }
    }
  }
</script>

<style scoped>

</style>