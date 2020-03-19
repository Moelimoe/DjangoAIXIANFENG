window.onload=function(){
    $(document).ready(function(){
        var account = document.getElementById("account")
        var accounterr = document.getElementById("accounterr")
        var checkerr = document.getElementById("checkerr")

        var pass = document.getElementById("pass")
        var passerr = document.getElementById("passerr")

        var password = document.getElementById("password")
        var passworderr = document.getElementById('passworderr')

        //鼠标的聚焦与离焦
        //一、判断长度是否合适
        account.addEventListener("focus", function(){
            console.log("~~~~~~~~~~~~~~~~~~~~~~");
            accounterr.style.display = "none";
            checkerr.style.display = "none";
        },false);
        account.addEventListener("blur", function(){
            instr = this.value;
            if (instr.length < 6 || instr.length > 12){
                accounterr.style.display = "block";
                return
            }
            //验证账户是否已注册
            $.post("/checkuserid/", {"userid":instr}, function(data){
                if (data.status == "error"){
                    checkerr.style.display = "block"
                }
            })
        },false);



        pass.addEventListener("focus", function(){
            passerr.style.display = "none"
        },false);
        pass.addEventListener("blur", function(){
            instr = this.value;
            if (instr.length < 6 || instr.length > 16){
                passerr.style.display = "block";
                return
            }
        },false);


        password.addEventListener("focus", function(){
            passworderr.style.display = "none"
        },false);
        password.addEventListener("blur", function(){
            instr = this.value;
            if (instr != pass.value){
                passworderr.style.display = "block"
            }
        },false);

});
};