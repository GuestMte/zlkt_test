

function bindEmailCaptchaBtnClick(){
    $("#captcha-btn").click(function (event) {
    var $this= $(this)//代表当前按钮的jquery对象
//阻止默认的事件
    event.preventDefault();
    var email=$("input[name='email']").val();//获取值
    $.ajax({

        url:"/auth/captcha/email?email="+email,
        method:"GET",
        success:function (result) {
            var code=result['code'];
            if(code==200) {
                //设计倒计时
                var countdown=5;
                //倒计时结束之前，取消点击事件
                $this.off("click")
                var timer=setInterval(function () {
                $this.text(countdown);
                countdown-=1;
                if (countdown<=0){
                    clearInterval(timer);//请掉定时器
                    $this.text("获取验证码");//将按钮文字修改过来
                    bindEmailCaptchaBtnClick();//重新绑定点击事件
                }
                },1000);//每隔多少秒执行一个函数
                alert("邮箱验证码发送成功");
            }else {
                alert(result['message']);
            }

        },
        fail:function (error) {
            console.log(error);
        }
    })
})
}



$(function () {
    bindEmailCaptchaBtnClick();
})










// function bindCaptchaBtnClick() {
//     //$说明在所有代码执行后执行 #代表id
//     $("#captcha-btn").on("click", function (event) {
//         var $this = $(this);
//         var email = $("input[name='email']").val();
//         if (!email) {
//             alert("please input email first ");
//             return;
//         }
//         $.ajax({
//             url: "/user/captcha",
//             method: "POST",
//             data: {
//                 "email": email
//             },
//             success: function (res) {
//                 var code = res['code'];
//                 if (code == 200) {
//                     $this.off("click");
//                     var countDown = 60;
//                     var timer = setInterval(function () {
//                         countDown -= 1;
//                         if (countDown > 0) {
//                             $this.text(countDown + "秒后重新发送");
//                         } else {
//                             $this.text("获取验证码");
//                             bindCaptchaBtnClick();
//                             clearInterval(timer);
//                         }
//                     }, 1000);
//                     alert("captcha send success...");
//                 } else {
//                     alert(res['message']);
//                 }
//             }
//         })
//     });
// }
//
// $(function () {
//     // var csrftoken = $('meta[name=csrf-token]').attr('content')
//     // $.ajaxSetup({
//     //     beforeSend: function (xhr, settings) {
//     //         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
//     //             xhr.setRequestHeader("X-CSRFToken", csrftoken)
//     //         }
//     //     }
//     // })
//     bindCaptchaBtnClick();
// });

