<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="paperListPanel">
    <div class="panelHead">试卷列表 </div>
    <!-- //SupportPanel</div> -->
    <div id="paperListPanelDiv" class="panelBody" ref="paperListPanelDiv">

      <el-table :data="tableData" height = 420 style="width: 100%;">
        <el-table-column prop="id" label="id" width="100">
        </el-table-column>
        <el-table-column prop="number" label="题目数量" width="300">
        </el-table-column>
        <!-- <el-table-column prop="province" label="省份" width="120">
        </el-table-column>
        <el-table-column prop="city" label="市区" width="120">
        </el-table-column>
        <el-table-column prop="address" label="地址" width="300">
        </el-table-column>
        <el-table-column prop="zip" label="邮编" width="120">
        </el-table-column> -->
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button @click="click_View(scope.row)" type="text" size="medium">查看</el-button>
            <!-- <el-button @click="click_ProAdd(scope.row)" type="text" size="small">添加</el-button> -->
          </template>
        </el-table-column>
      </el-table>
    <div class="pagination">
      <el-pagination @current-change="handleCurrentChange" :page-size="pageSize" :pager-count="11" layout="prev, pager, next" :total="papersNum">
      </el-pagination>
    </div>
      <!-- <div id="connectCon" ref="connectCon">
      </div> -->
      <div id="paperListData" ref="paperListData">

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
      paperIdList:[],
      papperChange:false,
      papersNum: 0,
      curPaperSankeyData:'',
      page:1,
      pageSize:20,
      tableData: [ ],
      margin: { top: 5, right: 5, bottom: 5, left: 5 },
    };
  },
  watch: {
    type(val) {
    },
    curEntId(curEntId) {
    },
    paperIdList(val){
      const _this = this;
      _this.$bus.$emit("paperIdList", val);
    }
  },
  methods: {
    click_ProAdd(val){
      console.log(val);
      const _this = this;
      if(_this.paperIdList.indexOf(val.id)==-1){
        _this.paperIdList.push(val.id);
      }

    },
    
    getPaperSankeyById(paperId) {
      const _this = this;
      this.$http
        .get("/api/paper/sankeyById", { params: { paperId: paperId } }, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          _this.curPaperSankeyData = response.body;
          _this.$bus.$emit("curPaperSankeyData", _this.curPaperSankeyData);
        });
    },

    getPapersNum() {
      const _this = this;
      let data = [];

      this.$http
        .get("/api/paper/paperNum", {}, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          _this.papersNum = response.body[0];
          _this.$bus.$emit("papersNum", _this.papersNum);
        });
    },
    getPapersByPages(page,pageSize) {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/paper/papersByPage", { params: { page: page, pageSize:pageSize } }, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          _this.tableData = response.body;
          console.log('paper',_this.tableData);
        });
    },
     // 显示第几页
    handleCurrentChange(val) {
      const _this = this;
      // 改变默认的页数
      this.page = val
      // 切换页码时，要获取每页显示的条数
      _this.getPapersByPages(_this.page,_this.pageSize);
    },
    click_View(data) {
      const _this = this;
      _this.getPaperSankeyById([data['id']])
      this.$bus.$emit("paperSelected", data);
    },
    click_Edit(data) {
      // this.$emit("timeDur", time);
    },
    updata(){
      const _this =this;
      _this.getPapersNum();
      _this.getPapersByPages(1,_this.pageSize);
    }
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      // _this.updata();
      // _this.paperIdList = ["1701115978840051712", "1697260400746143744"];
    });
  },
  mounted() {
    const _this = this

    _this.getPapersNum();
    _this.getPapersByPages(1,_this.pageSize);
    this.$bus.$on('allpaper', (val) => {
      _this.papersData = val;
      // _this.updata();
    });
    this.$bus.$on('proIdDelList', (val) => {
      _this.paperIdList = val;
    });
    this.$bus.$on('papperChange', (val) => {
      _this.papperChange = val;
      _this.updata();
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
