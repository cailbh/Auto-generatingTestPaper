<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="proConScatter" ref="proConScatterDiv">
    <div class="panelHead"></div>
    <div id="proConScatterCantain" class="panelBody" ref="proConScatterCantain">
    </div>
    
    <!-- <div class="close" ref="listen">
    </div> -->
    <!-- <el-button type="primary" @click="onSubmit">Create</el-button> -->
    <div class="proConScatterTooltip toolTip">
      <p>
          <br /><strong class="name toolTipAttr"></strong>
          <br /><strong class="text toolTipAttr"></strong>
          <br /><strong class="attr0 toolTipAttr"></strong>
          <br /><strong class="attr1 toolTipAttr"></strong>
          <br /><strong class="attr2 toolTipAttr"></strong>
          <br /><strong class="attr3 toolTipAttr"></strong>
          <br /><strong class="attr4 toolTipAttr"></strong>
        </p>
    </div>
  </div>
</div></template>
  
<script>
// import { param } from 'server/api';
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
// import TestJson from "@/assets/json/case2_fin.json";
// import TestRelJson from "@/assets/json/case2_fin_rel.json";
import Circle from '@/utils/geometry/circle';
import tools from "@/utils/tools.js";
import drawTools from "@/utils/drawingTools.js";

export default {
  props: ["toolsState"],
  data() {
    return {
      proName: '',
      scatterData:'',
      allProblems:'',
      allConcepts:'',
      allProInConGPTScatterData:'',
      allproConScatterData:'',
      proType: "",
      select: '',
      proForm: {
        name: "",
        type: "",
        content: ""
      },
      attrColorlist:[],
      rootSvg:'',
      width:0,
      height:0,
      thisId: 10,
      margin: { top: 5, right: 5, bottom: 5, left: 5 },
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
    },
    scatterData(val){
      const _this = this;
      _this.updataAll();
    }
  },
  methods: {
    getAllScatterData() {
      const _this = this;
      this.$http
        .get("/api/problem/allProInConGPTScatterData", { params: {} }, {})
        .then((response) => {
          _this.allProInConGPTScatterData = response.body;
          console.log("allProInConGPTScatterData",response.body);
          _this.scatterData = _this.allProInConGPTScatterData;
          // _this.allRelationships = response.body;
          // _this.drawnetPData();
        });
      this.$http
        .get("/api/concept/allproConScatterData", { params: {} }, {})
        .then((response) => {
          _this.allproConScatterData = response.body;
          console.log("allproConScatterData",response.body);
          // _this.allRelationships = response.body;
          // _this.drawnetPData();
        });
    },
    drawProConScatter(svg) {
      const _this = this;
      const margin = _this.margin;
      let psvg = svg
      let width = psvg.attr("width");
      let height = psvg.attr("height");
      psvg.select("#netPG").remove();
      // let prog = psvg.append("g").attr("id", "netPG").attr("width", width).attr("height", height);
      let groups = svg.append("g").attr("id", "proConScatterGroups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      // this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "proConScatterbackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "proConScatterarcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "proConScatterrelG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "proConScatterentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "proConScatterfrontG").attr("width", width).attr("height", height);

      let scatterData = _this.scatterData;
      let xMaxMinDR = tools.getMaxMin(scatterData, 'x');
      let yMaxMinDR = tools.getMaxMin(scatterData, 'y');
      let scatterxLinear = d3.scaleLinear().domain([xMaxMinDR[1], xMaxMinDR[0]]).range([0, width]);
      let scatteryLinear = d3.scaleLinear().domain([yMaxMinDR[1], yMaxMinDR[0]]).range([0, height/2]);
      let colorList = _this.attrColorlist;
      const allProblems = _this.allProblems;
      const allConcepts = _this.allConcepts;
      for(let i=0;i<scatterData.length;i++){
        let x = scatterxLinear(scatterData[i]['x']);
        let y = scatteryLinear(scatterData[i]['y']);
        let type = scatterData[i]['type'];
        if(type == "kp"){
          let points = drawTools.calcRegularPolygonPoints(3, x, y, 8);
          let trigal = drawTools.drawPolygon(entG, points, `scatterCircle_${scatterData[i]['type']}_${scatterData[i]['id']}`, '0px', "grey", colorList[parseInt(scatterData[i]['kLab'])]);
          // drawTools.drawCircle(entG, x, y, 5, colorList[parseInt(scatterData[i]['kLab'])], 1, 1, 1, 'scatterCircle', `scatterCircle_${scatterData[i]['type']}_${scatterData[i]['id']}`);
          trigal.on("mousemove", function (d) {
          let ts = d3.select(this);
          let tp = ts.attr("id").split("_")[1]
          let id = ts.attr("id").split("_")[2];
          let ent = {}
          // 更新浮层内容
          let attr = ['title'];
          let attrN = ['title'];
          if(tp == 'pro'){
            ent = allProblems.find(function(p){return p['id'] == id});
            attr = ['title'];
            attrN = ['title'];
          }
          else if(tp == 'kp'){
            ent = allConcepts.find(function(c){return c['sortId'] == id});
            
            attr = ['name'];
            attrN = ['name'];
          }
          console.log('id',d);

          let nametext = '';
          // let ent = groupData.find(function (c) { return c['id'] == id });
          var yPosition = d.offsetY + 2;
          var xPosition = d.offsetX + 2;
          
          // if(d.clientX>2100){
          //   xPosition = d.clientX - 210;
          // }
          let nameText = ent['title'];
          var scatterTooltip = d3
            .select(".proConScatterTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          // 更新浮层内容
          for (let a = 0; a < attr.length; a++) {

            scatterTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]]}`)
          }
          scatterTooltip.select(".name").text(nameText);
          // 移除浮层hidden样式，展示浮层
          scatterTooltip.classed("hidden", false);
        }).on("mouseleave", function (d) {
          _this.$bus.$emit("SelectingStu", "");
          d3.select(".proConScatterTooltip").classed("hidden", true);
        })
        }
        else{
        let circle = drawTools.drawCircle(entG, x, y, 5, colorList[parseInt(scatterData[i]['kLab'])], 1, 1, 1, 'scatterCircle', `scatterCircle_${scatterData[i]['type']}_${scatterData[i]['id']}`);
        circle.on("mousemove", function (d) {
          let ts = d3.select(this);
          let tp = ts.attr("id").split("_")[1]
          let id = ts.attr("id").split("_")[2];
          let ent = {}
          // 更新浮层内容
          let attr = ['title'];
          let attrN = ['title'];
          if(tp == 'pro'){
            ent = allProblems.find(function(p){return p['id'] == id});
            attr = ['title'];
            attrN = ['title'];
          }
          else if(tp == 'kp'){
            ent = allConcepts.find(function(c){return c['sortId'] == id});
            
            attr = ['name'];
            attrN = ['name'];
          }
          console.log('id',d);

          let nametext = '';
          // let ent = groupData.find(function (c) { return c['id'] == id });
          var yPosition = d.offsetY + 2;
          var xPosition = d.offsetX + 2;
          
          // if(d.clientX>2100){
          //   xPosition = d.clientX - 210;
          // }
          let nameText = ent['title'];
          var scatterTooltip = d3
            .select(".proConScatterTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          // 更新浮层内容
          for (let a = 0; a < attr.length; a++) {

            scatterTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]]}`)
          }
          scatterTooltip.select(".name").text(nameText);
          // 移除浮层hidden样式，展示浮层
          scatterTooltip.classed("hidden", false);
        }).on("mouseleave", function (d) {
          _this.$bus.$emit("SelectingStu", "");
          d3.select(".proConScatterTooltip").classed("hidden", true);
        })
      }
      }


      let scatterConData = _this.allproConScatterData;
      let xconMaxMinDR = tools.getMaxMin(scatterConData, 'x');
      let yconMaxMinDR = tools.getMaxMin(scatterConData, 'y');
      let scatterConxLinear = d3.scaleLinear().domain([xconMaxMinDR[1], xconMaxMinDR[0]]).range([0, width]);
      let scatterConyLinear = d3.scaleLinear().domain([yconMaxMinDR[1], yconMaxMinDR[0]]).range([height/2, height-50]);
      for(let i=scatterConData.length-1;i>=0;i--){
        let x = scatterConxLinear(scatterConData[i]['x']);
        let y = scatterConyLinear(scatterConData[i]['y']);
        let color = colorList[parseInt(scatterConData[i]['kLab'])]
        if(parseInt(scatterConData[i]['id'])<19){
          color = 'red';
        }
        console.log(scatterConData[i])
        let circles = drawTools.drawCircle(entG, x, y, 5, color, 1, 1, 1, 'scatterConCircle', `scatterConCircle_${scatterConData[i]['id']}`);
        circles.on("mousemove", function (d) {
          let ts = d3.select(this);
          // let tp = ts.attr("id").split("_")[1]
          let id = ts.attr("id").split("_")[1];
          let ent = {}
          // 更新浮层内容
          let attr = ['name'];
          let attrN = ['name'];
          ent = scatterConData.find(function(c){return c['id'] == id});
          console.log('id',ent,id);

          let nametext = '';
          // let ent = groupData.find(function (c) { return c['id'] == id });
          var yPosition = d.offsetY + 2;
          var xPosition = d.offsetX + 2;
          
          if(d.offsetX>200){
            xPosition = d.offsetX - 210;
          }
          if(d.offsetY>600){
            yPosition = d.offsetY - 150;
          }
          let nameText = ent['name'];
          var scatterTooltip = d3
            .select(".proConScatterTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          // 更新浮层内容
          for (let a = 0; a < attr.length; a++) {

            scatterTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]]}`)
          }
          scatterTooltip.select(".name").text(nameText);
          // 移除浮层hidden样式，展示浮层
          scatterTooltip.classed("hidden", false);
        }).on("mouseleave", function (d) {
          _this.$bus.$emit("SelectingStu", "");
          d3.select(".proConScatterTooltip").classed("hidden", true);
        })
      }
    },
    updataAll() {
      var _this = this;
      let margin = _this.margin
      let width = _this.$refs.proConScatterDiv.offsetWidth - margin.left - margin.right;
      let height = _this.$refs.proConScatterDiv.offsetHeight - margin.top - margin.bottom;
      _this.width = width;
      _this.height = height;
      d3.select("#proConScatterCantain").select("svg").remove()
      var svg = d3.select("#proConScatterCantain").append("svg")
        .attr("width", width - 0)
        .attr("height", height - 0)
        .attr('transform', 'translate(0,0)')
        .style("position", "absolute");

      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height);
      _this.rootSvg = svg;
      _this.drawProConScatter(svg);
      // });
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
    _this.getAllScatterData();
    d3.select(".scatterTooltip").classed("hidden", true);
    d3.select(".chartTooltip").classed("hidden", true);
    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
    });
    this.$bus.$on('allProblems', (val) => {
      _this.allProblems = val;
    });
    this.$bus.$on('allConcepts', (val) => {
      _this.allConcepts = val;
      _this.updataAll();
    });
    this.$bus.$on('attrColorlist', (val) => {
      _this.attrColorlist = val;
    });
    
    // this.$refs.moveproConScatterLeft.addEventListener("mouseover", _this.moveproConScatterLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
