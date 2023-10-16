<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="proListPanel">
    <div class="panelHead">Content View </div>
    <!-- //SupportPanel</div> -->
    <div id="proListPanelDiv" class="panelBody" ref="proListPanelDiv">

      <el-table :data="tableData" height="500" style="width: 100%;">
        <el-table-column prop="type" label="题型" width="100">
        </el-table-column>
        <el-table-column prop="title" label="题目" width="300">
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
            <el-button @click="click_View(scope)" type="text" size="medium">查看</el-button>
            <el-button type="text" size="small">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    <div class="pagination">
      <el-pagination @current-change="handleCurrentChange" :page-size="pageSize" :pager-count="11" layout="prev, pager, next" :total="problemsNum">
      </el-pagination>
    </div>
      <!-- <div id="connectCon" ref="connectCon">
      </div> -->
      <div id="proListData" ref="proListData">

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
      problemsNum: 0,
      page:1,
      pageSize:20,
      tableData: [
      //   {
      //   type: '选择题',
      //   name: '王小虎',
      // }, {
      //   type: '选择题',
      //   name: '王小虎',
      // }
      ],
      margin: { top: 5, right: 5, bottom: 5, left: 5 },
    };
  },
  watch: {
    type(val) {
    },
    curEntId(curEntId) {
    }
  },
  methods: {
    getProblemsNum() {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/problem/problemNum", {}, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          _this.problemsNum = response.body[0];
        });
    },
    getProblemsByPages(page,pageSize) {
      const _this = this;
      let data = [];
      this.$http
        .get("/api/problem/problemsByPage", { params: { page: page, pageSize:pageSize } }, {})
        // .get("/api/test", {}, {})
        .then((response) => {
          console.log("11",response.body);
          _this.tableData = response.body;
        });
    },
     // 显示第几页
    handleCurrentChange(val) {
      const _this = this;
      // 改变默认的页数
      this.page = val
      // 切换页码时，要获取每页显示的条数
      _this.getProblemsByPages(_this.page,_this.pageSize);
    },
    click_View(data) {
      const _this = this;
      console.log(data)
      // this.$emit("timeDur", time);
    },
    click_Edit(data) {
      // this.$emit("timeDur", time);
    },
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      // _this.updata();

    });
  },
  mounted() {
    const _this = this

    _this.getProblemsNum();
    _this.getProblemsByPages(1,10);
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
