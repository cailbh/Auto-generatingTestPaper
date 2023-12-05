<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="netPPanel">
    <div class="panelHead">Correlation View</div>
    <!-- //SupportPanel</div> -->
    <div id="netPPanelDiv" class="panelBody" ref="netPPanelDiv">
      <div id="topicLine" ref="topicLine"></div>
      <div id="netPData" ref="netPData"></div>

      <div class="netTooltip toolTip">
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
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
import tools from "@/utils/tools.js";
import drawTools from "@/utils/drawingTools.js";
import { tree } from 'd3';
import { SourceNode } from 'source-list-map';

export default {
  props: [],
  data() {
    return {
      problemsData:[],
      proIdList:[],
      relByPro:[],
      conByPro:[],
      typeRadio: "cell State",
      treeData: null,
      allRelationships: '',
      toolsState: '',
      proAttrList: [],
      selectedPro: [],
      selectedCon: '',
      proAttrMaxMinList: [],
      conAttrList: [],
      conAttrMaxMinList: [],
      problemsData: [],
      problemConceptData: [],
      problemRelByConcept: [],
      problemListByConcept: [],
      submissionsData: [],
      studentsData: [],
      conceptsData: [],
      netData: [],
      attrColorList: [],
      calcNetDataRady: 0,
      nameinput: "Fundamental Graphs",
      curEntId: "",
      insertEntId: "",
      EntProData: {},
      insertSourceEntId: "-1",
      insertTargetEntId: "-1",
      sonList: [],

      entProMinColor: "rgb(255,255,255)",
      entProMaxColor: "rgb(255, 0, 0)",

      entConMinColor: "rgb(255,255,255)",
      entConMaxColor: "rgb(46, 117, 182)",

      margin: { top: 5, right: 5, bottom: 5, left: 5 },
    };
  },
  watch: {
    typeRadio(val) {
    },
    netData() {
    },
    studentsData() {
      this.calcNetDataRady++;
    },
    problemsData() {
      this.calcNetDataRady++;
    },
    submissionsData() {
      this.calcNetDataRady++;
    },
    calcNetDataRady(val) {
      if (val == 3) {
        // this.calcNetData();
        // this.getProRel();
      }
    },
    type(val) {
    },
    // selectEnt(val){
    //   console.log(val);
    // },
    curEntId(curEntId) {
    }
  },
  methods: {
    getAllReltionship() {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/problem/allRelationship", { params: {} }, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          console.log("allRelationship", response.body);
          _this.allRelationships = response.body;
          // _this.drawnetPData();
        });
    },
    drawnetPData() {
      const _this = this;
      const margin = _this.margin;
      let width = this.$refs.netPData.offsetWidth - margin.left - margin.right;
      let height = this.$refs.netPData.offsetHeight - margin.top - margin.bottom;
      d3.select("#netPData").select("svg").remove();
      var svg = d3.select("#netPData").append("svg")
        .attr("id", "netPEnt")
        .attr("width", width)
        .attr("height", height);

      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height)
      //.attr("transform", "translate(1,320)");
      // _this.entG = entG;
      // _this.sonG = sonG;
      _this.drawProConNet(entG);
      _this.drawFigureAnnotation(svg);
    },
    drawProConNet(svg) {
      const _this = this;
      let psvg = svg
      let width = psvg.attr("width");
      let height = psvg.attr("height");
      psvg.select("#netPG").remove();
      // let prog = psvg.append("g").attr("id", "netPG").attr("width", width).attr("height", height);
      let groups = svg.append("g").attr("id", "groups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      // this.groupsSvg = groups;
 
      let backG = groups.append("g").attr("id", "proRbackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "proRarcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "proRrelG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "proRentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "proRfrontG").attr("width", width).attr("height", height);

      let problemConceptData = _this.relByPro;
      let conByPro = _this.conByPro;
      let proRel = tools.deepClone(_this.problemRelByConcept);
      let proInList = tools.deepClone(_this.problemListByConcept);
      let ent_edgeC = [];

      let ent_nodeC = [];
      let ent_nodeP = [];
      let ent_edgeP = [];
      let proId = _this.curEntId;
      // if (proId == "") { return; }
      // let proList = proInList[proId];
      let proList = proInList;
      console.log(111)
      console.log(proList, proRel,problemConceptData);
      let addEgList = { '0_0': [], "0_1": [], "1_0": [], "1_1": [] };
      // let conList = proRel[proId];
      let jagep= {};
      let jagec= {};
      for (let r = 0; r < problemConceptData.length; r++) {
        let curRel = problemConceptData[r];
        let pId = curRel['problemId'];
        let cId = curRel['conceptId'];
        // let type = curRel['type'];
        if(jagec[cId]!=1)
          ent_nodeP.push({ "id": cId, "type": "concept" });
        if(jagep[pId]!=1)
          ent_nodeP.push({ "id": pId, "type": "problem" });
        jagep[pId]=1;
        jagec[cId]=1;
        ent_edgeP.push({
          source: pId,
          target: cId,
          // type:type
        })
      }
      let svgWidth = width;
      let svgHeight = height;

      var forceSimulationP = d3.forceSimulation()
        .force("link", d3.forceLink().id((d) => { return d.id }))
        .force("charge", d3.forceManyBody().strength(-10))
        .force("center", d3.forceCenter(svgWidth / 2, svgHeight / 2));
      forceSimulationP.nodes(ent_nodeP)
        .on("tick");

      let disLinear = d3.scaleLinear().domain([0, 200]).range([svgWidth / 5, svgWidth / 50]);
      forceSimulationP.force("link")
        .links(ent_edgeP)
        .distance(disLinear(ent_nodeP.length + ent_edgeP.length));

      let rSize = 10;
      const drags = () => {

        function dragstarted(event, d) {
          if (!event.active) forceSimulationP.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }
        function dragged(event, d) {
          d.fx = event.x;
          d.fy = event.y;
          // d.rx = event.x;
          // d.ry = event.y;
        }

        function dragended(event, d) {
          if (!event.active) forceSimulationP.alphaTarget(0);
          d.fx = null;
          d.fy = null;
          // d.rx = event.x;
          // d.ry = event.y;
        }
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }

      var circle = frontG.selectAll('circle')
        .data(ent_nodeP)
        .enter()
        .append("circle")
        .attr("id", function (d) { return `asPro_${d.id}` })
        .attr("class", function (d) {
          return `c_${d.type}`
        })
        .attr("cx", function (d) {
          if (d.type == "problem")
            _this.drawEntityProblem(entG, d.x, d.y, `astPro_${d.id}`);
          else if (d.type == "concept")
            _this.drawEntityConcept(entG, d.x, d.y, `astPro_${d.id}`);
          return d.x;
        })
        .attr("cy", function (d) { return d.y })
        .attr("r", 25)
        .attr("opacity", "0")
        .call(drags())
        .on("click", function (d) {
        })
        .on("mousemove", function (d) {
          // 更新浮层内容
          // netTooltip.select(".name").text(clasN);
          // netTooltip.select(".text").text(nametext);
          // // 移除浮层hidden样式，展示浮层
          // netTooltip.classed("hidden", false);
        })
        .on("mouseleave", function (d) {

          _this.$bus.$emit("SelectingCon", '');
          _this.$bus.$emit("SelectingPro", '');

          d3.select(".netTooltip").classed("hidden", true);
        })
      // .call(drags());

      var path = relG.selectAll('.path')
        .data(ent_edgeP)
        .enter()
        .append('path')
        .attr("class", function (d) { return `"net_${d.type}-s-${d.source.id}-t-${d.target.id}` })
        .attr('d', function (d) {
          let eSource = d.source
          let eTarget = d.target
          let eSourceId = eSource['id']
          let eTargetId = eTarget['id']
          let startA = [eSource.x, eSource.y]
          let endA = [eTarget.x, eTarget.y]
          let path = d3.path()
          path.moveTo(startA[0], startA[1])
          path.quadraticCurveTo(startA[0], startA[1], endA[0], endA[1]);
          return path.toString()
        })
        .style('stroke', function (d) {
          if (d.type == 1) {
            return 'blue';
          }
          return "grey";
        })
        .style("stroke-opacity", "0.3")
        .style('stroke-width', function (d) {
          if ((d.source['id'] == proId) || (d.target['id'] == proId)) {
            return 4;
          }
          return 2;
        })

      forceSimulationP.on("tick", () => {
        circle.attr("cx", (d) => {
          if (d.rx != undefined) {
            d.x = d.rx;
            d.y = d.ry;
          }
          let esx = d.x;
          let esy = d.y;
          if (esx < rSize) esx = rSize;
          esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
          if (esy < rSize) esy = rSize;
          esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;

          _this.updateEntity(entG,esx,esy,`astPro_${d.id}`)

          if (d.x < rSize) return rSize;
          return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        })
          .attr("cy", (d) => {
            if (d.y < rSize) return rSize
            return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
          });

        path.attr("d", (d) => {
          // if (!((d.source.type == 'problem') && (d.target.type == 'problem'))) 
          if (!(d.type == 3)) {
            let eSource = d.source;
            let eTarget = d.target;
            let esx = eSource.x;
            let esy = eSource.y;
            if (esx < rSize) esx = rSize;
            esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
            if (esy < rSize) esy = rSize;
            esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;
            let etx = eTarget.x;
            let ety = eTarget.y;
            if (etx < rSize) etx = rSize;
            etx = etx > svgWidth - rSize ? svgWidth - rSize : etx;
            if (ety < rSize) ety = rSize;
            ety = ety > svgHeight - rSize ? svgHeight - rSize : ety;
            let path = d3.path();
            path.moveTo(esx, esy);
            path.quadraticCurveTo(esx, esy, etx, ety);
            return path.toString();
          }
        })

      });

    },

    drawEntityProblem(svg, x, y, pId) {
      const _this = this;
      d3.select("#" + pId).remove();
      let entG = svg.append("g").attr("id", pId);
      entG.attr("transform", `translate(${x},${y})`);
      drawTools.drawCircle(entG, 0, 0, 10, "red", 1, 1, 1, 'entCircle', pId) 
    },
    drawEntityConcept(svg, x, y, pId) {
      const _this = this;
      d3.select("#" + pId).remove();
      let entG = svg.append("g").attr("id", pId);
      entG.attr("transform", `translate(${x},${y})`);
      let points = drawTools.calcRegularPolygonPoints(3, 0, 0, 12);
      drawTools.drawPolygon(entG, points, `FigNet_Proc`, '1px', "grey", 'blue');
    },
    getControlPoints(startP, endP) {
      let conP = [];
      // return [(startP[0]+endP[0])/2,(startP[1]+endP[1])/2]
      return [(startP[0]), (endP[1])]
    },
    calclin(domin, toDomin, value) {
      let point_linear = d3.scaleLinear().domain([domin[0], domin[1]]).range([toDomin[0], toDomin[1]]);
      let rarc = point_linear(value);
      return rarc;
    },

    calcRsize(domin, value, r) {
      let point_linear = d3.scaleLinear().domain([0, domin[0]]).range([0, r]);
      let rarc = point_linear(value);
      return rarc;
    },
    calcattrPoint(totalNum, index, domin, value, x, y, r) {
      const _this = this;
      let arcStep = Math.PI * 2 / totalNum;
      let rarc = _this.calcRsize(domin, value, r);
      let point = [x - Math.sin(arcStep * index) * rarc, y + Math.cos(arcStep * index) * rarc];
      return point
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
    updateEntity(svg, x, y, pId) {
      const _this = this;
      console.log(pId)
      let entG = svg.select(`#${pId}`);
      let transformd = entG.attr("transform")
      let s = 'scale(1)';
      if (transformd.split("scale").length > 1) {
        s = `scale${transformd.split("scale")[1]}`;
      }
      entG.attr("transform", `translate(${x},${y}) ${s}`);
    },
    getProRel() {
      const _this = this;
      let problemsIdList = _this.proIdList;
      let conByPor = [];
      let problemConceptData = _this.allRelationships;
      // let pId = _this.curEntId;
      let proRel = []
      for (let c = 0; c < problemConceptData.length; c++) {
        let curPId = problemConceptData[c]['problemId'];
        let curCId = problemConceptData[c]['conceptId'];
        if (problemsIdList.indexOf(curPId)>0) {
          proRel.push(problemConceptData[c]);
          conByPor.push(curCId)
        }
      }
      console.log("rels",proRel);
      _this.relByPro = proRel;
      _this.conByPro = proRel;
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

    drawRect(svg, x, y, w, h, rx, fill, strokeWidth, stroke, opacity, idName, className) {
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
      return rect;
    },
    drawFigureAnnotation(svg) {
      const _this = this;
      let frontG = svg;

      let stuMaxColor = _this.stuMaxColor;
      let stuMinColor = _this.stuMinColor;

      let len = 6;

      let Color_linear = d3.scaleLinear().domain([0, len]).range([0, 1]);
      let Rsize_linear = d3.scaleLinear().domain([0, len]).range([1, 6]);
      let Compute_color = d3.interpolate(stuMinColor, stuMaxColor);

      let textsr = _this.drawTxt(frontG, 16, 15, "AcceptedRate", "black", 10, `FigNet_con`);
      let textat = _this.drawTxt(frontG, 16, 35, "Attempts", "black", 10, `FigNet_con`);
      let textbs = _this.drawTxt(frontG, 16, 55, "Connection nums", "black", 10, `FigNet_con`);

      let texttm = _this.drawTxt(frontG, 136, 15, "Concepts", "black", 10, `FigNet_con`);
      let textgn = _this.drawTxt(frontG, 136, 35, "problems", "black", 10, `FigNet_con`);
      let prex = 0;
      let prerx = 0;
      let colorar = _this.attrColorList[0];
      let colorat = _this.attrColorList[1];
      let colorcn = _this.attrColorList[2];

      let colortm = _this.entProMaxColor;
      let colorgn = _this.entConMaxColor;

      _this.drawRect(frontG, 1, 2, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectColoraB`, 'FigNet');
      _this.drawRect(frontG, 1, 5, 10, 12, 0, colorar, "1", "grey", "1", `FigNet_conRectColora`, 'FigNet');

      _this.drawRect(frontG, 1, 22, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectColorB`, 'FigNet');
      _this.drawRect(frontG, 1, 25, 10, 12, 0, colorat, "1", "grey", "1", `FigNet_conRectColor`, 'FigNet');

      _this.drawRect(frontG, 1, 42, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectB`, 'FigNet');
      _this.drawRect(frontG, 1, 45, 10, 12, 0, colorcn, "1", "grey", "1", `FigNet_conRect`, 'FigNet');

      drawTools.drawCircle(frontG, 120, 12, 7, colorgn, 1, "grey", "1", 'FigNet', `FigNet_conColorc`);

      let points = drawTools.calcRegularPolygonPoints(3, 120, 31, 9);

      let entPolygon = drawTools.drawPolygon(frontG, points, `FigNet_Proc`, '1px', "grey", colortm);

      let path1 = d3.path();
      // let points0 = [[10, 20], [10, 24], [14, 20], [10, 24], [14, 28], [10, 24], [10, 28], [10, 24], [40, 24], [40, 24], [36, 20], [40, 24], [36, 28], [40, 24], [40, 20], [40, 28]]
      // let points1 = [[10, 50], [10, 54], [14, 50], [10, 54], [14, 58], [10, 54], [10, 58], [10, 54], [40, 54], [40, 54], [36, 50], [40, 54], [36, 58], [40, 54], [40, 50], [40, 58]]
      // let points2 = [[10, 80], [10, 84], [14, 80], [10, 84], [14, 88], [10, 84], [10, 88], [10, 84], [40, 84], [40, 84], [36, 80], [40, 84], [36, 88], [40, 84], [40, 80], [40, 88]]
      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
      // .curve(d3.curveBasisClosed)
      // _this.drawLine(frontG, curve_generator(points0), "black", 1, '0', '1', `lineat`, 'FigNet_line1', "rgb(230,230,230)");
      // _this.drawLine(frontG, curve_generator(points1), "black", 1, '0', '1', `line2`, 'FigNet_line1', "rgb(230,230,230)");
      // _this.drawLine(frontG, curve_generator(points2), "black", 1, '0', '1', `line3`, 'FigNet_line1', "rgb(230,230,230)");
      for (let i = 0; i < len * 3; i++) {
      }
      for (let i = 0; i < len; i++) {
        // let color = Compute_color(Color_linear(i));
        // let circle = _this.drawCircle(frontG, 15 + prex, 23, Rsize_linear(i), color, 1, "red", "1", 'FigNet', `FigNet_conColor${i}`);
        // prex += Rsize_linear(i) * 2 + 4;
        // prerx += i * 4 + 2;
      }

    },

    updata() {
      const _this = this;
      _this.getProRel();
      // _this.getAllReltionship();
      _this.drawnetPData();

    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      // _this.calcNetData();
      
      // _this.getAllReltionship();
      _this.updata();
      d3.select(".netTooltip").classed("hidden", true);
      _this.drawnetPData();
    });
  },
  mounted() {
    const _this = this;
    
    _this.getAllReltionship();
    this.$bus.$on('proIdList', (val) => {
      _this.proIdList = val;
      _this.updata();
    });
    
    this.$bus.$on('allProblem', (val) => {
     _this.problemsData = val;
    });
  },
  // beforeDestroy() {
  //   clearInterval(this.moveTimer);
  // },
} 
</script>

<style>@import './index.css';</style>
