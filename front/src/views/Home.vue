<template>
  <div class="home">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h2>上智大学エレクトロニクスラボ</h2>
    <router-link to="/1">第1回 オンラインハッカソン</router-link>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Home extends Vue {
  get breadcrumbs() {
    return [
      {
        text: "エレラボ オンラインハッカソン",
        disabled: true,
        href: "/contests"
      }
    ];
  }
}
</script>
