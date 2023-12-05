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
        <div id="procPanel" class="panel">
          <ProcPanel></ProcPanel>
        </div>
        <!-- <div id="graphContainer" v-show="showGraph" class="panel">
          <Graph :toolsState="toolsState"></Graph>
        </div> -->
        
        <div id="paperContainerC" v-show="showGraph" class="panel">
        </div>
        <div id="paperContainer" v-show="showGraph" class="panel">
          <Paper :toolsState="toolsState"></Paper>
        </div>
        <div id="indexContainer" v-show="showGraph" class="panel">
          <!-- <Paper :toolsState="toolsState"></Paper> -->
          <indexInput></indexInput>
        </div>
        <div id="proModelContainer" v-show="showGraph" class="panel">
          <!-- <Paper :toolsState="toolsState"></Paper> -->
          <proModel></proModel>
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
import proModel from '@/components/proModel/index.vue';
import IndexInput from '@/components/Indexinput/index.vue';

import Scatter from '@/components/Scatter/index.vue';

import ProcPanel from '@/components/ProblemContentPanel/index.vue';
import ProListPanel from '@/components/ProblemsListContentPanel/index.vue';

import ControlPanel from '@/components/ControlPanel/index.vue'
import NetPPanel from '@/components/NetProblemPanel/index.vue';
import GroupJson from "@/assets/json/group.json";
import SetJson from "@/assets/json/quz.json";
import tools from "@/utils/tools.js";
export default {
  components: { Head, Graph, Scatter, ProcPanel, ProListPanel, NetPPanel, ControlPanel,Proinput,Paper,IndexInput,proModel },
  /* eslint-disable no-unused-vars */
  data() {
    return {
      problemsData: [],
      submissionsData: [],
      groupData: GroupJson,
      setTimeData: SetJson,
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
    // getProblems() {
    //   const _this = this;
    //   let data = [];
    //   this.$http
    //     // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
    //     .get("/api/test", {}, {})
    //     .then((response) => {
    //       console.log(response.body);
    //     });
    // },
   
    getAllData() {
      const _this = this;
      // this.getProblems();
    }
  },
  created: function () {
    var _this = this;
  },
  mounted() {
    const _this = this;
    this.$el.style.setProperty("--heightStyle", this.windowHeight + "px");
    // this.showVideo = true;
    // this.$bus.$emit("groupData", _this.groupData);
    // this.toolState = {
    //   "addRel": false,
    //   "addRelMain": false,
    //   "delRel":false,
    // }
    this.getAllData();
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