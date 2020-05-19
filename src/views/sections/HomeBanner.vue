<template>
  <body>

  <div class="hero-image">
      <div class="hero-text">
        <img class="logo" src="@/assets/logo_small.png">
      </div>
  </div>
  </body>
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
  body {
    margin: 0;

  }

  .hero-image {
    background-image: url("../../assets/logo-2.jpg");
    background-color: darkcyan;
    height: 300px;
    background-position: initial;
    background-repeat: no-repeat;
    background-size: cover;
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
