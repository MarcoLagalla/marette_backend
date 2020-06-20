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
                    <div id="map" :class="$vuetify.breakpoint.smAndDown? 'mapmob':'mapdesk' "></div>
               </v-col>
           </v-row>
       </div>
    </div> 
</template>
<script src="https://maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyAq7abrbPQCp4oxf0jRCHIZZ5yMsphbB_8"></script>
<script>
import ax from 'axios'
export const axios = ax

export default {
    name: "BaseRestInfo",
    props: ['id'],

    mounted: function(){
        this.initMap();
    },
    methods: {
        initMap() {
            var myLatLng = {lat: -25.363, lng: 131.044};
            var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 12,
            center: myLatLng,
            disableDefaultUI: true
            });

            this.getStreetAddressFrom(map)

        },
        async getStreetAddressFrom(map) {
       try {
           var address = this.restData.address + " " + this.restData.n_civ + " " + this.restData.city + " " + this.restData.cap;
          var {
             data
          } = await axios.get("https://maps.googleapis.com/maps/api/geocode/json?address=" +
              address + "&key=AIzaSyAq7abrbPQCp4oxf0jRCHIZZ5yMsphbB_8"
          );
          if (data.error_message) {
             console.log(data.error_message)
          } else {
              var myLatLng = {lat: data.results[0].geometry.location.lat, lng: data.results[0].geometry.location.lng}
              var marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
              title: this.restData.activity_name
            });
              map.setCenter(marker.getPosition());
                var infowindow = new google.maps.InfoWindow({
                    content: this.restData.activity_name
                  });
                infowindow.open(map, marker);
               marker.addListener('click', function() {
    infowindow.open(map, marker);
  });
          }
       } catch (error) {
          console.log(error.message);
       }
    }
    },
    computed: {
        restData() {
            return this.$store.getters["restaurantData/restData"];
        }
    },
}
</script>
<style  scoped>
    .mapmob{
        width: 100%;
        height: 250px;
    }
    .mapdesk{
        width: 450px; height: 250px;
        margin: auto;
    }
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
    margin: auto;
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
