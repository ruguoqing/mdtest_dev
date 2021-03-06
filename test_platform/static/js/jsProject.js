
//项目和模块联动下拉列表
var ProjectInit = function(_cmbProject, _cmbModule, defaultProject, defaultModule)
{
    var cmbProject = document.getElementById(_cmbProject);
    var cmbModule = document.getElementById(_cmbModule);
    var dataList = [];
    // window.alert(defaultProject);
    // window.alert(defaultModule);
    //设置默认选项
    function cmbSelect(cmb, str){
        for(var i=0; i< cmb.options.length; i++){
            if(cmb.options[i].value == str){
                cmb.selectedIndex = i;
                return;
            }
        }
    }
    //创建下拉选项
    function cmbAddOption(cmb, str, obj){
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = str;
        option.value = str;
        option.obj = obj;
    }

    //改变项目
    function changeProject(){
        cmbModule.options.length = 0;
        if (cmbProject.selectedIndex === -1){
            return;
        }
        var item = cmbProject.options[cmbProject.selectedIndex].obj;
        for (var i = 0; i<item.moduleList.length; i++){
            cmbAddOption(cmbModule, item.moduleList[i],null);
        }
        cmbSelect(cmbModule, defaultModule)
    };


    function getProjectList(){
        //调用项目列表接口
        $.get("/interface/get_project_list", {}, function(resp){
            if(resp.success === "true"){
                dataList = resp.data;
                //遍历项目
                for (var i = 0;i < dataList.length; i++){
                    cmbAddOption(cmbProject, dataList[i].name, dataList[i]);
                }
                cmbSelect(cmbProject, defaultProject);
                changeProject();
                cmbProject.onchange = changeProject;
            }
        });
    }
    //调用getProjectList函数
    getProjectList();
}
