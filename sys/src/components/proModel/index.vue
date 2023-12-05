<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="proModel" ref="proModelDiv">
    <div class="panelHead"></div>
    <div id="proModel" class="panelBody">
     
      <el-button type="primary" @click="onSubmit">Create</el-button>
    </div>
  </div>
  <!-- <div id="moveLeft" ref="moveproModelLeft"></div>
                    <div id="moveRight" ref="moveproModelRight"></div> -->
  <!-- <div id="assistproModelPanel" class="panel">
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
      thisId: 10,
      contentTreeData: [{
        id: 1,
        label: '基本数据类型与表达式',
        children: [{
          id: 2,
          label: '表达式',
          children: []
        },{
          id: 3,
          label: '输入输出格式化控制',
          children: []
        }
      ]
      }, {
        id: 4,
        label: '分支控制',
        children: [{
          id: 5,
          label: 'if-else'
        }, {
          id: 6,
          label: 'switch'
        }]
      }, {
        id: 7,
        label: '循环控制',
        children: [{
          id: 8,
          label: 'for'
        }, {
          id: 9,
          label: 'while和do-while'
        }, {
          id: 10,
          label: '嵌套循环'
        }]
      }, {
        id: 11,
        label: '函数与程序结构',
        children: [{
          id: 12,
          label: '函数定义与调用'
        }, {
          id: 13,
          label: '递归函数'
        }, {
          id: 14,
          label: '变量作用域与存储类型'
        }]
      }, {
        id: 15,
        label: '数组',
        children: [{
          id: 16,
          label: '一维数组'
        }, {
          id: 17,
          label: '字符串'
        }, {
          id: 18,
          label: '二维数组'
        }]
      }, {
        id: 19,
        label: '指针与结构',
        children: [{
          id: 20,
          label: '指针'
        }, {
          id: 21,
          label: '结构'
        }, {
          id: 22,
          label: '链表'
        }]
      }, {
        id: 23,
        label: '文件',
        children: [{
          id: 24,
          label: '文本文件处理'
        }, {
          id: 25,
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
      const newChild = { id: this.thisId++, label: 'testtest', children: [] };
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
        <span class="custom-tree-node">
          <span>{node.label}</span>
          <span>
            {/* <el-button size="mini" type="text" on-click={() => this.append(data)}>Append</el-button>
            <el-button size="mini" type="text" on-click={() => this.remove(node, data)}>Delete</el-button> */}
          </span>
        </span>);
    },

    onSubmit() {
      const _this = this;
      _this.getProblemsIds();
    },

    getProblemsIds() {
      const _this = this;
      let data = [];
      this.$http
        // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
        .post("/api/FormPaper", { params: { pro: "111" } }, {})
        .then((response) => {
          console.log(response.body);
          // _this.$bus.$emit("proIdList", response.body);
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
    // this.$refs.moveproModelLeft.addEventListener("mouseover", _this.moveproModelLeft); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
