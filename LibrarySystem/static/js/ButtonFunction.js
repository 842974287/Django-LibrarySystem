$(document).ready(function() {
	$('.borrowButton').click(function() {
		if(confirm('确定借阅？')) {
			$('.borrowButton').attr('disabled', 'disabled');
			var ISBN = $(this).attr("id");
			$.ajax({
				url: '/BorrowBook/',
				type: 'POST',
				dataType: 'json',
				data: {'ISBN': ISBN},
				success:function(callback){
					if (callback.info == 'ok'){
						alert("借书成功");
						window.location.reload();
					}
					else {
						alert(callback.info);
						window.location.reload();
					}
				}
			});
		}
	});
	$('.returnButton').click(function() {
		if(confirm('请收取罚金')) {
			$('.returnButton').attr('disabled', 'disabled');
			var ListId = $(this).attr("id");
			$.ajax({
				url: '/ReturnBook/',
				type: 'POST',
				dataType: 'json',
				data: {'ListId': ListId},
				success:function(callback){
					if (callback.info == 'ok'){
						alert("还书成功");
						window.location.reload();
					}
					else {
						alert(callback.info);
						window.location.reload();
					}
				}
			});
		}
	});
});
