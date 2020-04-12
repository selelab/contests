<template>
  <div class="team">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h2>{{contestInfo.title}}</h2>
    <div>
      <h3>チーム {{teamInfo.name}}</h3>
      <h4>サーバー情報</h4>
      <v-card class="table-card">
        <v-simple-table fixed-header>
          <tbody>
            <tr v-for="item in properties" :key="item.name">
              <td width="180px">{{ item.name }}</td>
              <td>
                <a
                  v-if="item.link"
                  :href="item.link"
                  target="_blank"
                  rel="noopener"
                >{{ shorten(item.value) }}</a>
                <div v-else>{{ shorten(item.value) }}</div>
              </td>
              <td width="10px">
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
        </v-simple-table>
      </v-card>
      <br />
      <h4>提出/質問</h4>
      <v-card class="table-card" flat>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>提出</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <div style="width: 80%; display: inline-block;">
          <v-select
            v-model="submitTask"
            :items="submittableTasks"
            menu-props="auto"
            label="Select"
            hide-details
            prepend-icon="mdi-flash"
            single-line
          ></v-select>
        </div>
        <div style="width: 10%; display: inline-block; margin: 0 5%;">
          <v-btn style="width: 100%; margin: auto">提出</v-btn>
        </div>
        <v-divider style="margin: 20px 0"></v-divider>
        <div>
          <v-textarea v-model="questionText" />
        </div>
        <div style="width: 10%; display: inline-block; margin: 0 5%;">
          <v-btn style="width: 100%; margin: auto">送信</v-btn>
        </div>
      </v-card>
      <h4>回答状況</h4>
      <v-card class="table-card" flat>
        <v-data-table
          :headers="submission_headers"
          :items="submissions"
          hide-default-footer
          class="elevation-1"
        >
          <template v-slot:item.status="{ item }">
            <v-icon :color="getColor(item.status)">{{getIcon(item.status)}}</v-icon>
          </template>
          <template v-slot:item.score="{ item }">{{item.score || "一"}}</template>
        </v-data-table>
      </v-card>
      <br />
      <h4>問題</h4>
      <Tasks :tasks="tasks"></Tasks>
    </div>
    <v-snackbar v-model="snackbar">
      {{ snackbarText }}
      <v-btn color="pink" text @click="snackbar = false">閉じる</v-btn>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import camelcaseKeys from "camelcase-keys";
import { Component, Vue, Emit } from "vue-property-decorator";

import Tasks from "@/components/Tasks.vue";
import Markdown from "@/components/Markdown.vue";
import api from "../api";

@Component({
  components: {
    Tasks,
    Markdown
  }
})
export default class ContestHome extends Vue {
  tasks = [];
  snackbar = false;
  snackbarText = "コピーしました";
  teamInfo = {
    vsLiveshareLink: null,
    name: null,
    title: null,
    id: null
  };

  submitTask = null;
  questionText = "### 質問の内容\n\n### 試したこと\n- 箇条書きで書く\n";
  submission_headers = [
    {
      text: "問題番号",
      value: "taskName"
    },
    {
      text: "得点",
      value: "score",
      align: "center"
    },
    {
      text: "提出回数",
      value: "count",
      align: "center"
    },
    {
      text: "提出時刻",
      value: "time"
    },
    {
      text: "ステータス",
      value: "status"
    }
  ];
  submissions = [
    {
      taskName: "問題1",
      score: null,
      time: "00:10",
      count: "1 / 3 回目",
      status: "rejected"
    },
    {
      taskName: "問題1",
      score: 100,
      time: "00:13",
      count: "2 / 3 回目",
      status: "accepted"
    },
    {
      taskName: "問題2",
      score: null,
      time: "00:30",
      count: "1 / 3 回目",
      status: "pending"
    }
  ];
  properties = [
    {
      name: "IPアドレス",
      key: "ipAddress",
      value: "",
      link: "http://<value>/"
    },
    {
      name: "VS Live Share リンク",
      key: "vsLiveshareLink",
      value: "",
      link: "<value>"
    },
    {
      name: "GitHubブランチ",
      key: "githubBranchName",
      value: "",
      link: "https://github.com/selelab/admin/tree/<value>"
    }
  ];
  contestInfo = {
    id: null,
    title: null
  };

  created(): void {
    (async () => {
      try {
        const result = camelcaseKeys(
          (await api.get(`/v1/teams/${this.teamId}/`)).data
        );
        this.teamInfo.name = result.name;
        this.properties.forEach(item => {
          if (item.key) {
            item.value = result[item.key];
            if (item.link)
              item.link = item.link.replace(/<value>/g, result[item.key]);
          }
        });
        this.tasks = result.contest.tasks;
        this.contestInfo = result.contest;
      } catch (error) {
        console.log(error);
      }
    })();
  }

  get contestId() {
    return this.$route.params.contest_id;
  }

  get teamId() {
    return this.$route.params.id;
  }

  get submittableTasks() {
    return this.tasks.map(
      (item: { id: string; title: string }, index: number) => {
        return {
          text: String.fromCodePoint(index + 65) + "." + item.title,
          value: item.id
        };
      }
    );
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
        href: "/contests/" + this.contestInfo.id
      },
      {
        text: this.teamInfo.name,
        disabled: true,
        href: "#"
      }
    ];
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
    const maxLength = 32;
    if (!text) return "";
    if (text.length > (len || maxLength)) {
      return text.substr(0, len || maxLength) + "...";
    } else {
      return text;
    }
  }

  @Emit("get-icon")
  getIcon(status: string) {
    if (status == "accepted") return "mdi-check";
    else if (status == "pending") return "mdi-circle-medium";
    else return "mdi-cancel";
  }

  @Emit("get-color")
  getColor(status: string) {
    if (status == "accepted") return "green";
    else if (status == "pending") return "orange";
    else return "red";
  }
}
</script>

<style scoped>
.table-card {
  width: 80%;
  margin: 10px 0;
  padding: 10px 20px;
}
</style>