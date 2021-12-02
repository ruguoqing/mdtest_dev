
//项目和模块联动下拉列表
var CaseInit = function() {


    function getCaseList() {
        //调用获取用例接口
        $.get("/interface/get_case_info", {}, function (resp) {
            if (resp.success === "true") {
                dataList = resp.data;
                //遍历用例
                for (var i = 0; i < dataList.length; i++) {
                    // $("#case_list").append("<input type='checkbox' name='caseinfo' value=" + dataList[i].case_id +">" + dataList[i].case + "<br>");
                    $("#case_list").append("<input type='checkbox' name='caseinfo' value=" + dataList[i].case_id + " id=" + dataList[i].case_id + ">" + dataList[i].case + "<br>");


                }
            }
        });
    }

    //调用getCaseList函数
    getCaseList();
}


var CaseSelected = function() {


    function selectedCaseList(){

        let path= window.location.pathname;
        let tid = path.split('/')[3]
        console.log('路径', path, tid)
        //调用获取任务用例接口
        $.post("/interface/get_selected_cases", {
            'tid': tid,
        }, function(resp){
            if(resp.success === "true"){
                cids = resp.data;
            }
        });

        //调用获取用例接口
        $.get("/interface/get_case_info", {}, function(resp){
            if(resp.success === "true"){
                dataList = resp.data;
                 //遍历用例
                for (var i = 0;i < dataList.length; i++){
                    if(cids.includes(dataList[i].case_id)){
                        $("#case_list").append("<input type='checkbox' name='caseinfo' value=" + dataList[i].case_id + " id=" + dataList[i].case_id + " checked/>" + dataList[i].case + "<br>");

                    }else {
                        $("#case_list").append("<input type='checkbox' name='caseinfo' value=" + dataList[i].case_id + " id=" + dataList[i].case_id + ">" + dataList[i].case + "<br>");
                    }


                }
            }
        });
    }
    //调用getCaseList函数
    selectedCaseList();

}
