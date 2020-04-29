<template>
<div class="body">
  <v-theme-provider>
    <base-section id="contact-us" space="300">
      <div class="infocart">
        <v-row justify="center">
          <v-col cols="10">
            <base-title :space="$vuetify.breakpoint.mdAndUp ? 0 : 4" title="HAVE QUESTIONS? LET US KNOW!" />

            <base-body space="0">
              <span class="">
                Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolor itaque modi ab accusantium architecto voluptates ipsa molestiae.
              </span>
            </base-body>
          </v-col>

          <v-col cols="12" md="2">


          </v-col>
        </v-row>
      </div>
    </base-section>
  </v-theme-provider>
</div>
</template>

<script>
export default {
  name: 'SectionChisiamo',
}
</script>
<style scoped>
.body {
  margin: 0 !important;
  background: url("https://images6.alphacoders.com/757/757258.jpg") no-repeat center center fixed;
  //background: url("https://images6.alphacoders.com/607/607222.jpg") no-repeat center center fixed;
  background-size: 1920px 1080px;
}

.infocart {
  background: white;
  padding: 20px;
  box-shadow: 0 0 20px black
}
</style>
