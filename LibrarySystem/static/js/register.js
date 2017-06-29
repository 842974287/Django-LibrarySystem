jQuery(document).ready(function($) {

$('#id_username').blur(function() {
	$("#user_error").css("display", "none");
	var username = $('#id_username').val();
	reg = /[\u4e00-\u9fa5]/
	if (reg.test(username)) {
		$("#user_remind").css("color", "#d82424").css("display", "inline").html("用户名不允许含有中文");
	}
	else if (username.length > 5) {
		$.ajax({
			url: '/UserCheck/',
			type: 'POST',
			dataType: 'json',
			data: {
				username:username,
			},
			success: function(data) {
				if (data.info == 1) {
					$("#user_remind").css("color", "#d82424").css("display", "inline");
					$("#user_remind").html("用户名已注册");
				}
				else {
					$("#user_remind").css("color", "green").css("display", "inline");
					$("#user_remind").html("合法用户名");
				}
			}
		});
	}
	else if (username.length != 0) {
		$("#user_remind").css("color", "#d82424").css("display", "inline");
		$("#user_remind").html("用户名至少6位");
	}
	else {
		$("#user_remind").css("color", "#d82424").css("display", "inline");
		$("#user_remind").html("用户名不能为空");
	}
});

$('#id_pwd2').blur(function() {
	$("#pwd2_error").css("display", "none");
	var pwd = $('#id_pwd').val();
	var pwd2 = $('#id_pwd2').val();
	if (pwd != pwd2) {
		$("#pwd2_remind").css("display", "inline");
		$("#pwd2_remind").html("二次输入密码不匹配");
	}
	else {
		$("#pwd2_remind").css("display", "none")
	}
});

$('#id_pwd').blur(function() {
	$("#pwd_error").css("display", "none");
	var pwd = $('#id_pwd').val();
	if (pwd === "") {
		$("#pwd_remind").css("display", "inline");
		$("#pwd_remind").html("密码不能为空");
	}
	else {
		$("#pwd_remind").css("display", "none")
	}
});

$('#id_phone').blur(function() {
	$("#phone_error").css("display", "none");
	var phone = $('#id_phone').val();
	if (phone === "") {
		$("#phone_remind").css("display", "inline");
		$("#phone_remind").html("手机号码不能为空");
	}
	else {
		$("#phone_remind").css("display", "none")
	}
});

});
