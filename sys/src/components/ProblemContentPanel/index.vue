<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="procPanel">
    <div class="panelHead">Content View </div>
      <!-- //SupportPanel</div> -->
    <div id="procPanelDiv" class="panelBody" ref="procPanelDiv">
      <div id="questionSer" ref="questionSer"></div>
      
        <el-table stripe  :data="tableData" style="width: 100%;height:80%;overflow-y: scroll;scrollbar-width: none;"         
        :row-style="iRowStyle"
        :cell-style="iCellStyle"
        :header-row-style="iHeaderRowStyle"
        :header-cell-style="iHeaderCellStyle">
          <!-- <el-table-column prop="key" label="" width="190">
          </el-table-column> -->
          <!-- eslint-disable -->
          <el-table-column prop="value" label="" width="480">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Title'">
                <div style="float: left;height: 40px;font-size: 24px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>

              </div>
              <div v-if="scope.row.key == 'Type'">
                <!-- <div style="float: left;height:15px;font-size: 17px;"> -->
                <div style="float: left;height: auto;;font-size: 20px;color: rgb(103, 103, 103);">
                  {{ `${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'ContentT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Content'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'InputT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Input'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'OutT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Out'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
            </template>
          </el-table-column>
          <!-- eslint-enable -->
        </el-table>
      <!-- <div id="connectCon" ref="connectCon">
      </div> -->
      <div id="procData" ref="procData">

      </div>
    </div>
    </div>
</template>
  
<script>
import * as d3 from 'd3'
import tools from "@/utils/tools.js";

export default {
  props: [],
  data() {
    return {
      typeRadio: "cell State",
      treeData: null,
      toolsState: '',
      problemsData:[],
      problemConceptData:[],
      conceptTree:[],
      // confirmUrl: require("@/assets/img/confirm.svg"),
      // cancelUrl: require("@/assets/img/cancel.svg"),
      // toolsButsUrl: require("@/assets/img/toolsButs.png"),
      // addNodeSonUrl: require("@/assets/img/addNode1.png"),
      // addNodePerUrl: require("@/assets/img/addNode2.png"),
      // addLinkBasicUrl: require("@/assets/img/addLink.png"),
      // nameinput: "Random Variables",
      nameinput: "Fundamental Graphs",
      // nameinput: "Trees",
      lectureStyleValue: [0, 80],
      tableData: [{
        key: 'Title',
        value: '',
      },{
        key: 'Type',
        value: '',
      }, {
        key: 'ContentT',
        value: '',
      }, {
        key: 'Content',
        value: '',
      }, {
        key: 'InputT',
        value: '',
      }, {
        key: 'Input',
        value: '',
      },{
        key: 'OutT',
        value: '',
      },{
        key: 'Out',
        value: '',
      }
      ],
      
      graphGTransformK: 1,
      graphGTransformX: 0,
      graphGTransformY: 10,
      curEntId: "",
      insertEntId: "",
      insertSourceEntId: "-1",
      insertTargetEntId: "-1",
      sonList: [],
      minDImportance: 0,
      maxDImportance: 0,
      minDRelevance: 0,
      maxDRelevance: 0,
      maxDDuration: 0,
      maxTotalDuration: 0,
      importanceMinColor: "rgb(203, 230, 209)",
      importanceMaxColor: "rgb(22, 144, 207)",
      totalDuration: 1000,
      importanceColor_linear: null,
      importanceCompute_color: null,
      relevanceScale_linear: null,
      totalDurationScale_linear: null,
      DivisionDataList: [],
      rootDivisionDataList: [],
      entDivisionDataList: [],
      colorMap: {},
      rootColorMap:{},
      videoDuration: 570,
      selectRectId: "",
      selectRectClass: "",
      topicLineWidth: 1000,
      topicLineHeight: 1000,
      moveLineWidth: 1000,
      entLineWidth: 1000,
      totalSonDuration: 0,
      treeGTransformK:1,
      treeGTransformX:10,
      treeGTransformY:100,
      margin: { top: 5, right: 5, bottom: 5, left: 5 },
    };
  },
  watch: {
    typeRadio(val) {
    },
    lectureStyleValue(val){
      console.log(val);
      let mid = (val[0]+val[1])/2;
      d3.select("#procData .el-slider__runway")
      .attr("style","background: linear-gradient(90deg, #ff9c9c "+mid+"%,#6f8be0 "+mid+"%) !important")
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
    selectType(v) {
      // console.log(v)
    },
    

    iRowStyle:function ({row, rowIndex}) {
        return 'height:35px';
    },
    iHeaderRowStyle:function ({row, rowIndex}) {
        return 'height:35px';
    },
    iCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:2px'
    },
    iHeaderCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px' 
    },
    drawQuestionSurface(svg){
      const _this = this;
      let psvg =svg
      let w = psvg.attr("width");
      let h = psvg.attr("height");
      psvg.select("#procG").remove();
      let backg = psvg.append("g").attr("id", "backG").attr("width", w).attr("height", h);
      let prog = psvg.append("g").attr("id", "procG").attr("width", w).attr("height", h);
      let proData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let conceptTree = _this.conceptTree;

      console.log(conceptTree,problemConceptData);
      let proId = _this.curEntId;
      if(proId == ""){return;}
      let curPro = proData.find(function(p){return (p['id']).toString() == (proId).toString()})
      let title = curPro['title'];
      let type = curPro['type'];
      let tx=10;
      let ty = 20;
      // ty = _this.drawTxt(prog,tx,ty,w,`Title:${title}`,"black",22,'title');
      let content = curPro['content'].split("###");

      let input =" ";
      let output ="";
      if(proId == '1568086661408161798'){
        title = "ASCII";
        content = ["已知字符 'a' 的ASCII码为 97，执行下列语句的输出是_______。 `printf ('%d, %c', 'b', 'b'+1 )` ;"];
        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "";
        input = "A.98, b   B.错误 C. 98, 99   D. 98, c"
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "";
        // output = "C. 98, 99   D. 98, c"
      }
      else if(proId == '1568086661408161798'){
        title = "ASCII";
        content = ["已知字符 'a' 的ASCII码为 97，执行下列语句的输出是_______。 `printf ('%d, %c', 'b', 'b'+1 )` ;"];
        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "";
        input = "A.98, b   B.错误 C. 98, 99   D. 98, c"
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "";
        // output = "C. 98, 99   D. 98, c"
      }
      else if(type == 'PROGRAMMING'){
        input =" "+ content[1].split("输入格式:")[1];
        output =""+ content[2].split("输出格式:")[1];
        title = `Title: ${' '} ${title}`;
        _this.tableData.find(function(t){return t['key'] == 'ContentT'})['value'] = "Description:";
        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "Input Format:";
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "Output Format:";
      }
      else{
        title = "";

        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "";
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "";
      }
      _this.tableData.find(function(t){return t['key'] == 'Title'})['value'] = `${' '} ${title}`;
      _this.tableData.find(function(t){return t['key'] == 'Type'})['value'] = `Type: ${type}`;
      _this.tableData.find(function(t){return t['key'] == 'Content'})['value'] = content[0];
      _this.tableData.find(function(t){return t['key'] == 'Input'})['value'] = ` ${input}`;
      _this.tableData.find(function(t){return t['key'] == 'Out'})['value'] = ` ${output}`;
      console.log(_this.tableData)
      let conMap = {}
      let conName = []
      for(let i=0;i<conceptTree.length;i++){
        conMap[conceptTree[i]['id']] = -1;
        conName.push(conceptTree[i]['id'])
      }
      // var compare = function (x, y) {//比较函数
      //   let lenx = x.length;
      //   let leny = y.length;
      //   if(lenx!=leny)return lenx>leny;
      //   return x["problemSetId"] > y["problemSetId"] 
      // };
      // conName.sort(compare)

      for (let i = 0; i < problemConceptData.length; i++) {
        let conceptId = problemConceptData[i]['conceptId'];
        let problemId = problemConceptData[i]['problem'];
        let type = problemConceptData[i]['type'];
        if(problemId == proId){
          conMap[conceptId] = type;
        }
      }
      let prex = 30;
      let prey = 60;
      let textWidth = _this.drawTxt(prog, 14, 20, "Related concepts：", "rgb(103, 103, 103)", 22, `kd`);
      conceptTree.forEach(con=>{
        let jg = conMap[con['id']];
        if(jg!=-1){
          let recColor = "rgb(218, 127, 136)";
          if(jg==0)
            recColor = "grey"
          let textWidth = _this.drawTxt(prog, prex, prey, con['name'], "white", 16, `ProSur_con${con['id']}`);
          _this.drawRect(backg, prex-4, prey-20, textWidth+8,28,  10, recColor, "1", "none", "1", `ProSur_coRect${con['id']}`, 'ProSur');
        // prey+=10;
          prex+=textWidth+20;
          if(prex>270){
            prex = 30;
            prey+=30
          }
        }
        // let textWidth = _this.drawTxt(prog, prex, prey, con['id']+''+conMap[con['id']], "black", 10, `FigNet_con`);

          // _this.drawTxt(prog,prex,prey,w,`Title:${content}`,"black",16,'title');
      })
      // _this.drawTxt(prog,tx,ty+25,w,`Title:${content}`,"black",16,'title');
    },    
    
    drawprocData() {
      const _this = this;
      const margin = _this.margin;
      let width = this.$refs.procData.offsetWidth - margin.left - margin.right;
      let height = this.$refs.procData.offsetHeight - margin.top - margin.bottom;
      d3.select("#procData").select("svg").remove();
      var svg = d3.select("#procData").append("svg")
        .attr("id", "procEnt")
        .attr("width", width)
        .attr("height", height);

        let graphGTransformX = _this.graphGTransformX;
      let graphGTransformY = _this.graphGTransformY;
      let graphGTransformK = _this.graphGTransformK;
      
      let stx = 0;
      let sty = 0;
      let stk = 1;
      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height).attr("transform", "translate(1,320)");
        var graphZoom = d3.zoom()
        .scaleExtent([0, 100])
        .on("start", (e) => {
          sty = e.transform.y;
          stx = e.transform.x;
          stk = e.transform.k;
        })
        .on('zoom', (e) => {
          graphGTransformX = _this.graphGTransformX //+ e.transform.x - stx;
          graphGTransformY = _this.graphGTransformY + e.transform.y - sty;
          graphGTransformK = _this.graphGTransformK //+ e.transform.k - stk;
          entG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.graphGTransformX = graphGTransformX;
          _this.graphGTransformY = graphGTransformY;
          _this.graphGTransformK = graphGTransformK;
          entG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        });

      svg.call(graphZoom);
      // _this.entG = entG;
      // _this.sonG = sonG;
      _this.drawQuestionSurface(entG);
      // _this.drawSonLine(_this.data[1]);
    },
    updata() {
      
    const _this = this;
      _this.drawprocData();
    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      _this.updata();

    });
  },
  mounted() {
    const _this = this
    // _this.tableData.find(function (d) { return d['key'] == 'name' })['value'] = 'Computer Network';
    this.$bus.$on('selectEnt', (val) => {
     _this.curEntId = val;
     _this.updata();
    });
    this.$bus.$on('allProblem', (val) => {
     _this.problemsData = val;
      // _this.updata();
    });
  },
  // beforeDestroy() {
  //   clearInterval(this.moveTimer);
  // },
} 
</script>

<style>
@import './index.css';
</style>
