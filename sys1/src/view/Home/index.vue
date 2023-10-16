<template>
   <div id="Root">
            <!-- <div id="importProPanel" class="panel">

            </div> -->
            <div id="graphPanel" class="panel">
                <ProcPanel></ProcPanel>
            </div>
            <div id="graphPanel" class="panel">
                <ProcPanel></ProcPanel>
            </div>
            <div id="graphPanel" class="panel">
                <ProcPanel></ProcPanel>
            </div>
   </div>
</template>

<script>

import ProcPanel from '@/components/ProblemContentPanel/index.vue';
// import Head from "@/components/Header/index.vue"
export default {
  // components: { scene,Head,homeLeft,homeRight,homeBottom,navBar,uiBtns},
  components: { ProcPanel},
  /* eslint-disable no-unused-vars */
  data() {
    return {
      windowWidth: document.documentElement.clientWidth, //实时屏幕宽度
      windowHeight: document.documentElement.clientHeight, //实时屏幕高度
      marge: {
        top: 6,
        right: 10,
        bottom: 16,
        left: 6,
      },
    };
  },
  watch: {
    
    cube_data() {
      this.$nextTick(() => { });
    },
    cluData() {
      this.$nextTick(() => {
      });
    },
  },
  methods: {
    async testPy() {
      const _this = this;
      let data = [];
      const {data:res} = await this.$http.get('/api/test',{})
      console.log(res);
      this.$http
        // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
        .get("/api/test", {}, {})
        .then((response) => {
          console.log('test')
          console.log(response)
        });
    },
    clickHandler() {
      console.log(111111);
    },
  },
  created: function () {
    var _this = this;
  },
  mounted() {
    this.$el.style.setProperty("--heightStyle", this.windowHeight + "px");
    this.showVideo = true;
    this.testPy();
    // this.getData();
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  }
};
</script>

<style>
  @import './index.css';
</style>