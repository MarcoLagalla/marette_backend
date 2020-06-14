<template>
   <div class="body" id="">
       <!--div class="infbanner">

       </div-->
       <div class="infcols">
           <v-row>
               <v-col cols="12" md="4">
                   <div class="restlogo">
                        <v-img
                                max-width="200" max-height="200" class="ma-auto"
                                src="@/assets/logo_small_icon_only.png">
                        </v-img>
                   </div>
               </v-col>
               <v-col cols="12" md="4" align="center" class="mt-4">
                    <div class="continfs">
                        <span class="restname">{{restData.activity_name}}</span>
                        <span class="restdati">{{restData.city}}</span>
                        <span class="restdati">{{restData.cap}}</span>
                        <span class="restdati">{{restData.address}} {{restData.n_civ}}</span>
                    </div>
               </v-col>
               <v-col cols="12" md="4">

                        <gmaps-map :options="mapOptions" />

               </v-col>
           </v-row>
       </div>
    </div> 
</template>

<script>
    import { gmapsMap } from 'x5-gmaps'

export default {
    name: "BaseRestInfo",
    components: { gmapsMap },
    props: ['id'],
    data: () => ({
        mapOptions: {
            center: { lat: -27.47, lng: 153.025 },
            zoom: 12,
        },
    }),
    computed: {
        restData() {
            return this.$store.getters["restaurantData/restData"];
        }
    },
}
</script>
<style  scoped>
.infbanner {
    margin: 0;
    height: 300px;
    width: 100%;
    background: url("https://images3.alphacoders.com/597/597555.jpg") no-repeat center center fixed;
    background-size: cover;
}
.continfs {
    margin: auto;
    justify-content: center;
}
.infcols {
    width: 90%;
}
.restdati {
    display: block;
    text-transform: capitalize;
    font-size: 1em;

}
    .restname {
        font-size: 1.2em;
        text-transform: capitalize;
        font-weight: bold;
    }
</style>
