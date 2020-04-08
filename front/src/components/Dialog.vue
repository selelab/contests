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
      <v-container style="max-width: 600px;">
        <v-timeline dense clipped>
          <v-slide-x-transition group>
            <v-timeline-item
              v-for="event in timeline"
              :key="event.id"
              class="mb-4"
              color="pink"
              small
            >
              <v-row justify="space-between">
                <v-col cols="7" v-text="event.text"></v-col>
                <v-col class="text-right" cols="5" v-text="event.time"></v-col>
              </v-row>
            </v-timeline-item>
          </v-slide-x-transition>

          <v-timeline-item class="mb-4" color="light-green" small>
            <v-row justify="space-between">
              <v-col cols="7">提出 2/3回</v-col>
              <v-col class="text-right" cols="5">21:30 JST</v-col>
            </v-row>
          </v-timeline-item>

          <v-timeline-item fill-dot class="white--text mb-12" color="grey" large>
            <template v-slot:icon>
              <span>bot</span>
            </template>
            <v-row justify="space-between">
              <v-col cols="7" style="color: #333;">1件の誤りがあります。</v-col>
              <v-col class="text-right" style="color: #333;" cols="5">21:27 JST</v-col>
            </v-row>
          </v-timeline-item>

          <v-timeline-item class="mb-4" color="red" small>
            <v-row justify="space-between">
              <v-col cols="7">提出 1/3回</v-col>
              <v-col class="text-right" cols="5">21:25 JST</v-col>
            </v-row>
          </v-timeline-item>

          <v-timeline-item color="grey" small>
            <v-row justify="space-between">
              <v-col cols="7">競技開始</v-col>
              <v-col class="text-right" cols="5">21:00 JST</v-col>
            </v-row>
          </v-timeline-item>
        </v-timeline>
      </v-container>
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
