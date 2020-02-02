function showUser() {
	console.log(window.localStorage.username)
	var label_username = $(".label-username");
	if (label_username.length > 0) {
		if (window.localStorage.username) {
			$(".btn-login").remove();
			$(".label-username").html(window.localStorage.username);
			$(".label-username").after('<a class="btn btn-primary btn-logout" href="#">注销</a>');
		} else {
			$(".label-username").html("");
			$(".label-username").after('<a class="btn btn-primary btn-login" href="login.html">登录/注册</a>');
		}
	}
	
}
	
$(document).ready(function(){
	showUser();
	
	$(".btn-logout").click(function(){
		var user = {
			username:window.localStorage.username
		}
		console.log(user)
		$.ajax({
			url:"logout",
			type:"POST",
			data:user,
			dataType:"json",
			success:function(data){
				console.log(data);
				window.localStorage.removeItem("username");
				window.location.reload();
			}
		});
	});
});