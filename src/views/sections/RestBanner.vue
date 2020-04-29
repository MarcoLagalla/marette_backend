<template>
  <div class="body" id="Home">
    <v-row align="center" class="ma-0 pa-8" justify="center">
      <v-col cols="6" md="4">
      </v-col>
      <v-col cols="6" md="4">
      </v-col>
      <v-col cols="6" md="4">
        <base-name-rest-card :activity_description="restData.activity_description" :activity_name="restData.activity_name" :admin="admin"></base-name-rest-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  name: "restban",
  props: {
    restData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    admin: true
  })
}
</script>
<style scoped>
.infocard {
  height: 400px;
}
.body {
  margin: 0 !important;
  background: url("https://images6.alphacoders.com/609/609345.jpg") no-repeat center center fixed;
  background-size: cover;
}
.regbtn2 {
  padding: 10px;
  margin: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
