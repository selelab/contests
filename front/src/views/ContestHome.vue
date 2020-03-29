<template>
  <div class="contest">
    <h2>第{{ contestId }}回 オンラインハッカソン</h2>
    <div>
      開始 2020-4-22 21:00
      <br />終了 2020-4-22 23:00
    </div>
    <div>
      <h3>順位表</h3>
      <v-data-table :headers="headers" :items="desserts" class="elevation-1">
        <template v-slot:item.teamName="{ item }">
          <router-link :to="'/' + contestId + '/teams/' + item.teamName">{{ item.teamName }}</router-link>
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

@Component
export default class ContestHome extends Vue {
  contestId = "";
  headers = [
    {
      text: "チーム名",
      align: "start",
      sortable: false,
      value: "teamName"
    },
    { text: "合計得点", value: "points" },
    {
      text: "解答数",
      align: "center",
      value: "taskIndex"
    },
    { text: "最終提出時間", value: "lastSubmissionTime" }
  ];
  desserts = [
    {
      teamName: "アイスクリームサンド	",
      points: 237,
      taskIndex: 3,
      lastSubmissionTime: "1:23"
    },
    {
      teamName: "フローズンヨーグルト",
      points: 159,
      taskIndex: 2,
      lastSubmissionTime: "1:43"
    },
    {
      teamName: "豆腐",
      points: 56,
      taskIndex: 1,
      lastSubmissionTime: "0:31"
    }
  ];
  created(): void {
    this.contestId = this.$route.params.id;
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