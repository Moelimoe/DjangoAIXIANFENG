$(document).ready(function(){
    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping");
    var subShoppings = document.getElementsByClassName("subShopping");

    //添加商品
    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i];
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga");
            $.post("/changetrolley/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data;
                    //购物车需要一个总价
                    document.getElementById(pid+"price").innerHTML = data.totalPrice;
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
                    document.getElementById(pid).innerHTML = data.data;
                    //购物车需要一个总价
                    document.getElementById(pid+"price").innerHTML = data.totalPrice;
                    if(data.data == 0) {
                        //window.location.href = "http://127.0.0.1:8000/trolley/"
                        var li = document.getElementById(pid+"li");
                        li.parentNode.removeChild(li)
                    }
                }
            })
        })
    }



    //勾选购物篮物品
    var ischoses = document.getElementsByClassName("ischose");
    for (var j = 0; j < ischoses.length; j++){
        ischose = ischoses[j];
        ischose.addEventListener("click", function(){
            pid = this.getAttribute("goodsid");
            $.post("/changetrolley/2/", {"productid":pid}, function(data){
                if (data.status == "success"){
                    //window.location.href = "http://127.0.0.1:8000/trolley/"
                    var s = document.getElementById(pid+"a");
                    s.innerHTML = data.data
                }
            })
        },false);
    }

    // //全选购物篮物品
    // var chooseall = document.getElementById("_chooseall");
    // chooseall.addEventListener("click", function(){
    //     $.post("/changetrolley/3/", function(data){
    //         if (data.status == "success"){
    //             console.log("全选啊");
    //             chooseall.innerHTML = "√";
    //             // for (var k=0; k < data.data.length; k++){
    //             //     if(data.data[k].isChose!=="True"){
    //             //         var s = document.getElementById(pid+"a");
    //             //         s.innerHTML = "√";
    //             //     }
    //             //     chooseall.innerHTML = "√";
    //             // }
    //         }
    //     })
    // },false)



    var ok = document.getElementById("ok");
    ok.addEventListener("click", function(){
        var f = confirm("是否确认下单？");
        if (f){
            $.post("/submitorder/", function(data){
                if (data.status == "success"){
                    window.location.href = "/trolley/";
                    // var tp = document.getElementById("total_price");
                    // console.log("~~~~~~~~");
                    // tp.innerHTML = data.data
                }
            })
        }
    },false)
});
