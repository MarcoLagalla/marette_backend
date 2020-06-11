<template>
<div class="tabella">
    <v-row v-for="(day, i) in openingDays" :key="i" class="rowhover" >
        <v-col cols="6" sm="6">
            <span class="giorno">{{day.day}}</span>
        </v-col>
        <v-col cols="6" sm="6">
            <span class="orario">{{fasceToString(day.fasce)}}</span>
        </v-col>
        <div class="divider"></div>
    </v-row>
</div>
</template>

<script>
    export default {
        name: "BaseOrari",
        data() {
            return {
                openingDays: []
            }
        },
        computed: {
            restData() {
                return this.$store.getters["restaurantData/restData"];
            },
        },
        methods: {
            fasceToString: function (fasce) {
                var string = ''
                fasce.forEach((orario)=>{
                    string += orario.start + ' - ' + orario.end + ' | '
                })
                return string.substring(0, string.length-3);
            },
            getOpeningDays() {
                if (Object.prototype.hasOwnProperty.call(this.restData, 'openingDays')) {
                    this.openingDays = this.restData.openingDays
                } else {
                    setTimeout(this.getOpeningDays, 200);
                }
              },
        },
        created() {
          this.getOpeningDays()
        }
    }
</script>

<style scoped>
.tabella {

    border-radius: 25px;
    width: 100%;
    margin: auto;
    padding: 10px;

}
    .divider{
        height: 1px;
        width: 90%;
        margin: auto;
        background: darkslategray;
        filter: blur(2px);
        transition: 0.3s ease-in-out;
    }
    .divider::before {
        content: '';
        position: absolute;
        border-color: rgba(200,200,255,0.2);
        border-style: solid;
        border-width: 50px 0 0 0;
        height: 0;
        left: 0;
        bottom: 0;
        width: 0;
        transition: .4s;
    }
    .giorno {
        text-transform: capitalize;
    }
    .orario {
        color: darkslateblue;
    }
    .rowhover:hover > .divider::before{
        transition: ease .4s;
        content: '';
        position: absolute;
        border-color: rgba(200,200,255,0.2);
        border-style: solid;
        border-width: 50px 0 0 0;
        height: 0;
        bottom: 0;
        width: 100%;
        filter: blur(2px);
    }
</style>