<template>
  <div :id="randomId" class="editor"></div>
</template>

<script lang="ts">
import { onMounted, defineComponent, watchEffect } from "@vue/composition-api";

import * as ace from "brace";
import "brace/mode/javascript";
import "brace/theme/monokai";

type Props = {
  value: string;
  editable: boolean;
};

export default defineComponent({
  props: {
    value: {
      type: String,
      default: ""
    },
    editable: {
      type: Boolean,
      default: true
    }
  },
  setup(props: Props, { emit }) {
    const randomId =
      "editor-" +
      Math.random()
        .toString(32)
        .substring(2);
    onMounted(() => {
      const editor = ace.edit(randomId);
      editor.setOptions({
        maxLines: 30,
        mode: "ace/mode/javascript",
        tabSize: 2,
        useSoftTabs: true,
        readOnly: !props.editable
      });

      editor.$blockScrolling = Infinity;
      editor.setTheme("ace/theme/monokai");
      editor.setValue(props.value);
      editor.clearSelection();

      if (props.editable) {
        editor.getSession().on("change", function() {
          const val = editor.getSession().getValue();
          if (props.value != val) emit("input", val);
        });
      }
    });

    watchEffect(() => {
      const editor = ace.edit(randomId);
      if (editor.getValue() != props.value) editor.setValue(props.value, -1);
    });
    return {
      randomId
    };
  }
});
</script>

<style lang="scss">
::-webkit-scrollbar {
  width: 0.5em;
  height: 0.5em;
}

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
}

::-webkit-scrollbar-thumb {
  border-radius: 0.5em;
  background: rgba(255, 255, 255, 0.8);
}

::-webkit-scrollbar-corner,
::-webkit-scrollbar-thumb:window-inactive {
  background: rgba(100, 100, 100, 0.4);
}
</style>