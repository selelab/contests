<template>
  <v-dialog v-model="isOpen">
    <v-card width="100%">
      <v-card-title>
        <span class="headline">{{ title }}</span>
        <v-btn icon absolute right>
          <v-icon color="grey lighten-1">mdi-send</v-icon>
        </v-btn>
      </v-card-title>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title v-text="subTitle"></v-list-item-title>
        </v-list-item-content>

        <v-list-item-action></v-list-item-action>
      </v-list-item>

      <v-card-text>
        <br />
        <br />
        <Markdown :src="description"></Markdown>
      </v-card-text>
      <v-card-actions>
        <v-spacer />

        <v-btn class="mx-0" depressed @click="comment">提出</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Emit, Prop } from "vue-property-decorator";

import Markdown from "@/components/Markdown.vue";

@Component({
  components: {
    Markdown
  }
})
export default class Dialog extends Vue {
  @Prop({ default: "" })
  title!: string;

  @Prop({ default: "" })
  subTitle!: string;

  @Prop({ default: "" })
  description!: string;

  isOpen = false;
  events: {
    id: number;
    text: string | null;
    time: string;
  }[] = [];
  text = null;
  nonce = 0;

  @Emit("dialog-open")
  open() {
    this.isOpen = true;
  }

  @Emit("dialog-close")
  close() {
    this.isOpen = false;
  }

  @Emit("send-comment")
  comment() {
    const time = new Date().toTimeString();
    const eventPayload: {
      id: number;
      text: string | null;
      time: string;
    } = {
      id: this.nonce++,
      text: this.text,
      time: time.replace(/:\d{2}\sGMT-\d{4}\s\((.*)\)/, (match, contents) => {
        return ` ${contents
          .split(" ")
          .map((v: string) => v.charAt(0))
          .join("")}`;
      })
    };

    this.events.push(eventPayload);

    this.text = null;
  }

  get timeline() {
    return this.events.slice().reverse();
  }
}
</script>

<style>
</style>
