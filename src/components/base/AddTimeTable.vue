<template>
  <div>
    <button class="managebtn" @click="activated">Modifica orari di apertura</button>
    <v-dialog v-model="active" max-width="815" >
      <v-card max-width="800" class="pa-6">
        <v-select prepend-icon="mdi-calendar" :items="remainingDays" chips item-text="name" item-value="id" label="Aggiungi giorni di apertura:" v-model="newDay"></v-select>
        <button class="managebtn" @click="submitNewDays">Aggiungi</button>

        <v-card v-for="day in openingDays" :key="day.day">
          <h2>
            <button name="delete" class="managebtn" @click="deleteDay(day)">
              <i  class="fas fa-times"></i>
            </button>
            {{day.day}}:
          </h2>

          <div v-for="orario in day.fasce" :key="orario.id">
            <button name="delete" class="managebtn" @click="deleteTime(day, orario)">
                    <i class="fas fa-times"></i>
                </button>
            {{orario.start}} - {{orario.end}}
          </div>
          <v-expansion-panels
              :value="pannello"
              multiple
          >
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
                <v-row>
                  <button @click="submitTimeInterval(day)">Aggiungi</button>
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
      newDay: '',
      newStart: '',
      newEnd: '',
      pannello: [],
      openingDays: []
    }),
    methods: {
      ...mapActions('restaurantData', ['addOpeningDays', 'removeOpeningDay', 'addTimeInterval', 'removeTimeInterval']),
      activated: function () {
        this.active = !this.active
      },

      submitNewDays: function () {
        this.addOpeningDays(this.newDay).then(()=>{
            this.getOpeningDays()
        })
        this.newDay = []
      },

      deleteDay: function (day) {
        this.removeOpeningDay(day).then(()=>{
            this.getOpeningDays()
            this.days.push(day.day)
            this.remainingDays.push(day.day)
        })
      },


      deleteTime: function (day, time) {
        var payload = {day: day, time: time}
        this.removeTimeInterval(payload).then(()=>{
            this.getOpeningDays()
        })
      },

      submitTimeInterval: function (day) {
        var payload = {day:day, data: {start: this.newStart, end: this.newEnd}}
        console.log(payload)
        console.log(this.openingDays)
        this.addTimeInterval(payload).then(()=>{
            this.getOpeningDays()
            this.pannello = []
        })
      },

      allowedMinutes: m => m % 30 === 0,

      getOpeningDays() {
        if (Object.prototype.hasOwnProperty.call(this.restData, 'openingDays')) {
            this.openingDays = this.restData.openingDays
        } else {
            setTimeout(this.getOpeningDays, 200);
        }
      },

    },
    computed: {
      restData() {
        return this.$store.getters["restaurantData/restData"];
      },
      remainingDays() {
        this.openingDays.forEach((day)=>{
            if(this.days.includes(day.day))
              this.days.splice(this.days.indexOf(day.day), 1)
        })
        return this.days
      }
    },
    created() {
      this.getOpeningDays()

    }
  }
</script>

<style scoped>
  .managebtn {
  box-shadow: 0 0 4px darkslategrey;
margin: 0;
    padding: 10px;
    background: rgba(250,250,250,0.8);
    text-transform: capitalize;
    transition: 0.3s ease-in-out;
  }
  .managebtn:hover {
    background: rgba(250,250,250,1);
  }</style>