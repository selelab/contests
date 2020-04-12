<template>
  <div>
    <div>問題一覧</div>
    <v-card
      class="task-card"
      v-for="(task, index) in tasks"
      :key="index"
    >
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
</template>

<script lang="ts">
import { Component, Vue, Emit, Prop } from "vue-property-decorator";

import Markdown from "@/components/Markdown.vue";

@Component({
  components: {
    Markdown
  }
})
export default class Tasks extends Vue {
  @Prop({ default: null })
  tasks!: { id: string; title: string; subTitle: string; text: string }[];
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
