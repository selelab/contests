<template>
  <div class="question">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h2>{{questionInfo.title}}</h2>
    <Markdown :src="questionInfo.text"></Markdown>
    <v-divider style="margin: 20px 0"></v-divider>
    <h2>回答</h2>
    <Markdown :src="getCommentHTML(questionInfo)"></Markdown>
  </div>
</template>

<script lang="ts">
import { Component, Emit, Vue } from "vue-property-decorator";

import Markdown from "@/components/Markdown.vue";
import api from "../api";

@Component({
  components: {
    Markdown
  }
})
export default class ContestHome extends Vue {
  questionInfo = {
    comment: "",
    text: ""
  }
  contestInfo = {
    title: null
  };

  async retrieveInformation() {
    try {
      this.questionInfo = (await api.get(`/v1/questions/${this.questionId}/`)).data;
      this.contestInfo = (await api.get(`/v1/contests/${this.contestId}/`)).data;
    } catch (error) {
      console.log(error);
    }
  }

  created(): void {
    this.retrieveInformation();
  }

  get questionId() {
    return this.$route.params.id;
  }

  get contestId() {
    return this.$route.params.contestId;
  }

  get breadcrumbs() {
    return [
      {
        text: "エレラボ オンラインハッカソン",
        disabled: false,
        href: "/contests"
      },
      {
        text: this.contestInfo.title,
        disabled: false,
        href: "/contests/" + this.contestId
      },
      {
        text: "質問",
        disabled: true,
        href: "/contests/" + this.contestId + '/questions/' + this.questionId
      }
    ];
  }

  @Emit("get-comment-html")
  getCommentHTML(item: { comment: string; link: string }) {
    if (!item.comment) return "";
    if (!item.link) return item.comment.replace("%%%HINT%%%", "");
    return item.comment.replace(
      "%%%HINT%%%",
      `<a href="${item.link}" target="_blank" rel="noopener">ヒント</a> `
    );
  }
}
</script>

<style lang="scss" scoped>
a {
  color: gray !important;
}
</style>
