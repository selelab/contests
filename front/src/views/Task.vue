<template>
  <div>
    <v-row>
      <v-col cols="12" sm="12" md="6" lg="6">
        <v-card>
          <v-card-title>プログラム</v-card-title>
          <v-card-text>
            <h4 class="my-3">{{entrypoint}}関数</h4>
            <v-alert dense outlined type="error" v-if="codeError">
              <h4>{{codeError.name}}</h4>
              {{ codeError.message }}
            </v-alert>
            <editor v-model="code" />
          </v-card-text>
          <v-list-item>
            <v-spacer />
            <v-btn class="my-3" @click="runCode">実行</v-btn>
          </v-list-item>
          <v-card-text v-if="codeResult">
            <h4 class="my-3">実行結果</h4>
            <editor v-model="codeResult" :editable="false" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="6" lg="6">
        <v-card>
          <v-card-title>引数の値</v-card-title>
          <v-card-text>
            <div v-for="(value, key) in params" :key="key">
              <h4 class="my-3">{{key}}</h4>
              <editor v-model="params[key]" />
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang='ts'>
import { defineComponent, ref, Ref } from "@vue/composition-api";
import Editor from "@/components/Editor.vue";
import axios from "axios";

const initialCode = `function filterByName(data) {
  console.log('hoge');
  const target = ['か', 'き', 'く', 'け', 'こ'];
  console.log('fuga');
  return data
    .filter(
      (item) => target.includes(item.cityKana[0])
    );
}
`;
const initialParams = {
  data: JSON.stringify(
    [
      { city: "千代田区", cityKana: "ちよだく" },
      { city: "中央区", cityKana: "ちゅうおうく" },
      { city: "港区", cityKana: "みなとく" },
      { city: "新宿区", cityKana: "しんじゅくく" },
      { city: "文京区", cityKana: "ぶんきょうく" },
      { city: "台東区", cityKana: "たいとうく" },
      { city: "墨田区", cityKana: "すみだく" },
      { city: "江東区", cityKana: "こうとうく" },
      { city: "品川区", cityKana: "しながわく" },
      { city: "目黒区", cityKana: "めぐろく" },
      { city: "大田区", cityKana: "おおたく" },
      { city: "世田谷区", cityKana: "せたがやく" },
      { city: "渋谷区", cityKana: "しぶやく" },
      { city: "中野区", cityKana: "なかのく" },
      { city: "杉並区", cityKana: "すぎなみく" },
      { city: "豊島区", cityKana: "としまく" },
      { city: "北区", cityKana: "きたく" },
      { city: "荒川区", cityKana: "あらかわく" },
      { city: "板橋区", cityKana: "いたばしく" },
      { city: "練馬区", cityKana: "ねりまく" },
      { city: "足立区", cityKana: "あだちく" },
      { city: "葛飾区", cityKana: "かつしかく" }
    ],
    null,
    "  "
  )
};

export default defineComponent({
  components: {
    Editor
  },
  setup() {
    const code = ref(initialCode);
    const codeResult = ref("");
    const codeError: Ref<Error | null> = ref(null);
    const params = ref(initialParams);
    const entrypoint = "filterByName";

    const runCode = function() {
      codeResult.value = "";
      codeError.value = null;
      try {
        const sandboxPrefix = `const oldLog = console.log;
        const loggedValues = [];
        const altLogger = (message) => {
            let obj = {};
            Error.captureStackTrace(obj, altLogger);
            const stack = obj.stack.split('\\n').slice(1);
            loggedValues.push({ message, stack });
            oldLog(message);
        };
        window.console.log = altLogger;
        const evaluater = (entrypoint) => (...value) => { return { result: entrypoint(...value), loggedValues } };
        `;
        const sandboxCode = `'use strict';${sandboxPrefix}${code.value};return(evaluater(${entrypoint}))`;
        const sandboxFunc = Function(sandboxCode)({ axios });
        const sandboxParams = Object.values(params.value).map(value => {
          return Function(`'use strict';return(${value})`)();
        });
        codeResult.value = JSON.stringify(
          sandboxFunc(...sandboxParams),
          null,
          "  "
        );
      } catch (error) {
        if (error instanceof Error) {
          codeError.value = error;
        } else {
          console.error(error);
        }
      }
    };

    return {
      codeResult,
      codeError,
      runCode,
      entrypoint,
      code,
      params
    };
  }
});
</script>
