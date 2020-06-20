<template>
  <v-theme-provider>
    <div>
      <base-img
        :src="require('@/assets/logo_small.png')"
        contain
        max-width="128"
        min-height="70"
        width="100%"
      />

      <base-title
        size="body-1"
        space="4"
        title="Modernizziamo chi è rimasto nel 1800"
        weight="regular"
        class="mt-4"
      />
      <base-btn
        class="mb-12"
        color="white"
        to="/about"
        outlined
      >
        Chi siamo
      </base-btn>

      <base-btn
        class="mb-12"
        color="white"
        to="/registrationBusiness"
        outlined
      >
        Lavora Con Noi
      </base-btn>
    </div>
  </v-theme-provider>
</template>

<script>
  export default {
    name: 'BaseInfo',

    data: () => ({

    }),
  }
</script>

<style scoped>
  .mb-12 {
    margin-right: 30px;
    margin-top: 20px;
  }
</style>