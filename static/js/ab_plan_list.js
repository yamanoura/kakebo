function search(){
    var year_month = $('#search_plan_year_month').val();
    var error_flag = 0;

    if(!vmonth(year_month)){
	error_flag = 1;
	alert('予定年月に利用できない年月が入力されました');
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
