<template>
  <v-app>
    <v-app-bar dense flat color="primary" dark>
      <div class="d-flex align-center"></div>

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
