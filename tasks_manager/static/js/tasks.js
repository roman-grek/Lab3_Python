$(document).ready(function () {
	$(document).on('click', '.checkbox', function() {
		$(this).parent().addClass('completed');
		$(this).attr('disabled', true);

		let uid = $(this).attr('data-uid');
		$.get("/tasks/complete/" + uid);
	});

	$(document).on('click', '.remove', function(){
		$(this).parent().remove();
	});

});