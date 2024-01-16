<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="paper" ref="paperDiv">
    <div class="panelHead"></div>
    <div id="paperPanel" class="panelBody">
      <el-menu  class="el-menu-demo" mode="horizontal" @select="handleSelectProType">
        <el-menu-item index="1">选择题</el-menu-item>
        <el-menu-item index="2">判断题</el-menu-item>
        <el-menu-item index="3">填空题</el-menu-item>
        <el-menu-item index="4">编程题</el-menu-item>
      </el-menu>
      <div id="problemListPanel" ref="problemListPanel">
        <div class="proItem" v-for="proItem in proList" :key="proItem.id">
          <template v-if="showProType.indexOf(proItem.type) >= 0">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>{{ proItem.title }}</span>
                <el-button style="float: right; padding: 3px 0" type="text"
                  @click="click_ProDel(proItem.id)">删除</el-button>
              </div>
              <!-- <div v-for="o in 4" :key="o" class="text item"> -->
              <div v-html="proItem.content"></div>
              <!-- </div> -->
            </el-card>
          </template>
        </div>
      </div>
      <!-- <div class="chartTooltip toolTip">
        <p>
          <br /><strong class="name toolTipAttr"></strong>
          <br /><strong class="text toolTipAttr"></strong>
          <br /><strong class="attr0 toolTipAttr"></strong>
          <br /><strong class="attr1 toolTipAttr"></strong>
          <br /><strong class="attr2 toolTipAttr"></strong>
          <br /><strong class="attr3 toolTipAttr"></strong>
          <br /><strong class="attr4 toolTipAttr"></strong>
        </p>
      </div> -->
    </div>
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
// import TestJson from "@/assets/json/case2_fin.json";
// import TestRelJson from "@/assets/json/case2_fin_rel.json";
import tools from "@/utils/tools.js";

export default {
  props: ["toolsState"],
  data() {
    return {
      data: '',
      paperHeight: 0,
      allPapers: "",
      proIdList: [],
      proList: [],
      paperSelectedData:'',
      showProType: [],
      toolAddRel: false,
      toolAddRelMain: false,
      toolDelRel: false,
      detailsEntPro: [],
      SelectingStudentId: "",
      SelectingConId: "",
      SelectingProId: "",
      groupData: [],
      SelectStudentList: [],
      problemsData: [],
      proSetOriData: [],
      submissionsData: [],
      maxSetCon: 0,
      studentsData: [],
      conceptsData: [],
      conceptTree: [],
      proSetData: [],
      interY: 10,
      problemConceptData: [],
      createdProblemConceptData: [],
      userProblemData: [],
      proMaxMinDR: [],
      proMaxMinDC: [],
      proAttrList: [],
      proAttrMaxMinList: [],
      conMaxMinDR: [],
      conMaxMinDC: [],
      conAttrList: [],
      conAttrMaxMinList: [],
      Ent_problem: [],
      Ent_concept: [],
      entG: "",
      entSetG: "",
      entbySetG: "",
      relG: "",
      frontG: "",
      curProblemId: '',
      curConceptId: '',
      curProblemSetId: '',
      selectProblemId: '',
      selectConceptId: '',
      proX: 450,
      proY: 30,
      setWidth: 300,
      setX: 830,
      setY: 30,
      treeX: 50,
      treeY: 30,
      proStepY: 0,
      conStepY: 0,
      rootSvg: null,
      groupsSvg: null,
      arcG: null,
      curEntId: '',
      minDImportance: 0,
      maxDImportance: 0,
      minDRelevance: 0,
      maxDRelevance: 0,
      maxDDuration: 0,
      maxTotalDuration: 0,
      videoDuration: 672,
      totalDuration: 1000,
      importanceColor_linear: null,
      importanceCompute_color: null,
      relevanceScale_linear: null,
      paperGTransformK: 1,
      paperGTransformX: 10,
      paperGTransformY: 10,
      paperSvgScale: 1
    };
  },

  watch: {
    type(val) {
    },
    toolAddRel(val) {
    },
    allPapers(val) {
      const _this = this;
      let idList = [];
      for (let i = 0; i < val.length; i++) {
        if (val[i]['Selected']) {
          for (let t = 0; t < 4; t++) {
            let tp = `type${t}`;
            for (let d = 0; d < val[i][tp].length; d++) {
              idList.push(val[i][tp][d])
            }
          }
            _this.proIdList = idList;
          break;
        }
      }
    },
    paperSelectedData(val){
      const _this = this;
      let idList = [];
      // for (let i = 0; i < val.length; i++) {
      //   if (val[i]['Selected']) {
          for (let t = 0; t < 4; t++) {
            let tp = `type${t}`;
            for (let d = 0; d < val[tp].length; d++) {
              idList.push(val[tp][d]+"")
            }
          }
            _this.proIdList = idList;
      //   }
      // }
    },
    toolsState: {
      deep: true,
      handler(val) {
        this.toolAddRel = val['addRel'];
        this.toolAddRelMain = val['addRelMain'];
        this.toolDelRel = val['delRel'];
      }
    },
    proIdList(val) {
      const _this = this;
      _this.$bus.$emit("proIdList", val);
      _this.getProById(val);
    },
    proList(val) {
      this.updatePaper();
    }
  },
  methods: {
    getProById(proIds) {
      let pro = '';
      const _this = this;
      this.$http
        .get("/api/problem/problemById", { params: { proIds: proIds } }, {})
        .then((response) => {
          pro = response.body;
          _this.proList = pro;
        });

      return pro;
    },
    click_ProDel(val) {
      const _this = this;
      _this.proIdList.splice(_this.proIdList.indexOf(val), 1);
      // _this.$bus.$emit("proIdDelList", val);
    },
    handleSelectProType(val) {
      const _this = this;
      if (val == '1') {
        _this.showProType = ['MULTIPLE_CHOICE'];
      }
      if (val == '2') {
        _this.showProType = ['TRUE_OR_FALSE'];
      }
      if (val == '3') {
        _this.showProType = ['FILL_IN_THE_BLANK'];
      }
      if (val == '4') {
        _this.showProType = ['CODE_COMPLETION', 'PROGRAMMING'];
      }
    },
    updatePaper() {
      const _this = this;
      let proList = _this.proList;
      for(let i=0;i<proList.length;i++){
        proList[i].content = proList[i].content.toString().replaceAll("\n", "<br></br>");
      }
    },
    
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    var _this = this;
    let margin = _this.margin
    this.$nextTick(() => {
    });
  },
  mounted() {
    const _this = this;

    d3.select(".chartTooltip").classed("hidden", true);
    // _this.proIdList = ["1701115978840051712", "1697260400746143744"];

    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
    });
    this.$bus.$on('proIdList', (val) => {
      _this.proIdList = val;
    });
    // this.$bus.$on('allPapers', (val) => {
    //   _this.allPapers = val;
    // });
    this.$bus.$on('paperSelected', (val) => {
      _this.paperSelectedData = val;
    });
    // this.$refs.movepaperLeft.addEventListener("mouseover", _this.movepaperLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  }
} 
</script>

<style>
@import './index.css';
</style>
