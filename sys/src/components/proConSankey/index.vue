<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="proConSankey" ref="proConSankeyDiv">
    <div class="panelHead"></div>
    <div id="proConSankeyCantain" class="panelBody" ref="proConSankeyCantain">
    </div>

    <!-- <div class="close" ref="listen">
    </div> -->
    <!-- <el-button type="primary" @click="onSubmit">Create</el-button> -->
    <!-- <div class="proConSankeyTooltip toolTip">
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
</div></template>
<script>
// import { param } from 'server/api';
import * as d3 from 'd3'
import * as d3Sankey from 'd3-sankey'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
// import TestJson from "@/assets/json/case2_fin.json";
// import TestRelJson from "@/assets/json/case2_fin_rel.json";
import Circle from '@/utils/geometry/circle';
import tools from "@/utils/tools.js";
// import "@/utils/sankey.js";
import drawTools from "@/utils/drawingTools.js";

export default {
  props: ["toolsState"],
  data() {
    return {
      proName: '',
      ConceptOri:'',
      sankeyNodeData:'',
      sankeyLinkData:'',
      curPaperSankeyData:"",
      sankeyData: '',
      allProblems: '',
      allConcepts: '',
      allProInConGPTSankeyData: '',
      allproConSankeyData: '',
      proType: "",
      select: '',
      proForm: {
        name: "",
        type: "",
        content: ""
      },
      attrColorlist: [],
      rootSvg: '',
      width: 0,
      height: 0,
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
    // sankeyData: {
    //   deep: true,
    //   handler(val) {
    //     console.log(val)
    //     this.updataAll();
    //   }
    // },
    sankeyNodeData(){
      
        this.updataAll();
    }
  },
  methods: {
    getAllSankeyData() {
      const _this = this;
    //   _this.sankeyData ={
    //     "nodes": [
    //       { "name": "A" },
    //       { "name": "B" },
    //       { "name": "C" },
    //       { "name": "D" },
    //       ],
    //   "links": [
    //     {'source':0,'target':2,'value':"110"},
    //     {'source':0,'target':3,'value':"5"},
    //     {'source':1,'target':2,'value':"4"},
    //     {'source':1,'target':3,'value':"2"},

    //   ]
    // }
      this.$http
        .get("/api/sankeyData", { params: {} }, {})
        .then((response) => {
          _this.sankeyLinkData = response.body;
          _this.getAllSankeyNodeData();
        });
      // this.$http
      //   .get("/api/concept/allproConSankeyData", { params: {} }, {})
      //   .then((response) => {
      //     _this.allproConSankeyData = response.body;
      //     console.log("allproConSankeyData",response.body);
      //     // _this.allRelationships = response.body;
      //     // _this.drawnetPData();
      //   });
    },
    
    getAllSankeyNodeData() {
      const _this = this;
      let nodes = [];
      let conOri = _this.ConceptOri;
      let sankeyLinkData = _this.sankeyLinkData;
      let j = 0;
      let max = 0;
      for(let i=0;i<conOri.length;i++){
        nodes.push(conOri[i]);
        j++;
      }
      for(let i=0;i<sankeyLinkData.length;i++){
        let target = sankeyLinkData[i]['target'];
        if(target>max){max=target;}
      }
      let i=0;
      console.log(conOri, 2131313,j,max,nodes)
      while(j<=max){
        nodes.push({"name":`con${i}`});
        i++;
        j++
      }
      _this.sankeyNodeData = nodes;

    },
    drawProConSankey(svg) {
      const _this = this;
      const margin = _this.margin;
      let psvg = svg
      let width = psvg.attr("width");
      let height = psvg.attr("height");
      psvg.select("#netPG").remove();
      // let prog = psvg.append("g").attr("id", "netPG").attr("width", width).attr("height", height);
      let groups = svg.append("g").attr("id", "proConSankeyGroups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      // this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "proConSankeybackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "proConSankeyarcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "proConSankeyrelG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "proConSankeyentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "proConSankeyfrontG").attr("width", width).attr("height", height);

      // let scatterData = _this.scatterData;
      // let xMaxMinDR = tools.getMaxMin(scatterData, 'x');
      // let yMaxMinDR = tools.getMaxMin(scatterData, 'y');
      // let scatterxLinear = d3.scaleLinear().domain([xMaxMinDR[1], xMaxMinDR[0]]).range([0, width]);
      // let scatteryLinear = d3.scaleLinear().domain([yMaxMinDR[1], yMaxMinDR[0]]).range([0, height / 2]);
      let colorList = _this.attrColorlist;
      var node = _this.sankeyNodeData
      var lk = _this.sankeyLinkData;
      let marge = _this.margin;

      const nodeSort = function(a,b){
        return 0;
      }

      var sankey = d3Sankey.sankey()
        .nodeWidth(50)//每个资源块的水平像素宽度
        .nodePadding(0)//资源块间的纵向间距
        // .nodeAlign(d3Sankey.sankeyLeft) 
        .nodeSort(nodeSort)
        .size([width, height * 0.95]);
      let { nodes, links } = sankey({
        nodes: node.map(d => Object.assign({}, d)),
        links: lk.map(d => Object.assign({}, d))
            });
      // var path = sankey.link();
      var link = svg.append("g").selectAll(".link")
        .data(links)
        .enter().append("path")
        .attr("class", "link")
        .attr("id", "san")
        .attr("fill","rgba(255, 0, 0,0)")
        .attr("stroke", "rgba(132, 132, 132,0.3)")
        .attr("stroke-width", d => d.width)
        .style("mix-blend-mode", "multiply")
        .attr("d", d3Sankey.sankeyLinkHorizontal())//链接的路径设置已经被sankey封装了，这里调用之后就可以生成连线呢的路径
        //下面这句生成线的宽度，//线的宽度按照线端点两端块较小者扩宽，但为啥偏移max(1, d.dy）？
        // .style("stroke-width", function (d) {
        //   return Math.max(1, d.dy);
        // })
        // .attr("transform", function (d) { return "translate(" + marge.left + "," + marge.top + ")"; })
        .sort(function (a, b) { return b.dy - a.dy; });//这句去掉效果一样不知为啥？
      //(5)sankey设置链接提示
      link.append("title")
        .text(function (d) { return d.source.name + " → " + d.target.name + "\n" + d.value; });

        const gradient = link.append("linearGradient")
        // .attr("id", d => (d.uid = DOM.uid("link")).id)
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", d => d.source.x1)
        .attr("x2", d => d.target.x0);
    gradient.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", d => colorList[parseInt(d.source.category)%colorList.length]);
    gradient.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", d => colorList[parseInt(d.target.category)%colorList.length]);

      //(6)拖动
      var node = svg.append("g").selectAll(".node")
        .data(nodes)
        .enter().append("g")
        .attr("class", "node")
        // .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; })

        .call(d3.drag()
          .on("drag", dragmove));
      //(7)块
      node.append("rect")
        .attr("id", "san")
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("height", d => (d.y1 - d.y0))
        .attr("width", (d) =>{
          let rectWidth = d.x1 - d.x0;
          if(d.index<=24){
            let lay =  parseInt(d.lay);
           rectWidth += (rectWidth/3)*(1-lay);
          }
          return rectWidth})
        // .text(d => `${d.name}\n${d.value.toLocaleString()}`)
        // .attr("height", function (d) { return d.dy; })
        // .attr("width", sankey.nodeWidth())//刚才设置的块的宽度  
        // .attr("transform", function (d) { return "translate(" + marge.left + "," + marge.top + ")"; })
        .style("fill", function (d) {
          let colorIndex =parseInt(d.index-25)%colorList.length;
          if(d.index<=24){
            colorIndex = parseInt(d.rootFatherIndex);
          }
          // na = d.name.substr(0, d.name.length - 1)
          // if (na == 'ori') {
          //   return mcolor[parseInt(d.name.substr(3)) - 1];
          // }
          // else {
            return colorList[colorIndex];
          // }
        }
        )
        // .style("stroke", function (d) { 
        //   if(d.index<=24)
        //   return d3.rgb(d.color).darker(0.1); })//较深
        .append("title")
        .text(function (d) { return d.name + "\n" + d.value; });
      //(8)文字
      node.append("text")
        .attr("x", function (d) { 
          let rectWidth = d.x1 - d.x0;
          if(d.index<=24){
            let lay =  parseInt(d.lay);
           rectWidth += (rectWidth/3)*(1-lay);
          }
          return d.x0+rectWidth; })
        .attr("y", function (d) { return d.y0+(d.y1 - d.y0)/2; })
        .attr("dy", ".35em")
        .attr("id", "san")
        .attr("text-anchor", "end")//文字在左边（中轴右边的）
        .attr("transform", null)
        .text(function (d) { return d.name; })
        // .filter(function (d) { return d.x < width / 2; })//除去在中轴左边的 
        // .attr("x", 6 + sankey.nodeWidth())
        .attr("text-anchor", "start")//文字在右边
        // .attr("transform", function (d) { return "translate(" + marge.left + "," + marge.top + ")"; })
      // (9)拖动
      function dragmove(d) {
        d3.select(this).attr("transform", "translate(" + d.x + "," +
          (d.y = //下面的纵坐标调整值是怎么计算的？
            Math.max(0,
              Math.min(
                height - d.dy,
                d3.event.y
              ))) + ")");
        sankey.relayout();//重新布局,线上下的位置调整
        link.attr("d", path);//更新路径
      }



    },
    updataAll() {
      var _this = this;
      let margin = _this.margin
      let width = _this.$refs.proConSankeyDiv.offsetWidth - margin.left - margin.right;
      let height = _this.$refs.proConSankeyDiv.offsetHeight - margin.top - margin.bottom;
      _this.width = width;
      _this.height = height;
      d3.select("#proConSankeyCantain").select("svg").remove()
      var svg = d3.select("#proConSankeyCantain").append("svg")
        .attr("width", width - 0)
        .attr("height", height - 0)
        .attr('transform', 'translate(0,0)')
        .style("position", "absolute");

      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height);
      _this.rootSvg = svg;
      _this.drawProConSankey(svg);
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
      _this.getAllSankeyData();
      _this.updataAll();
    });
    this.$bus.$on('ConceptOri', (val) => {
      _this.ConceptOri = val;
    });
    this.$bus.$on('attrColorlist', (val) => {
      _this.attrColorlist = val;
    });
    this.$bus.$on('curPaperSankeyData', (val) => {
      console.log("curPaperSankeyData",val)
      _this.curPaperSankeyData = val[0].link;
      _this.sankeyLinkData = _this.curPaperSankeyData;
      _this.updataAll();
    });

    // this.$refs.moveproConSankeyLeft.addEventListener("mouseover", _this.moveproConSankeyLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
