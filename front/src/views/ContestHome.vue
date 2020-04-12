<template>
  <div class="contest">
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h2>{{contestInfo.title}}</h2>
    <div>
      開始 {{strStartDateTime}}
      <br />
      終了 {{strEndDateTime}}
    </div>
    <div>
      <h3>順位表</h3>
      <v-data-table
        :headers="headers"
        :items="contestInfo.teams"
        hide-default-footer
        class="elevation-1"
      >
        <template v-slot:item.name="{ item }">
          <router-link :to="'/' + contestId + '/teams/' + item.id" v-if="item.id">{{ item.name }}</router-link>
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
      </v-data-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Emit, Vue } from "vue-property-decorator";
import api from "../api";
import camelcaseKeys from "camelcase-keys";

@Component
export default class ContestHome extends Vue {
  contestInfo = {
    title: null,
    start: 0,
    end: 0,
    teams: []
  };
  headers = [
    {
      text: "チーム名",
      align: "start",
      sortable: false,
      value: "name"
    },
    { text: "合計得点", value: "points" },
    {
      text: "解答数",
      align: "center",
      value: "taskIndex"
    },
    { text: "最終提出時間", value: "lastSubmissionTime" }
  ];
  created(): void {
    (async () => {
      try {
        const result = (await api.get(`/v1/contests/${this.contestId}/`)).data;
        this.contestInfo = result;
        this.contestInfo.teams = camelcaseKeys(this.contestInfo.teams);
      } catch (error) {
        console.log(error);
      }
    })();
  }

  get contestId() {
    return this.$route.params.id;
  }

  get strStartDateTime() {
    return (
      this.contestInfo.start &&
      new Date(this.contestInfo.start).toLocaleString()
    );
  }

  get strEndDateTime() {
    return (
      this.contestInfo.end && new Date(this.contestInfo.end).toLocaleString()
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
        disabled: true,
        href: "/contests/" + this.contestId
      }
    ];
  }

  @Emit("get-color")
  getColor(points: number) {
    if (points > 200) return "red";
    else if (points > 100) return "orange";
    else return "green";
  }
}
</script>

<style lang="scss" scoped>
a {
  color: gray !important;
}
</style>