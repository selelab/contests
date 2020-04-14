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
      <h4 id="forms">提出/質問</h4>
      <v-card class="table-card" flat>
        <v-alert
          v-model="alert"
          :value="!!errorMessage"
          type="error"
          style="margin: auto; margin-bottom: 30px"
          outlined
          dismissible
        >{{ errorMessage }}</v-alert>
        <v-card flat>
          <v-card-title>提出をする</v-card-title>
          <v-form ref="submitForm" v-model="submitValid" lazy-validation>
            <v-list-item>
              <v-list-item-content>
                <v-select
                  v-model="submitTaskId"
                  :items="submittableTasks"
                  menu-props="auto"
                  label="提出する問題"
                  prepend-icon="mdi-file-multiple"
                  :rules="[v => !!v || '提出する問題を選択してください。']"
                  required
                ></v-select>
              </v-list-item-content>
              <v-btn icon>
                <v-icon @click="clearSelection">mdi-close</v-icon>
              </v-btn>
            </v-list-item>
            <v-card-actions>
              <v-spacer />
              <v-btn
                style="width: 120px; margin: auto"
                @click="onSubmitClick"
                :disabled="connecting || !submitValid"
              >提出</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
        <v-divider style="margin: 20px 0"></v-divider>
        <v-card flat>
          <v-card-title>質問をする・ヒントを頼む</v-card-title>
          <v-form ref="questionForm" v-model="questionValid" lazy-validation>
            <v-list-item>
              <v-list-item-content>
                <v-select
                  v-model="submitTaskId"
                  :items="submittableTasks"
                  menu-props="auto"
                  label="質問に関連する問題"
                  prepend-icon="mdi-file-multiple"
                ></v-select>
              </v-list-item-content>
              <v-btn icon>
                <v-icon @click="clearSelection">mdi-close</v-icon>
              </v-btn>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-text-field
                  v-model="questionTitle"
                  label="タイトル (10文字程度)"
                  outlined
                  flat
                  :rules="[
                    v => !!v || 'タイトルを入力してください',
                  ]"
                />
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-textarea
                  v-model="questionText"
                  outlined
                  label="内容 (Markdown記法)"
                  flat
                  rows="7"
                  :rules="[
                    v => (!!v && (v && v != this.defaultQuestionText)) || '質問を入力してください。',
                  ]"
                />
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-spacer />
              <v-btn
                style="width: 120px; margin: auto"
                @click="requestQuestion"
                :disabled="connecting"
              >送信</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-card>
      <h4 id="questions">質問の回答一覧</h4>
      <v-card class="table-card" flat>
        <v-data-table
          :headers="questionsHeaders"
          :items="questions"
          hide-default-footer
          :items-per-page="questions.length"
          class="elevation-1"
        >
          <template v-slot:item.task="{ item }">
            <div>{{getTaskChar(item.task) || "一"}}</div>
          </template>
          <template v-slot:item.status="{ item }">
            <v-icon :color="getColor(item.status)">{{getIcon(item.status)}}</v-icon>
          </template>
          <template v-slot:item.commentHTML="{ item }">
            <div v-html="getCommentHTML(item)"></div>
          </template>
          <template v-slot:item.id="{ item }">
            <a
              class="gray-link"
              :href="`/contests/1/questions/${item.id}`"
              target="_blank"
              rel="noopener"
              v-if="!!item.id"
            >{{shorten(item.title, 10)}}</a>
          </template>
          <template v-slot:item.point="{ item }">{{item.point || "一"}}</template>
          <template v-slot:item.time="{ item }">{{getTimeElapsed(item.dateCreated)}}</template>
        </v-data-table>
      </v-card>
      <br />
      <h4 id="submissions">提出状況</h4>
      <v-card class="table-card" flat>
        <v-data-table
          :headers="submissionHeaders"
          :items="submissions"
          hide-default-footer
          :items-per-page="submissions.length"
          class="elevation-1"
        >
          <template v-slot:item.task="{ item }">
            <div>{{getTaskChar(item.task)}}</div>
          </template>
          <template v-slot:item.status="{ item }">
            <v-icon :color="getColor(item.status)">{{getIcon(item.status)}}</v-icon>
          </template>
          <template v-slot:item.point="{ item }">{{item.point || "一"}}</template>
          <template v-slot:item.time="{ item }">{{getTimeElapsed(item.dateCreated)}}</template>
          <template
            v-slot:item.count="{ item }"
          >{{getSubmissionNumber(item)}} / {{maxSubmitNumber}} 回目</template>
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
    <Confirm ref="confirm"></Confirm>
  </div>
</template>

<script lang="ts">
import camelcaseKeys from "camelcase-keys";
import { Component, Vue, Emit } from "vue-property-decorator";

import Tasks from "@/components/Tasks.vue";
import Markdown from "@/components/Markdown.vue";
import Confirm from "@/components/Confirm.vue";

import api from "../api";
import * as utils from "../utils";

@Component({
  components: {
    Tasks,
    Markdown,
    Confirm
  }
})
export default class ContestHome extends Vue {
  tasks = [
    {
      id: "",
      title: ""
    }
  ];
  errorMessage = "";
  alert = false;
  snackbar = false;
  batchFucntionId: number | null = null;
  snackbarText = "コピーしました";
  teamInfo = {
    vsLiveshareLink: null,
    name: null,
    title: null,
    id: null
  };
  connecting = false;
  submitValid = true;
  questionValid = true;
  submitTaskId = null;
  defaultQuestionText =
    "### 概要\n\n### 試したこと\n- 箇条書きで書く\n- \n";
  questionText = this.defaultQuestionText;
  questionTitle = "";
  questionsHeaders = [
    {
      text: "問題番号",
      value: "task",
      width: "100px"
    },
    {
      text: "質問",
      value: "id",
      align: "left"
    },
    {
      text: "コメント",
      value: "commentHTML",
      align: "left"
    },
    {
      text: "消費ポイント",
      value: "point",
      align: "right"
    },
    {
      text: "提出時刻",
      value: "time",
      align: "right"
    },
    {
      text: "状態",
      value: "status",
      align: "right"
    }
  ];
  submissionHeaders = [
    {
      text: "問題番号",
      value: "task",
      width: "100px"
    },
    {
      text: "得点",
      value: "point",
      align: "right"
    },
    {
      text: "提出回数",
      value: "count",
      align: "right"
    },
    {
      text: "提出時刻",
      value: "time",
      align: "right"
    },
    {
      text: "状態",
      value: "status",
      align: "right"
    }
  ];
  questions = [
    {
      task: "",
      id: "",
      comment: "",
      point: 0,
      link: null,
      status: "",
      title: ""
    }
  ];
  submissions = [
    {
      id: "",
      point: null,
      time: "",
      count: "",
      status: "",
      task: ""
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
    title: null,
    start: 0,
    end: 0
  };
  maxSubmitNumber = 3;

  async retriveInformation() {
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
      this.submissions = camelcaseKeys(result.submissions);
      this.questions = camelcaseKeys(result.questions);
    } catch (error) {
      console.log(error);
    }
  }

  created(): void {
    const curPath = this.$route.path;
    const sleep = (msec: number) =>
      new Promise(resolve => setTimeout(resolve, msec));
    const intervalRepeater = async (
      callback: { (): void },
      repeat?: boolean
    ) => {
      if (repeat == undefined) repeat = true;
      while (curPath == this.$route.path && repeat) {
        let interval = 30 * 1000;
        if (this.isSubmissionsPendingExists || this.isQuestionsPendingExists)
          interval = 10 * 1000;
        await Promise.all([callback(), sleep(interval)]);
      }
    };
    intervalRepeater(this.retriveInformation);
  }

  get isSubmissionsPendingExists() {
    return this.submissions.some(item => item.status == "pending");
  }

  get isQuestionsPendingExists() {
    return this.questions.some(item => item.status == "pending");
  }

  get contestId() {
    return this.$route.params.contestId;
  }

  get teamId() {
    return this.$route.params.id;
  }

  get submittableTasks() {
    const acceptedTasks = new Set(
      this.submissions
        .filter(item => item.status == "accepted")
        .map(item => item.task)
    );
    return this.tasks
      .map((item: { id: string; title: string }, index: number): {
        text: string;
        value: string;
      } => {
        return {
          text: String.fromCodePoint(index + 65) + "." + item.title,
          value: item.id
        };
      })
      .filter(item => !acceptedTasks.has(item.value));
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

  @Emit("on-submit-click")
  onSubmitClick() {
    const isContestFinished = () =>
      new Date().getTime() > new Date(this.contestInfo.end).getTime();
    const numSubmits = () =>
      this.submissions.filter(item => item.task == this.submitTaskId).length;
    const isPendingExists = () =>
      this.submissions
        .filter(item => item.task == this.submitTaskId)
        .some(item => item.status == "pending");
    const isAcceptedExists = () =>
      this.submissions
        .filter(item => item.task == this.submitTaskId)
        .some(item => item.status == "accepted");

    if (
      !(this.$refs.submitForm as Vue & { validate: () => boolean }).validate()
    )
      return;

    this.errorMessage = "";
    this.alert = false;
    if (isContestFinished())
      this.errorMessage = "コンテストは終了しました。お疲れ様でした。";
    else if (numSubmits() >= this.maxSubmitNumber)
      this.errorMessage = "提出は3回までしかできません。";
    else if (isPendingExists())
      this.errorMessage = "審議中の問題は提出できません。";
    else if (isAcceptedExists())
      this.errorMessage = "解答が完了した問題は提出できません。";

    if (this.errorMessage) {
      this.alert = true;
      utils.scrollToElementById("forms");
      return;
    }

    (async () => {
      try {
        this.connecting = true;
        const response = await api.post("/v1/submissions/", {
          task: this.submitTaskId,
          team: this.teamId
        });
        this.submissions.push(camelcaseKeys(response.data));
        utils.scrollToElementById("submissions");
      } catch (error) {
        this.requestErrorHandler(error);
      }
      this.connecting = false;
    })();
  }

  @Emit("request-question")
  requestQuestion() {
    if (
      !(this.$refs.questionForm as Vue & { validate: () => boolean }).validate()
    ) {
      this.questionText = this.defaultQuestionText;
      return;
    }

    (async () => {
      try {
        if (
          !this.submitTaskId &&
          !(await (this.$refs.confirm as Vue & {
            open: (
              title: string,
              text: string,
              option: { color: string }
            ) => Promise<boolean>;
          }).open(
            "確認",
            "問題に関連しない質問は別のチームも閲覧することができます。<br>本当に質問を送信しますか？",
            {
              color: "orange"
            }
          ))
        ) {
          return;
        }
        this.connecting = true;
        const response = await api.post("/v1/questions/", {
          task: this.submitTaskId,
          team: this.teamId,
          title: this.questionTitle,
          text: this.questionText
        });
        this.questions.push(camelcaseKeys(response.data));
        utils.scrollToElementById("questions");
      } catch (error) {
        this.requestErrorHandler(error);
      }
      this.connecting = false;
    })();
  }

  @Emit("clear-selection")
  clearSelection() {
    this.submitTaskId = null;
  }

  @Emit("error-handler")
  requestErrorHandler(error: { response: { code: number } }) {
    if (error.response) {
      const message = utils.getErrorMessage(error.response.code);
      if (message) {
        this.errorMessage = message;
        this.alert = true;
        utils.scrollToElementById("forms");
      }
    }
  }

  @Emit("get-submission-number")
  getSubmissionNumber(target: { id: string; task: string }): number {
    const counter: { [key: string]: number } = new Proxy(
      {},
      {
        get: (t: { [key: string]: number }, name: string) =>
          name in t ? t[name] : 0
      }
    );
    const summary = this.submissions
      .filter(item => item.task == target.task)
      .reduce(function(
        acc: { [key: string]: number },
        item: { id: string; task: string }
      ): { [key: string]: number } {
        acc[item.id] = ++counter[item.task];
        return acc;
      },
      {});
    return summary[target.id] || 0;
  }

  @Emit("shorten")
  shorten(text: string, len?: number) {
    return utils.shorten(text, len);
  }

  @Emit("get-icon")
  getIcon(status: string) {
    if (status == "accepted") return "mdi-check";
    else if (status == "pending") return "mdi-timer-sand-full";
    else return "mdi-cancel";
  }

  @Emit("get-color")
  getColor(status: string) {
    if (status == "accepted") return "green";
    else if (status == "pending") return "orange";
    else return "red";
  }

  @Emit("get-task-char")
  getTaskChar(id: string) {
    if (!id) return "";
    const index = this.tasks.findIndex(seek => seek.id == id);
    return String.fromCodePoint(index + 65);
  }

  @Emit("get-comment-html")
  getCommentHTML(item: { comment: string; link: string }) {
    if (!item.comment) return "";
    if (!item.link) return this.shorten(item.comment, 14).replace("%%%HINT%%%", "");
    return this.shorten(item.comment, 14).replace(
      "%%%HINT%%%",
      `<a href="${item.link}" target="_blank" rel="noopener">ヒント</a> `
    );
  }

  @Emit("get-time-elapsed")
  getTimeElapsed(strDateTime: string) {
    return utils.getTimeElapsed(this.contestInfo.start, strDateTime);
  }
}
</script>

<style scoped>
.table-card {
  width: 80%;
  margin: 10px 0;
  padding: 10px 20px;
}

.gray-link {
  color: gray !important;
}
</style>