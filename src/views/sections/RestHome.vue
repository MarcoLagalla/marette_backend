<template>
    <div :style="image" class="body" id="HOME">
        <v-row align="center" class="ma-0 pa-8" justify="center">
            <v-col cols="12" md="6">
                <base-name-rest-card :category="restData.restaurant_category" :description="description" :name="restData.activity_name" :admin="admin"
                                     :opened_now='restData.opened_now' :opens_at="restData.opens_at" @edited="submitDescription($event)"></base-name-rest-card>
            </v-col>
            <v-col cols="6" md="4">
            </v-col>
            <v-col cols="12" md="4">
            </v-col>
        </v-row>
        <template v-if="admin">
            <div class="buttonscontainer">
                <div class="buttons">
                    <v-row>
                        <v-col cols="6">
                            <button name="delete" class="managebtn" @click="deleteImage()">
                                <i class="fas fa-times"></i>
                            </button>
                        </v-col>
                        <v-col cols="6">
                            <base-add-home-image :imageUrl="imageURL" @edited="submitImage($event)"></base-add-home-image>
                        </v-col>
                    </v-row>
                </div>
            </div>
        </template>
    </div>
</template>
<script>
    import {mapActions} from "vuex";

    export default {
        name: "restHome",
        props: {
            restData: {
                type: Object,
                required: true,
            },
            admin: {
                type: Boolean,
                default: false,
            }
        },
        data: function () {
            return {
                modImage: false,
            }
        },
        methods: {
            ...mapActions('restaurantData', ['editHomeComponent', 'getTimeTable']),
            submitDescription: function (des) {
                const data = {
                    description: des
                };
                const formData = new FormData();
                formData.append('data', JSON.stringify(data));
                this.editHomeComponent(formData)
            },
            submitImage: function (img) {
                const formData = new FormData();
                formData.append('data', '{}');
                formData.append('image', img);
                this.editHomeComponent(formData)
            },
            deleteImage: function () {
                const formData = new FormData();
                formData.append('image', '');
                formData.append('data', '{}');
                this.editHomeComponent(formData)
            },

        },
        computed: {
            image() {
                const imgUrl = this.$store.getters['restaurantData/home'].image;
                return {backgroundImage: "url(" + imgUrl + ") "}
            },
            imageURL() {
                return this.$store.getters['restaurantData/home'].image;
            },
            description() {
                return this.$store.getters['restaurantData/home'].description
            },
        },
    }
</script>
<style scoped>

    .body {
        margin: auto;
        height: 100%;
        width: 100%;
        background: no-repeat center center fixed;
        background-size: cover;
        z-index: 10;
        margin-bottom: -10px!important;

    }

    .regbtn2 {
        padding: 10px;
        margin: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
  .buttons {
    position: absolute;
    bottom: 0;
      left: 0;

  }
  .buttonscontainer {
      position: relative;
  }
    .managebtn {
        width: 50px;
        margin: 0;
        border: solid 0.5px grey;
        padding: 10px;
        background: rgba(250,250,250,0.8);
        text-transform: uppercase;
        transition: 0.3s ease-in-out;

    }
    .managebtn:hover {
        background: rgba(250,250,250,1);
    }
</style>
