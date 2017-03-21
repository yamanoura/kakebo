function search(){
    var st_date_from = $('#search_trade_date_from').val();
    var st_date_to = $('#search_trade_date_to').val();
    var error_flag = 0;

    if(!vdate(st_date_from)){
	error_flag = 1;
	alert('取引日(From)に利用できない日付が入力されました');
    }

    if(!vdate(st_date_to)){ 
	error_flag = 1;
	alert('取引日(To)に利用できない日付が入力されました');
    }

    if(error_flag==0 && st_date_from > st_date_to){
	error_flag = 1;
	alert('取引日(From)の日付は取引日(To)より新しい日付は入力できません');
    }

    if(error_flag==0){
	var target = document.getElementById("search_form");
	target.method = 'get'
	target.submit();
    }
}

$(function() {
  // テキストボックスにフォーカス時、フォームの背景色を変化
    $('#search_trade_date_from,#search_trade_date_to,#search_dw_type_select,#search_at_select')
    .focusin(function(e) {
      $(this).css('background-color', '#ffc');
    })
    .focusout(function(e) {
      $(this).css('background-color', '');
    });

    $('#search_dw_type_select')
    .change(function(e) {
	var target = document.getElementById("search_form");
	target.method = 'get'
	target.submit();
    });
    
});
