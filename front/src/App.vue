<template>
  <v-app>
    <v-app-bar dense flat hide-on-scroll app color="primary" dark>
      <img alt="SEL" src="https://selelab.com/SEL_180x180.png" width="20px">
      <div class="d-flex align-center" style="padding: 0 10px">
        エレクトロニクスラボ オンラインハッカソン
      </div>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
      <router-view class="router-content" />
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "App",

  components: {},

  data: () => ({
    //
  })
});
</script>

<style lang="scss">
.router-content {
  width: 80%;
  margin: 5px auto 100px;
}
</style>
