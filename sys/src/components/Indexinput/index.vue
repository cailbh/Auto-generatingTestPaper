<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="indexInput" ref="indexInputDiv">
    <div class="panelHead">p</div>
    <div id="indexInput" class="panelBody">
      <el-tree :data="contentTreeData" show-checkbox node-key="id" default-expand-all :expand-on-click-node="false"
        :render-content="renderContent">
      </el-tree>
      <el-divider></el-divider>
      <el-form label-position='right' label-width="80px">
        <el-col :span="11">
        <el-form-item label="选择题">
          <el-input-number v-model="paperIndex.type1" :min="0" ></el-input-number>
          <!-- <el-input v-model="paperIndex.type1"></el-input> -->
        </el-form-item>
        <el-form-item label="判断题">
          
          <el-input-number v-model="paperIndex.type2" :min="0" ></el-input-number>
          <!-- <el-input v-model="paperIndex.type2"></el-input> -->
        </el-form-item>
        </el-col>
        <el-col :span="11">
        <el-form-item label="填空题">
          
          <el-input-number v-model="paperIndex.type3" :min="0" ></el-input-number>
          <!-- <el-input v-model="paperIndex.type3"></el-input> -->
        </el-form-item>
        <el-form-item label="编程题">
          <el-input-number v-model="paperIndex.type4" :min="0" ></el-input-number>
          <!-- <el-input v-model="paperIndex.type4"></el-input> -->
        </el-form-item>
        </el-col>
      </el-form>
      <el-button type="primary" @click="onSubmit">Create</el-button>
    </div>
  </div>
  <!-- <div id="moveLeft" ref="moveindexInputLeft"></div>
                    <div id="moveRight" ref="moveindexInputRight"></div> -->
  <!-- <div id="assistindexInputPanel" class="panel">
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
</div></template>
  
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
        name: "",
        type: "",
        content: ""
      },
      paperIndex:{
        type1:0,
        type2:0,
        type3:0,
        type4:0,
      },
      thisId: 10,
      contentTreeData: [{
        id: 1,
        label: '基本数据类型与表达式',
        indexValue: 0,
        children: [{
          id: 2,
          label: '表达式',
          indexValue: 0,
          children: []
        }, {
          id: 3,

          indexValue: 0,
          label: '输入输出格式化控制',
          children: []
        }
        ]
      }, {
        id: 4,

        indexValue: 0,
        label: '分支控制',
        children: [{
          id: 5,
          indexValue: 0,
          label: 'if-else'
        }, {
          id: 6,
          indexValue: 0,
          label: 'switch'
        }]
      }, {
        id: 7,
        indexValue: 0,
        label: '循环控制',
        children: [{
          id: 8,
          indexValue: 0,
          label: 'for'
        }, {
          id: 9,
          indexValue: 0,
          label: 'while和do-while'
        }, {
          id: 10,
          indexValue: 0,
          label: '嵌套循环'
        }]
      }, {
        id: 11,
        indexValue: 0,
        label: '函数与程序结构',
        children: [{
          id: 12,
          indexValue: 0,
          label: '函数定义与调用'
        }, {
          id: 13,
          indexValue: 0,
          label: '递归函数'
        }, {
          id: 14,
          indexValue: 0,
          label: '变量作用域与存储类型'
        }]
      }, {
        id: 15,
        indexValue: 0,
        label: '数组',
        children: [{
          id: 16,
          indexValue: 0,
          label: '一维数组'
        }, {
          id: 17,
          indexValue: 0,
          label: '字符串'
        }, {
          id: 18,
          indexValue: 0,
          label: '二维数组'
        }]
      }, {
        id: 19,
        indexValue: 0,
        label: '指针与结构',
        children: [{
          id: 20,
          indexValue: 0,
          label: '指针'
        }, {
          id: 21,
          indexValue: 0,
          label: '结构'
        }, {
          id: 22,
          indexValue: 0,
          label: '链表'
        }]
      }, {
        id: 23,
        indexValue: 0,
        label: '文件',
        children: [{
          id: 24,
          indexValue: 0,
          label: '文本文件处理'
        }, {
          id: 25,
          indexValue: 0,
          label: '二进制文件处理'
        }]
      }]
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


    append(data) {
      const newChild = { id: this.thisId++, label: 'testtest', children: [], indexValue: 0, };
      if (!data.children) {
        this.$set(data, 'children', []);
      }
      data.children.push(newChild);
    },
    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex(d => d.id === data.id);
      children.splice(index, 1);
    },

    renderContent(h, { node, data, store }) {
      return (
        // <template>
        <div class="custom-tree-node">
          <span>{node.label}</span>

          <span>
            <div class="treeSlider">
              {/* <el-slider value={node.indexValue} on-change={(d)=>this.changTreeSlider(d,data)}></el-slider> */}
            </div>
            {/* <el-progress type="dashboard" percentage="0" width="40"></el-progress> */}
            <el-button size="mini" type="text" on-click={() => this.append(data)}>+</el-button>
            <el-button size="mini" type="text" on-click={() => this.remove(node, data)}>-</el-button>
          </span>
        </div>
        // </template>
      );
    },

    onSubmit() {
      const _this = this;
      _this.getProblemsIds();
    },
    changTreeSlider(value,data) {
      data.indexValue = value;
      console.log(value,data)
    },
    getProblemsIds() {
      const _this = this;
      let data = [];
      console.log(_this.paperIndex)
      this.$http
        // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
        .post("/api/FormPaper", { params: _this.paperIndex }, {})
        .then((response) => {
          console.log(response, response.body);
          _this.$bus.$emit("proIdList", response.body);
        });
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
    // this.$refs.moveindexInputLeft.addEventListener("mouseover", _this.moveindexInputLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
