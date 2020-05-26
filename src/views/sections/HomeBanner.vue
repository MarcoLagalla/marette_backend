<template>
  <div class="body">

  <div class="hero-image">
      <div class="hero-text">
        <img class="logo" src="@/assets/logo_small_icon_only_inverted.png">
      </div>
  </div>
  </div>
</template>

<script>
export default {
  name: 'HomeBanner',

  provide: {
    heading: {
      align: 'center'
    },
  },
}
</script>

<style scoped>
  .body {
    margin: auto;

  }

  .hero-image {
    background-image: url("../../assets/pattern3.png");

    height: 300px;
    background-repeat: repeat;
    position: relative;
     border-bottom: 4px solid var(--ming);
  }

  .hero-text {
    text-align: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
  }
  .logo {
    width: 40%;
  }

</style>
