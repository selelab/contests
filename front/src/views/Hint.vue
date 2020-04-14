<template>
  <div class="hint">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <Markdown :src="text"></Markdown>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import Markdown from "@/components/Markdown.vue";
import api from "../api";

@Component({
  components: {
    Markdown
  }
})
export default class ContestHome extends Vue {
  text = "";

  async retriveInformation() {
    try {
      const result = (await api.get(`/v1/hints/${this.hintId}/`)).data;
      this.text = result.text;
    } catch (error) {
      console.log(error);
    }
  }

  created(): void {
    this.retriveInformation();
  }

  get hintId() {
    return this.$route.params.id;
  }

  get breadcrumbs() {
    return [
      {
        text: "エレラボ オンラインハッカソン",
        disabled: false,
        href: "/contests"
      },
      {
        text: "ヒント",
        disabled: true,
        href: "/contests/" + this.hintId
      }
    ];
  }
}
</script>

<style lang="scss" scoped>
a {
  color: gray !important;
}
</style>