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
          <v-card-text v-if="codeLog">
            <h4 class="my-3">コンソール出力</h4>
            <div v-for="(log, key) in codeLog" :key="key">
              {{ log.strStack }}
              <editor v-model="log.message" :editable="false" :maxLines="5" :showGutter="false" v-if="log" />
            </div>
          </v-card-text>
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
import { defineComponent, ref, Ref, computed } from "@vue/composition-api";
import Editor from "@/components/Editor.vue";

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
    const execInfo: Ref<{
      result: string;
      logData: {
        message: string;
        stack: { name: string; line: number; column: number }[];
      }[];
    } | null> = ref(null);
    const codeError: Ref<Error | null> = ref(null);
    const params = ref(initialParams);
    const entrypoint = "filterByName";

    const codeResult = computed(
      () => execInfo.value && JSON.stringify(execInfo.value.result, null, "  ")
    );
    const codeLog = computed(() => {
      if (!(execInfo.value && execInfo.value.logData && execInfo.value.logData.length)) return null;
      return execInfo.value.logData.map(item => {
        const { message, stack } = item;
        return {
          message: JSON.stringify(message, null, "  "),
          strStack: stack.reduce((acc, item) => {
            if (!acc) return `@${item.name}:${item.line}:${item.column}`;
            return `(${acc})@${item.name}:${item.line}:${item.column}`;
          }, "")
        };
      });
    });

    const runCode = function() {
      const prefixLines = 3;
      execInfo.value = null;
      codeError.value = null;
      const oldLog = console.log;
      try {
        const sandboxPrefix = `const oldLog = console.log;
        const makeLogger = (entrypoint, logData) => ((message) => {
          try {
            throw Error('');
          } catch(error) {
            const stack = error.stack.split('\\n');
            const epIndex = stack && stack.findIndex(
              (item) => (item.match(entrypoint.name))
            );
            const scopedStack = stack.slice(0, epIndex + 1).map(
              (item) => {
                const match = item.match(/(?<=<anonymous>):(?<line>\\d+):(?<column>\\d+)/);
                const { line, column } = (match && match.groups) || { line: 2, column: -1 };
                return { name: item.replace('    at ', '').split(/[ \\/@]/)[0], line: parseInt(line) - ${prefixLines}, column: parseInt(column) }
              }
            ).filter(
              (item) => (item.line > 0)
            );

            const data = { message, stack: scopedStack };
            logData.push(data);
            const strScopedStack = scopedStack.reduce(
              (acc, item) => {
                if (!acc) return \`@\${item.name}:\${item.line}:\${item.column}\`;
                return \`(\${acc})@\${item.name}:\${item.line}:\${item.column}\`;
              },
              ''
            );
            oldLog(\`\${data.message} \${strScopedStack}\`);
          }
        });

        const evaluater = (entrypoint) => (...value) => {
          const logData = new Array();
          const logger = makeLogger(entrypoint, logData);
          console.log = logger;
          const data = { result: entrypoint(...value), logData };
          console.log = oldLog;
          return data;
        };
        `;
        const sandboxCode = `'use strict';${sandboxPrefix.replace(
          /\n/g,
          ""
        )};\n${code.value};return(evaluater(${entrypoint}))`;
        const sandboxFunc = Function(sandboxCode)();
        const sandboxParams = Object.values(params.value).map(value => {
          return Function(`'use strict';return(${value})`)();
        });
        execInfo.value = sandboxFunc(...sandboxParams);
      } catch (error) {
        console.log = oldLog;
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
      codeLog,
      runCode,
      entrypoint,
      code,
      params
    };
  }
});
</script>
