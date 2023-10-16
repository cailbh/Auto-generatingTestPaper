<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="proinput" ref="proinputDiv">
    <div class="panelHead">p</div>
    <div id="proinput" class="panelBody">
      <div class="mt-4">
        <el-form :model="proForm" label-position="left" label-width="50px">
          <el-form-item label="Title">
            <el-input v-model="proForm.name" />
          </el-form-item>
          <el-form-item label="Type">
            <el-select v-model="proForm.type" placeholder="please select your zone">
              <el-option label="选择题" value="1" />
              <el-option label="判断题" value="2" />
              <el-option label="填空题" value="3" />
              <el-option label="编程题" value="4" />
            </el-select>
          </el-form-item>
          <el-form-item label="" label-position="top">
            <el-input v-model="proForm.content"  :autosize="{ minRows: 18, maxRows: 80 }" type="textarea" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">Create</el-button>
            <el-button>Cancel</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <!-- <div id="moveLeft" ref="moveproinputLeft"></div>
                    <div id="moveRight" ref="moveproinputRight"></div> -->
    <!-- <div id="assistproinputPanel" class="panel">
        <div class="panelHead"></div>
      </div> -->
    <!-- <div id="zoomInDiv" @click="zoomInLayoutClk">
      <img class="icons" :src="zoomInUrl">
    </div>
    <div id="zoomOutDiv" @click="zoomOutLayoutClk">
      <img class="icons" :src="zoomOutUrl">
    </div>
    <div id="editToolDiv" @click="editToolClk">
      <img class="icons" :src="editToolUrl">
    </div> -->
  </div>
</template>
  
<script>
// import { param } from 'server/api';
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
      proName: '',
      proType: "",
      select: '',
      proForm: {
        name:"",
        type:"",
        content:""
      },


      data: '',
      proinputHeight: 0,
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
      proinputGTransformK: 1,
      proinputGTransformX: 10,
      proinputGTransformY: 10,
      proinputSvgScale: 1
    };
  },

  watch: {
    type(val) {
    },
    toolAddRel(val) {
    },
    toolsState: {
      deep: true,
      handler(val) {
        console.log(val)
        this.toolAddRel = val['addRel'];
        this.toolAddRelMain = val['addRelMain'];
        this.toolDelRel = val['delRel'];
      }
    }
  },
  methods: {
    onSubmit(){
      const _this = this;
      console.log(_this.proForm);
      _this.getProblemsKP(_this.proForm);
    },
    
    getProblemsKP(proForm) {
      const _this = this;
      let data = [];
      this.$http
        // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
        .post("/api/test", {params:{pro: proForm}}, {})
        .then((response) => {
          console.log(response.body);
        });
    },
    drawMain(svg) {
      let _this = this;
      let data = _this.data;
      let margin = _this.margin;

      let width = _this.width - margin.left - margin.right;
      let height = _this.height - margin.top - margin.bottom;

      let proinputGTransformX = _this.proinputGTransformX;
      let proinputGTransformY = _this.proinputGTransformY;
      let proinputGTransformK = _this.proinputGTransformK;
      let groups = svg.append("g").attr("id", "groups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + proinputGTransformX + ',' + proinputGTransformY + ") scale(" + proinputGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "backG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "arcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "relG").attr("width", width).attr("height", height);
      let entSetG = groups.append("g").attr("id", "entSetG").attr("width", width).attr("height", height);
      let entbySetG = groups.append("g").attr("id", "entbySetG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "frontG").attr("width", width).attr("height", height);

      _this.arcG = arcG;
      _this.entG = entG;
      _this.entSetG = entSetG;
      _this.entbySetG = entbySetG;
      _this.relG = relG;
      _this.frontG = frontG;
      let interval = _this.circleInterval;


      let scalePre = _this.proinputSvgScale;
      let stx = 0;
      let sty = 0;
      let stk = 1;
      var proinputZoom = d3.zoom()
        .scaleExtent([0, 100])
        .on("start", (e) => {
          sty = e.transform.y;
          stx = e.transform.x;
          stk = e.transform.k;
        })
        .on('zoom', (e) => {
          proinputGTransformX = _this.proinputGTransformX //+ e.transform.x - stx;
          proinputGTransformY = _this.proinputGTransformY + e.transform.y - sty;
          proinputGTransformK = _this.proinputGTransformK //+ e.transform.k - stk;
          _this.updataPro_ProSetRel(proinputGTransformY);
          // _this.updataPro_ProSelfRel(proinputGTransformY);
          entbySetG.attr('transform', 'translate(' + (proinputGTransformX) + ',' + (proinputGTransformY) + ') scale(' + (proinputGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.proinputGTransformX = proinputGTransformX;
          _this.proinputGTransformY = proinputGTransformY;
          _this.proinputGTransformK = proinputGTransformK;
          entbySetG.attr('transform', 'translate(' + (proinputGTransformX) + ',' + (proinputGTransformY) + ') scale(' + (proinputGTransformK) + ')')
        });
    },
    drawTxt(svg, x, y, text, fill, fontsize = 12, idN, an = 'start') {
      let txt = svg.append("text")
        .attr("y", y)
        .attr("x", x)
        .attr("id", idN)
        .attr("fill", fill)
        .attr("font-size", fontsize)
        .style("text-anchor", an)
        .text(text)
      return txt;
    },
    drawLine(svg, path, stroke, width, stroke_dasharray = "0", opacity, idName, className, fill = 'none') {
      d3.select(`#${idName}`).remove();
      let line = svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .style("stroke-opacity", opacity)
        .attr('fill', fill)
      return line;
    },
    drawRect(svg, x, y, w, h, rx, fill, strokeWidth, stroke, opacity, idName, className, strokeDasharray = '0') {
      d3.select(`#${idName}`).remove();
      let rect = svg.append("rect")
        .attr("x", x)
        .attr("y", y)
        .attr("width", w)
        .attr("height", h)
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("fill", fill)
        .attr("rx", rx)
        .attr("stroke", stroke)
        .attr("stroke-width", strokeWidth)
        .attr("stroke-dasharray", strokeDasharray)
      return rect;
    },
    drawPathLine(svg, path, stroke, width, stroke_dasharray = "0", idName, className) {
      svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .attr('fill', 'none')
    },
    drawCircle(svg, x, y, r, fill, opacity, stroke, width, className = 'entCircle', idName) {
      const _this = this;
      const oData = _this.data
      let circle = svg.append("circle")
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", r)
        .attr('stroke', stroke)
        .attr('stroke-width', width)
        .attr("fill", fill)
      return circle;
    },

    drawArc(svg, x, y, arcPath, stroke, fill, className, stroke_dasharray = "0", width = 3) {
      svg.append("path")
        .attr("d", arcPath)
        .attr("class", className)
        .attr("transform", "translate(" + x + "," + y + ")")
        .attr("stroke", stroke)
        .attr('stroke-width', width)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr("stroke-linejoin", "round")
        .attr("fill", fill)
    },
    getMaxMin(data, attrname) {
      return [
        Math.max.apply(Math, data.map(function (d) { return d[attrname]; })),
        Math.min.apply(Math, data.map(function (d) { return d[attrname]; }))
      ]
    },
    updataproinput() {
      var _this = this;
      let margin = _this.margin
      let width = _this.$refs.proinputDiv.offsetWidth - margin.left - margin.right;
      let height = document.getElementById("proinputPanel").clientHeight - margin.top - margin.bottom;
      _this.width = width;
      _this.height = height;
      d3.select("#proinputPanel").select("svg").remove()
      var svg = d3.select("#proinputPanel").append("svg")
        .attr("width", width)
        .attr("height", height);
      _this.rootSvg = svg;
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
    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
    });
    // this.$refs.moveproinputLeft.addEventListener("mouseover", _this.moveproinputLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
