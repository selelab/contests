<template>
  <div class="contest">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h2>{{contestInfo.title}}</h2>
    <div>
      開始時刻 {{strStartDateTime}}
      <br />
      終了時刻 {{strEndDateTime}}
    </div>
    <div>
      <h3>順位表</h3>
      <v-data-table
        :headers="headers"
        :items="contestInfo.teams"
        :options="options"
        hide-default-footer
        class="elevation-1"
      >
        <template v-slot:item.name="{ item }">
          <router-link
            :to="'/' + contestId + '/teams/' + item.id"
            v-if="item.id && isContestFinished"
          >{{ item.name }}</router-link>
          <div v-else>{{ item.name }}</div>
        </template>
        <template v-slot:item.points="{ item }">
          <v-chip :color="getColor(item.points)" dark>{{ item.points }}</v-chip>
        </template>
        <template v-slot:item.taskIndex="{ item }">
          <v-chip v-if="item.taskIndex==3" color="light-green" dark>
            <v-icon left>mdi-check</v-icon>
            {{ item.taskIndex }}
          </v-chip>
          <div v-else style="text-align: center">{{ item.taskIndex }}</div>
        </template>
        <template
          v-slot:item.lastSubmissionTime="{ item }"
        >{{getTimeElapsed(item.lastSubmissionTime)}}</template>
      </v-data-table>
      <br />

      <h3 id="questions">質問の回答一覧</h3>
      <v-card class="table-card" flat>
        <v-data-table
          :headers="questionsHeaders"
          :items="questions"
          hide-default-footer
          :items-per-page="questions.length"
          class="elevation-1"
        >
          <template v-slot:item.status="{ item }">
            <v-icon :color="getStatusColor(item.status)">{{getStatusIcon(item.status)}}</v-icon>
          </template>
          <template v-slot:item.comment="{ item }">
            {{shorten(item.comment, 20)}}
          </template>
          <template v-slot:item.id="{ item }">
            <a
              class="gray-link"
              :href="`/contests/1/questions/${item.id}`"
              target="_blank"
              rel="noopener"
              v-if="!!item.id"
            >{{shorten(item.title, 20)}}</a>
          </template>
          <template v-slot:item.point="{ item }">{{item.point || "一"}}</template>
          <template v-slot:item.time="{ item }">{{getTimeElapsed(item.dateCreated)}}</template>
        </v-data-table>
      </v-card>
      <br />
    </div>
  </div>
</template>

<script lang="ts">
import camelcaseKeys from "camelcase-keys";

import { Component, Emit, Vue } from "vue-property-decorator";

import api from "../api";
import * as utils from "../utils";

@Component
export default class ContestHome extends Vue {
  contestInfo = {
    title: null,
    start: 0,
    end: 0,
    teams: [],
    tasks: []
  };
  options = {
    sortBy: ["points", "taskIndex", "lastSubmissionTime"],
    sortDesc: [true, false, false]
  };
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
  headers = [
    {
      text: "チーム名",
      align: "start",
      sortable: false,
      value: "name"
    },
    {
      text: "合計得点",
      value: "points",
      align: "center"
    },
    {
      text: "解答数",
      align: "center",
      value: "taskIndex"
    },
    {
      text: "最終提出時間",
      value: "lastSubmissionTime",
      align: "center",
      sort: (a: string | null, b: string | null) => {
        if (!a) return 1;
        if (!b) return -1;
        return new Date(a).getTime() - new Date(b).getTime();
      }
    }
  ];
  questionsHeaders = [
    {
      text: "質問",
      value: "id",
      align: "left"
    },
    {
      text: "コメント",
      value: "comment",
      align: "left"
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

  async retrieveInformation() {
    try {
      const result = (await api.get(`/v1/contests/${this.contestId}/`)).data;
      this.contestInfo = result;
      this.contestInfo.teams = camelcaseKeys(this.contestInfo.teams);

      this.questions = camelcaseKeys((await api.get("/v1/questions/")).data);
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
        const interval = 30 * 1000;
        await Promise.all([callback(), sleep(interval)]);
      }
    };
    intervalRepeater(this.retrieveInformation);
  }

  get contestId() {
    return this.$route.params.id;
  }

  get strStartDateTime() {
    return (
      this.contestInfo.start &&
      utils.convertDateToString(this.contestInfo.start)
    );
  }

  get strEndDateTime() {
    return (
      this.contestInfo.end && utils.convertDateToString(this.contestInfo.end)
    );
  }

  get isContestFinished() {
    const now = new Date().getTime();
    const end = new Date(this.contestInfo.end).getTime();

    return end <= now;
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
        disabled: true,
        href: "/contests/" + this.contestId
      }
    ];
  }

  @Emit("shorten")
  shorten(text: string, len?: number) {
    return utils.shorten(text, len);
  }

  @Emit("get-color")
  getColor(points: number) {
    if (points > 200) return "red";
    else if (points > 100) return "orange";
    else return "green";
  }

  @Emit("get-time-elapsed")
  getTimeElapsed(strDateTime: string) {
    return utils.getTimeElapsed(this.contestInfo.start, strDateTime) || "一";
  }

  @Emit("get-status-icon")
  getStatusIcon(status: string) {
    if (status == "accepted") return "mdi-check";
    else if (status == "pending") return "mdi-timer-sand-full";
    else return "mdi-cancel";
  }

  @Emit("get-status-color")
  getStatusColor(status: string) {
    if (status == "accepted") return "green";
    else if (status == "pending") return "orange";
    else return "red";
  }
}
</script>

<style lang="scss" scoped>
a {
  color: gray !important;
}
</style>