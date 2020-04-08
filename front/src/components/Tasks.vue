<template>
  <div>
    <div>問題一覧</div>
    <v-card class="task-card" v-for="(task, index) in tasks" :key="index" @click="onCardClick">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="headline">{{`${(index + 1)}. ${task.title}`}}</v-list-item-title>
          <v-list-item-subtitle>{{task.subTitle}}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-card-text>
        <Markdown :src="task.text"></Markdown>
      </v-card-text>
    </v-card>
    <Dialog
      v-bind:title="selectedTask.title"
      v-bind:subTitle="selectedTask.subTitle"
      v-bind:description="selectedTask.text"
      ref="dialog"
    ></Dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Emit } from "vue-property-decorator";

import Dialog from "@/components/Dialog.vue";
import Markdown from "@/components/Markdown.vue";

@Component({
  components: {
    Dialog,
    Markdown
  }
})
export default class Tasks extends Vue {
  tasks = [
    {
      title: "画面遷移",
      subTitle: "デバッグコンソールの使い方基礎",
      text:
        "## Idemque caede trementia stagna in timori vitamque\n\nLorem markdownum stravit, quia curae grates, saecula nec saepe hastile. Mihi ubi\ncum saniemque aeterna, [est terra](http://www.undaut.com/)?\n\n    driveRss = dataTokenIbm - error.eSurgeFile.wordart_bus(matrixMarkupMedia);\n    if (scanner(3, mampVramOop + urlEVpi, cdBox.batch_oem_serial(\n            faq_northbridge.vgaScrapingFragmentation(debug_print_trash,\n            965890)))) {\n        metafileIrcSearch /= kindle_zip_markup;\n    }\n    if (web.search(httpsSoa, box_hard_server.link_logic_repeater.ip_rom(5),\n            15)) {\n        load_ssid.ddr_intelligence_gateway += 2;\n    } else {\n        mouseSmartphone(software(editor));\n        nodeCapacity += trackball_header(usPort, 2);\n    }\n    if (forum >= andRecycleHtml) {\n        c -= bin_and_bcc + textMedia;\n    } else {\n        spooling(num_metadata, ultraPort);\n    }\n    if (teraflops <= rootEsports) {\n        wired_power.double.flashPhreaking(friend_byte);\n        token.wizardPowerRgb += 5 + client_wildcard_isa;\n    }\n\n## Ambobus non Vidi\n\nTuas hostibus Taurusque obtulimus donec egerere? Cruoris esse extrema, nescis\nobscurum; iubet solidum femina, ante, pendebant.\n\n- Quod arduus fundit senectae tegminis spes propositique\n- Limbus in levis Alcmenae in et omnis\n- Iactatam iuncta lucosque ad dedit latet incerta\n- Proiecerat alebat vixque\n\nIuvenes Tereus, pisces vina fratribus [nunc est](http://www.manum.io/lupi)\npennis, vultus Lethaea et demum flumina utque se castris? Nempe in credite\ndiemque usu sit vota origine illa populi iecit capillos Haemonia. Dextra tum\ndigitis aenea dei cultro virgo doque partu tulit et\n[toto](http://vocefalsa.org/). Veneri ignara, terras ne dedit et superos dixit;\ntoto corpora omnes misistis letali submovet dextroque placebant arcus, respicit?\n\n## Illo mihi agros se cornibus versat harenae\n\nDescendere Threicio ardor coctilibus poterat tellus, hic libro hos et. Terga\nSaturnius rupti virgo pieros confusaque, Meriones ceu; iniecique ambitiosa. Erat\nad labra Proetidas sibi corpore, mutatus navita, hostem? Ad cum temporis cernis\net sensit plenissima, est formosissima mora; ora est senesque tellure nostris\ntransit. Inplevi ipsum, in metuam mensis et oleis,\n[idem](http://me.org/ille.php) canes nudare cara qua eadem pondere si pressa\nAchaidas augur.\n\n> Tenax milite effugies querenda annis **in terra est** sensit adhaeret; in\n> *sibi aetas versa* eburnea et femina *iuvenis*. Factum ille! Nec unam\n> servabant, Aeaeae comes: cum etiam fallis, precibus raptam hirtus corque,\n> pondere. Pavent concordant imagine Iovi *erat dura quoque*, fuit Lacon grata\n> meum per!\n\nIamdudum qui honore bicolor ne soletur incepti scissaque laticem quem, quondam!\nFormamque praemia ab gelido illa; nomina Abantiades in vidi partes **eadem**,\nmisit, o. Est corpore draconem. Est erat iuvenemque sentit quod est a aperire\npraeter, ex ille utilitas.\n\nSic foret mixtaque patitur invitae viginti saepe iram parentum sic silvis\npostquam perque: amari unam [superorum](http://omnes-quas.org/). Ira laevo\nmelius supplentur erat bitumine amplexus ulla ausum membra ingentem. Temporis\nagebat tibi ora petunt genitor silvis nec quam nympha per Medusaei. Aurum hic,\nhoc rumpere palmis *licet* Spercheides locum nec regionibus caput omnipotens."
    },
    {
      title: "スマホ対応",
      subTitle: "レスポンシブデザインの基礎",
      text:
        "`/kusatsu/app/#/users` のユーザ一覧からユーザ詳細画面に遷移した際、詳細情報が画面に出力されない。デバックコンソールのネットワークの項目を注視し、これを解決せよ。"
    },
    {
      title: "機能実装",
      subTitle: "仕様書からアプリケーションを構築する",
      text:
        "`/kusatsu/app/#/users` のユーザ一覧からユーザ詳細画面に遷移した際、詳細情報が画面に出力されない。デバックコンソールのネットワークの項目を注視し、これを解決せよ。"
    }
  ];
  selectedTask = this.tasks[0];
  isDialogOpen = false;

  @Emit("card-click")
  onCardClick() {
    console.log("card clicked");
    (this.$refs.dialog as Vue & { open: () => null }).open();
  }
}
</script>

<style scoped>
.task-card {
  max-width: 344px;
  width: 90%;
  padding-bottom: 20px;
  margin: 10px;
  display: inline-block;
}
</style>
