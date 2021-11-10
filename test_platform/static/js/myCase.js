
//项目和模块联动下拉列表
var CaseInit = function()
{

    function getCaseList(){
        //调用获取用例接口
        $.get("/interface/get_case_info", {}, function(resp){
            if(resp.success === "true"){
                dataList = resp.data;
                //遍历用例
                for (var i = 0;i < dataList.length; i++){
                    $("#case_list").append("<input type=\"checkbox\" name=\"vehicle\" value=" + dataList[i].case_id +"/>" + dataList[i].case + "<br>");

                }
                console.log(dataList);
            }
        });
    }
    //调用getCaseList函数
    getCaseList();
}
