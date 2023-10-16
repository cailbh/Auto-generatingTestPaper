<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="procPanel">
    <div class="panelHead">Content View </div>
      <!-- //SupportPanel</div> -->
    <div id="procPanelDiv" class="panelBody" ref="procPanelDiv">
      <el-button>这是一个按钮</el-button>
    </div>
    </div>
</template>
  
<script>
import * as d3 from 'd3'
// import tools from "@/utils/tools.js";

export default {
  props: [],
  data() {
    return {
      typeRadio: "cell State",
      
    };
  },
  watch: {
    typeRadio(val) {
    },
    lectureStyleValue(val){
      console.log(val);
      let mid = (val[0]+val[1])/2;
      // d3.select("#procData .el-slider__runway")
      // .attr("style","background: linear-gradient(90deg, #ff9c9c "+mid+"%,#6f8be0 "+mid+"%) !important")
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
    drawprocData() {
      const _this = this;
      const margin = _this.margin;
      // let width = this.$refs.procData.offsetWidth;
      // let height = this.$refs.procData.offsetHeight;
      // d3.select("#procData").select("svg").remove();
      // var svg = d3.select("#procData").append("svg")
      //   .attr("id", "procEnt")
      //   .attr("width", width)
      //   .attr("height", height);

       
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
    // this.$bus.$on('selectEnt', (val) => {
    //  _this.curEntId = val;
    //  _this.updata();
    // });
  },
  // beforeDestroy() {
  //   clearInterval(this.moveTimer);
  // },
} 
</script>

<style>
@import './index.css';
</style>
