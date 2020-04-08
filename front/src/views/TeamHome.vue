<template>
  <div class="team">
    <h2>第{{ contestId }}回 オンラインハッカソン</h2>
    <div>
      <h3>チーム {{teamId}}</h3>
      <h4>サーバー情報</h4>
      <v-simple-table fixed-header height="150px">
        <template v-slot:default>
          <tbody>
            <tr v-for="item in properties" :key="item.name">
              <td>{{ item.name }}</td>
              <td>
                <a
                  v-if="item.link"
                  :href="item.link"
                  target="_blank"
                  rel="noopener"
                >{{ shorten(item.value) }}</a>
                <div v-else>{{ shorten(item.value) }}</div>
              </td>
              <td>
                <v-icon
                  small
                  class="mr-2"
                  v-clipboard:copy="item.value"
                  v-clipboard:success="onCopy"
                  v-clipboard:error="onError"
                >mdi-content-copy</v-icon>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <h4>問題</h4>
      <Tasks></Tasks>
    </div>
    <v-snackbar v-model="snackbar">
      {{ snackbarText }}
      <v-btn color="pink" text @click="snackbar = false">閉じる</v-btn>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Emit } from "vue-property-decorator";

import Tasks from "@/components/Tasks.vue";

@Component({
  components: {
    Tasks
  }
})
export default class ContestHome extends Vue {
  snackbar = false;
  snackbarText = "コピーしました";
  contestId = "";
  teamId = "";
  properties = [
    {
      name: "IPアドレス",
      value: "172.217.26.35",
      link: "http://172.217.26.35/"
    },
    {
      name: "VS Live Share リンク",
      value: "https://prod.liveshare.vsengsaas.visualstudio.com/join?************************************",
      link: "https://prod.liveshare.vsengsaas.visualstudio.com/join?************************************"
    },
    {
      name: "GitHubブランチ",
      value: "feature/contest",
      link: "https://github.com/selelab/admin/tree/feature/contest",
    }
  ];
  members = [
    {
      avatar: "https://cdn.vuetifyjs.com/images/lists/1.jpg",
      title: "山田 太郎"
    },
    {
      avatar: "https://cdn.vuetifyjs.com/images/lists/2.jpg",
      title: "山本 隆"
    },
    {
      avatar: "https://cdn.vuetifyjs.com/images/lists/3.jpg",
      title: "山川 穂高"
    }
  ];
  created(): void {
    this.contestId = this.$route.params.contest_id;
    this.teamId = this.$route.params.id;
  }

  @Emit("on-copy")
  onCopy() {
    this.snackbar = true;
    this.snackbarText = "コピーしました";
  }

  @Emit("on-error")
  onError() {
    this.snackbar = true;
    this.snackbarText = "コピーしました";
  }

  @Emit("shorten")
  shorten(text: string, len?: number) {
    if (text.length > (len || 15)) {
      return text.substr(0, (len || 15)) + "...";
    } else {
      return text;
    }
  }
}
</script>