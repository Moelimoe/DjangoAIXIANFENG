$(document).ready(function(){
    var alltypebtn = document.getElementById("alltypebtn");
    var showsortbtn = document.getElementById("showsortbtn");

    var typediv = document.getElementById("typediv");
    var sortdiv = document.getElementById("sortdiv");

    typediv.style.display = "none";
    sortdiv.style.display = "none";


    alltypebtn.addEventListener("click", function(){
        typediv.style.display = "block";
        sortdiv.style.display = "none"
    },false);
    showsortbtn.addEventListener("click", function(){
        typediv.style.display = "none";
        sortdiv.style.display = "block"
    },false);
    // 点击其他区域，分类窗口隐藏
    typediv.addEventListener("click", function(){
        typediv.style.display = "none"
    },false);
    sortdiv.addEventListener("click", function(){
        sortdiv.style.display = "none"
    },false);




    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping");
    var subShoppings = document.getElementsByClassName("subShopping");
    var domain = document.domain;

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i];
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga");
            $.post("/changetrolley/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                } else {
                    //-1表示未登录
                    if (data.data == -1){
                        // window.location.href = "http://127.0.0.1:8000/login/"
                        // 使用login可以直接定位到当前网域下
                        window.location.href = "/login/";
                    }
                }
            })
        })
    }


    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i];
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga");
            $.post("/changetrolley/1/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                } else {
                    if (data.data == -1){
                        window.location.href = "/login/"
                    }
                }
            })
        })
    }

});