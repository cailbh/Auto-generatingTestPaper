<template>
  <div id="root">
    <!-- <button1 ref="button1"></button1>
    <button v-on:click="clickHandler">按钮</button> -->
    <!-- <svg width="1200" height="1000"></svg> -->

    <div id="Container">
      <!-- <div id="Container-back"></div> -->
      <div id="head">

        <!-- <Head></Head> -->
      </div>
      <div id="allBody">
        <!-- <div id="controlPanel" class="panel"> -->
          <!-- <ControlPanel @getToolState="getToolState"></ControlPanel> -->
        <!-- </div> -->
        <div id="proListPanel" class="panel">
          <ProListPanel></ProListPanel>
        </div>

        <div id="proinputPanel" class="panel">
          <Proinput></Proinput> 
        </div>
        <div id="paperListPanel" class="panel">
          <PaperListPanel></PaperListPanel>
        </div>

        <div id="procPanel" class="panel">
          <ProcPanel></ProcPanel>
        </div>
        <!-- <div id="graphContainer" v-show="showGraph" class="panel">
          <Graph :toolsState="toolsState"></Graph>
        </div> -->
        
        <div id="paperContainerC" v-show="showGraph" class="panel">
        </div>
        <div id="indexContainer" v-show="showGraph" class="panel">
          <!-- <Paper :toolsState="toolsState"></Paper> -->
          <indexInput></indexInput>
        </div>
        <div id="paperContainer" v-show="showGraph" class="panel">
          <Paper :toolsState="toolsState"></Paper>
        </div>
        <div id="proConScatterContainer" v-show="showGraph" class="panel">
          <!-- <Paper :toolsState="toolsState"></Paper> -->
          <proConScatter></proConScatter>
        </div>
        <div id="proConSankeyContainer" v-show="showGraph" class="panel">
          <!-- <Paper :toolsState="toolsState"></Paper> -->
          <proConSankey></proConSankey>
        </div>
        <!-- <div id="overviewPanel" class="panel">
          <OverviewPanel></OverviewPanel>
        </div> -->
        <!-- <transition name="sceneTran"> -->

        <!-- <div id="editPanel" class="panel"  v-if='showEdit==true'>
          <EditPanel></EditPanel>
        </div> -->
        <div id="scatterPanel" class="panel">
          <!-- <Scatter></Scatter> -->
        </div>
        <div id="netPPanel" class="panel">
          <NetPPanel></NetPPanel>
        </div>
        <!-- </transition> -->
      </div>
    </div>
  </div>
</template>

<script>
import Head from "@/components/Header/index.vue";
import Graph from '@/components/Graph/index.vue';
import Paper from '@/components/PaperC/index';
import Proinput from '@/components/Proinput/index.vue';
import proConScatter from '@/components/proConScatter/index.vue';
import proConSankey from '@/components/proConSankey/index.vue';
import IndexInput from '@/components/Indexinput/index.vue';

import Scatter from '@/components/Scatter/index.vue';

import ProcPanel from '@/components/ProblemContentPanel/index.vue';
import ProListPanel from '@/components/ProblemsListContentPanel/index.vue';
import PaperListPanel from '@/components/PaperListContentPanel/index.vue';

import ControlPanel from '@/components/ControlPanel/index.vue'
import NetPPanel from '@/components/NetProblemPanel/index.vue';
import GroupJson from "@/assets/json/group.json";
import SetJson from "@/assets/json/quz.json";
import tools from "@/utils/tools.js";
export default {
  components: { Head, Graph, Scatter, ProcPanel, ProListPanel, NetPPanel, ControlPanel,Proinput,Paper,IndexInput,proConScatter,proConSankey,PaperListPanel },
  /* eslint-disable no-unused-vars */
  data() {
    return {
      problemsData: [],
      submissionsData: [],
      groupData: GroupJson,
      setTimeData: SetJson,
      conceptOri:'',
      allConcept:'',
      allProblem:'',
      allPaper:'',
      netData: [],
      problemRelByConcept: [],
      problemListByConcept: [],
      studentsData: [],
      conceptsData: [],
      SelectStudentList: [],
      conceptTree: [],
      proSetData: [],
      problemConceptData: [],
      userProblemData: [],
      toolsState: {},
      timer: null,
      showVideo: true,
      showGraph: true,
      showEdit: false,
      selectEntId: "0",
      selectEnt: "0",
      toolState: {},
      timeDur: "",
      videoTime: 0,
      windowWidth: document.documentElement.clientWidth, //实时屏幕宽度
      windowHeight: document.documentElement.clientHeight, //实时屏幕高度
      attrColorLightList:[
        "rgb(253, 174, 134)",
        "rgb(255, 184, 240)",
        "rgb(255, 173, 159)",
        "rgb(255, 208, 133)",
        "rgb(145, 226, 199)",
        "rgb(167, 158, 221)",
        "#ffd8b1",
      ],
      attrColorList:[
        "rgb(254, 33, 79)",
        "rgb(115, 230, 163)",
        "rgb(250, 210, 50)",
        "rgb(255, 120, 90)",
        "rgb(255, 159, 28)",
        "rgb(6, 214, 160)",
        "rgb(125, 98, 211)",
        "#b6a2f7",
      ],
      mcolor: [
        "rgb(255,60,60)",
        "rgb(155,20,100)",
        "rgb(255,83,255)",
        "rgb(200,100,50)",
        "rgb(235,135,162)",
        "rgb(200,200,102)",
        "rgb(255,178,101)",
        "rgb(63,151,134)",
        "rgb(83,155,255)",
        "rgb(50,200,120)",
        "rgb(2,50,200)",
        "rgb(0,122,244)",
        "rgb(150,122,244)",
        "rgb(168,168,255)",
        "rgb(200,200,200)",
      ],
      mLigntcolor: [
        "#ff9c9c",
        "#cc88b0",
        "#ffa8ff",
        "#e3b097",
        "#f4c3d0",
        "#f4f4d0",
        "#ffd8b1",
        "#9ecac2",
        "#a8ccff",
        "#97e3ba",
        "#6f8be0",
        "rgb(0,122,244)",
        "#b6a2f7",
        "rgb(168,168,255)",
        "rgb(200,200,200)",
      ],
      marge: {
        top: 6,
        right: 10,
        bottom: 16,
        left: 6,
      },
    };
  },
  watch: {
    toolState(val) {
      if (val == 'edit')
        this.showEdit = true;
      else
        this.showEdit = false;
    },
    selectEnt(val) {
      this.selectEntId = val;
    },
    timeDur() {
    },
    cube_data() {
      this.$nextTick(() => { });
    },
    cluData() {
      this.$nextTick(() => {
      });
    },
  },
  methods: {

    getAllProblems() {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/problem/allProblem", { params: { } }, {})
        .then((response) => {
          _this.allProblem = response.body;
          this.$bus.$emit("allProblems", _this.allProblem);
        });
    },
    getAllPapers() {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/paper/allPaper", { params: { } }, {})
        .then((response) => {
          _this.allPaper = response.body;
          this.$bus.$emit("allPapers", _this.allPaper);
        });
    },
    getAllConcepts() {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/concept/ConceptOri", { params: { } }, {})
        .then((response) => {
          _this.ConceptOri = response.body;
          this.$bus.$emit("ConceptOri", _this.ConceptOri);
        });
      this.$http
        .get("/api/concept/allConcept", { params: { } }, {})
        .then((response) => {
          _this.allConcept = response.body;
          this.$bus.$emit("allConcepts", _this.allConcept);
        });
    },
    getAllData() {
      const _this = this;
      this.getAllProblems();
      this.getAllPapers();
      this.getAllConcepts();
    }
  },
  created: function () {
    var _this = this;
  },
  mounted() {
    const _this = this;
    this.$el.style.setProperty("--heightStyle", this.windowHeight + "px");
    this.getAllData();
    this.$bus.$emit("attrColorlist", _this.attrColorLightList);
    this.$bus.$emit("allProblem", _this.allProblem);
    // this.showVideo = true;
    // this.$bus.$emit("groupData", _this.groupData);
    // this.toolState = {
    //   "addRel": false,
    //   "addRelMain": false,
    //   "delRel":false,
    // }
    this.$bus.$on('SelectedStu', (val) => {
    });
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  }
};
</script>

<style>
@import '../../assets/style/home.css';
</style>