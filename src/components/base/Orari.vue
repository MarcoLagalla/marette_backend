<template>
<div class="tabella">
    <v-row v-for="(orari, i) in orari" :key="i" class="rowhover" >
        <v-col cols="6" sm="6">
            <span class="giorno">{{orari.giorno}}</span>
        </v-col>
        <v-col cols="6" sm="6">
            <span class="orario">{{orari.orario}}</span>
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
                orari: [
                    {
                        giorno: 'Lunedi',
                        orario: '18:00 - 22:00',
                    },
                    {
                        giorno: 'martedi',
                        orario: '18:00 - 22:00',
                    },
                ],
            }
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