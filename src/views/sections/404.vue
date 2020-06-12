<template>
<div id="404" class="body">
    <gmaps-map>
        <gmaps-marker :position="{ lat: 0, lng: 0 }" />
    </gmaps-map>
</div>
</template>

<script>
    import { gmapsMap, gmapsMarker } from 'x5-gmaps'
export default {
  name: 'FourOhFour',
    components: { gmapsMap, gmapsMarker },
  provide: {
    heading: {
      align: 'center'
    },
  },
}
</script>
<style scoped>
  .body {
    height: 500px!important;
  background: grey;
  }
</style>