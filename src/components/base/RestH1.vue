<template>
  <div class="container">
  <h2 class="background"><span><slot/></span></h2>
  <div class="divider"></div>
  </div>
</template>

<script>
export default {
  name: 'BaseRestH1',

  props: {

  },

}
</script>

<style lang="css" scoped>
/* Helper classes */
.basil {
  background-color: var(--ghostwhite) !important;

}
.basil--text {
  color: var(--emerald) !important;
  text-shadow: 0 0 2px grey;
}
h2 {
  font-size: 26px;
  color: var(--ming);
  margin-top: 0;
  padding: 2vmax;
  text-align: center;
  text-transform: uppercase;
}
@media screen and (max-width: 992px) {
  h2 {
    font-size: 26px;
  }
}
h2.background {
  position: relative;
  z-index: 1;
  padding: 1vmax;
}
h2.background:before {

}
h2.background span {
  /* to hide the lines from behind the text, you have to set the background color the same as the container */
  background: var(--whitesmoke);
  padding: 5px 10vmax;
  color: var(--ming);
  font-weight: lighter;
  letter-spacing: 5px;

}
.divider {
  background: linear-gradient( to right, var(--ming), grey, var(--ming));
  //background: var(--ming);
  height: 4px;
  width: 20vmax;
  margin:  auto;
  filter: blur(2px);
}
  .container {
    padding: 10px;
  }
</style>
