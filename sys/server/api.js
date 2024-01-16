/* eslint-disable no-unused-vars */
"use strict";
const models = require('./db');
const express = require('express');
const router = express.Router();
const child_process = require('child_process');

router.post('/api/test',function(req,res,next){
    //创建子进程
    //这里是shell语句，可以通过&&将多条命令执行，这里cmd 用activate就可以激活，只有conda的shell才需要加conda
    var workerProcess = child_process.exec('python ../public/py/test.py ', function (error, stdout, stderr) {
      if (error) {
          console.log(error.stack);
          console.log('Error code: '+error.code);
          console.log('Signal received: '+error.signal);
      }else{
        console.log('stdout: ' + stdout);
        console.log('stderr: ' + stderr);
        res.send(stdout);
        // res.send(eval(stdout))   //这里要eval一下，然后在客户端才能eval将字符串转化为json数组
      }
      
        
    });
  
    workerProcess.on('exit', function (code) {
        console.log('子进程已退出，退出码 '+code);
    });
  });
router.post('/api/paper/addPaper',function(req,res,next){
    console.log('addPaper');
    console.log(req.body.params)
    
    let newPaper = new models.Paper({
        id:req.body.params.id,
        type0:req.body.params.type0,
        type1:req.body.params.type1,
        type2:req.body.params.type2,
        type3:req.body.params.type3,
        number:req.body.params.number
    });
    // 保存数据newAccount数据进mongoDB
    newPaper.save((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send('createAccount successed');
        }
    });


  });

router.post('/api/FormPaper',function(req,res,next){
    console.log('FormPaper');
    console.log(req.body.params)
    let paperIndex = req.body.params.paperIndex;
    let paperId = req.body.params.paperId;
    let indexStr = paperIndex['type1']+' '+paperIndex['type2']+' '+paperIndex['type3']+' '+paperIndex['type4']+' '+paperIndex['ids']+' '+paperId+' ';
    //创建子进程
    //这里是shell语句，可以通过&&将多条命令执行，这里cmd 用activate就可以激活，只有conda的shell才需要加conda
    var workerProcess = child_process.exec('python ../public/py/FormPaper.py '+indexStr, function (error, stdout, stderr) {
      if (error) {
          console.log(error.stack);
          console.log('Error code: '+error.code);
          console.log('Signal received: '+error.signal);
      }else{
        // console.log('stdout: ' + stdout);
        // console.log('stderr: ' + stderr);
        // res.send(stdout);
        res.send(eval(stdout))   //这里要eval一下，然后在客户端才能eval将字符串转化为json数组
      }
      
        
    });
  
    workerProcess.on('exit', function (code) {
        console.log('子进程已退出，退出码 '+code);
    });
  });
router.post('/api/pro/createData', (req, res) => {
    // 这里的req.body能够使用就在index.js中引入了const bodyParser = require('body-parser')
    let newProblem = new models.Login({
        account: req.body.account,
        password: req.body.password
    });
    // 保存数据newAccount数据进mongoDB
    newAccount.save((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send('createAccount successed');
        }
    });
});
//创建联系
router.post('/api/conceptProblem/createRel', (req, res) => {
    // 这里的req.body能够使用就在index.js中引入了const bodyParser = require('body-parser')
    let newRel = new models.createdRel({
        problem: req.body.params.problem,
        conceptId:req.body.params.conceptId,
        type:req.body.params.type
    });
    // 保存数据数据进mongoDB
    newRel.save((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send('createRelsuccessed');
        }
    });
});
//删除联系
router.post('/api/conceptProblem/delRel', (req, res) => {
    // 保存数据数据进mongoDB
    models.createdRel.deleteMany({
        problem: req.body.params.problem,
        conceptId:req.body.params.conceptId,
    },(err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send('createRelsuccessed');
        }
    });
});
// 获取问题接口
router.get('/api/problem/allProblem', (req, res) => {
    // 通过模型去查找数据库
    models.Problem.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    })
});
// 获取关系接口
router.get('/api/problem/allRelationship', (req, res) => {
    // 通过模型去查找数据库
    models.ProblemConcept.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    })
});
// 获取GPT关系接口
router.get('/api/problem/allGPTRelationship', (req, res) => {
    // 通过模型去查找数据库
    models.ProConGPTRel.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    })
});
// 获取问题概念GPT散点数据接口
router.get('/api/problem/allProInConGPTScatterData', (req, res) => {
    // 通过模型去查找数据库
    models.ProInConGPTScatter.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    })
});
// 获取概念散点数据接口
router.get('/api/concept/allproConScatterData', (req, res) => {
    // 通过模型去查找数据库
    models.ProConScatter.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    })
});
// 获取问题总数
router.get('/api/problem/problemNum', (req, res) => {
    // 通过模型去查找数据库
    models.Problem.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send([data.length])
        }
    })
    //.count();
    
    // res.send(cnt);
});
// 获取sankeyData总数
router.get('/api/sankeyData', (req, res) => {
    // 通过模型去查找数据库
    models.SankeyData.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data)
        }
    })
    //.count();
    
    // res.send(cnt);
});
// 通过页码获取问题
router.get('/api/problem/problemsByPage', (req, res) => {
    var pageNum = req.query['page']
    var pageSize = req.query['pageSize']
    const aggregate = [
        {
            "$project":
            {
                "_id": 0,
                "title": 1,
                "type": 1,
                "id": 1,
                // "cnt": {"$size": '$seq'}
            }
        },
        //  {"$sort": {"cnt": -1}},
        // {"$match": {"cnt": {"$gt": 300, "$lte": 1000}}},
        { "$skip": (parseInt(pageNum) - 1) * parseInt(pageSize) },
        { "$limit": parseInt(pageSize) }
    ]
    // 通过模型去查找数据库
    models.Problem.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
            console.log(err)
        } else {
            res.send([data]);
        }
    });
});
// 通过Id获取问题
router.get('/api/problem/problemById', (req, res) => {
    var proIds = req.query['proIds'];
    const aggregate = [
        {
            "$project":
            {
                "_id": 0,
                "title": 1,
                "type": 1,
                "id": 1,
                "content": 1
                // "cnt": {"$size": '$seq'}
            }
        },
        {
            "$match": {
                "id":{$in:proIds}
            }
        },
        // {"id":{$all:proIds}}
    ]
    // 通过模型去查找数据库
    models.Problem.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
            console.log(err)
        } else {
            res.send([data]);
        }
    });
});

// 通过Id获取试卷SankeyData
router.get('/api/paper/sankeyById', (req, res) => {
    var paperId = req.query['paperId'];
    const aggregate = [
        {
            "$project":
            {
                "_id": 0,
                "id": 1,
                "link": 1
                // "cnt": {"$size": '$seq'}
            }
        },
        {
            "$match": {
                "id":{$in:paperId}
            }
        },
        // {"id":{$all:proIds}}
    ]
    // 通过模型去查找数据库
    models.PaperSankey.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
            console.log(err)
        } else {
            res.send([data]);
        }
    });
});
// 获取问题接口
// router.get('/api/problem/allProblem', (req, res) => {
//     // 通过模型去查找数据库
//     models.Problem.find((err, data) => {
//         if (err) {
//             res.send(err);
//         } else {
//             res.send(data);
//         }
//     }).select({ 
//         "_id":0,
//         "score": 1,
//          "id": 1,
//         "title":1,
//         "content":1,
//         "type":1,
//         "problemSetId":1,
//     });
//     ;
// });


// 获取user做题记录接口
router.get('/api/Submission/allLog', (req, res) => {
    // 通过模型去查找数据库
    models.Submission.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    }).select({ 
        "_id":0,
        "score": 1,
        "user":1,
        "submitAt":1,
         "id": 1,
        "judgeResponseContents":1,
        "content":1,
        "type":1,
        "problemSetId":1,
    });
});
// 获取概念接口
router.get('/api/concept/allConcept', (req, res) => {
    // 通过模型去查找数据库
    models.Concept.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取试卷接口
router.get('/api/paper/allPaper', (req, res) => {
    // 通过模型去查找数据库
    models.Paper.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});

// 获取试卷总数
router.get('/api/paper/paperNum', (req, res) => {
    // 通过模型去查找数据库
    models.Paper.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send([data.length])
        }
    })
    //.count();
    
    // res.send(cnt);
});

// 通过页码获取试卷
router.get('/api/paper/papersByPage', (req, res) => {
    var pageNum = req.query['page']
    var pageSize = req.query['pageSize']
    const aggregate = [
        // {
        //     "$project":
        //     {
        //         "_id": 0,
        //         "title": 1,
        //         "type": 1,
        //         "id": 1,
        //         // "cnt": {"$size": '$seq'}
        //     }
        // },
        //  {"$sort": {"cnt": -1}},
        // {"$match": {"cnt": {"$gt": 300, "$lte": 1000}}},
        { "$skip": (parseInt(pageNum) - 1) * parseInt(pageSize) },
        { "$limit": parseInt(pageSize) }
    ]
    // 通过模型去查找数据库
    models.Paper.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
            console.log(err)
        } else {
            res.send([data]);
        }
    });
});
// 获取概念接口
router.get('/api/concept/ConceptOri', (req, res) => {
    // 通过模型去查找数据库
    models.ConceptOri.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取概念树接口
router.get('/api/concept/conceptTree', (req, res) => {
    // 通过模型去查找数据库
    models.ConceptTree.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取学生接口
router.get('/api/student/allStudent', (req, res) => {
    // 通过模型去查找数据库
    const aggregate = [
        {
            "$project":
            {
                "_id": 0
            }
        }
    ]
    models.Student.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});

// 获取问题关联概念接口
router.get('/api/conceptProblem/allRel', (req, res) => {
    // 通过模型去查找数据库
    models.ProblemConcept.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});


module.exports = router;