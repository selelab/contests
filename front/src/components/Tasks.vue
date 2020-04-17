<template>
  <div>
    <div>問題一覧</div>
    {{ hoge }}
    <div v-for="(task, index) in tasks" :key="index">
      <v-card class="task-card" v-if="submittableTaskIds.indexOf(task.id) != -1">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title
              class="headline"
            >{{`${(String.fromCodePoint(index + 65))}. ${task && task.title}`}}</v-list-item-title>
            <v-list-item-subtitle>{{task && task.subTitle}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-card-text>
          <Markdown :src="task.text"></Markdown>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

import Markdown from "@/components/Markdown.vue";

@Component({
  components: {
    Markdown
  }
})
export default class Tasks extends Vue {
  @Prop({ default: null })
  tasks!: { id: string; title: string; subTitle: string; text: string }[];

  @Prop({ default: null })
  submittableTasks!: { value: string }[];

  get submittableTaskIds() {
    if (!this.submittableTasks) return [];
    return this.submittableTasks.map((item: { value: string }): string => {
      return item.value;
    });
  }
}
</script>

<style scoped>
.task-card {
  width: 90%;
  padding-bottom: 20px;
  margin: 10px auto;
  display: inline-block;
}
</style>
