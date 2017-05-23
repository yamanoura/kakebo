function confirm(){
    error_flag = 0
    var st_date = $('#search_trade_date').val();
    var sdt_select = $('#search_dw_type_select').val();
    var sa_select = $('#search_at_select').val();

    if(!vdate(st_date)){
	error_flag = 1;
	alert('取引日に利用できない日付が入力されました');
    }

    if(sdt_select==""){
	error_flag = 1;
	alert('入出金種類が選択されていません');
    }

    if(sa_select==""){
	error_flag = 1;
	alert('科目が選択されていません');
    }

    if(error_flag==0){
	var target = document.getElementById("listform");
	$('<input>').attr({
	    type: 'hidden',
	    id: 'is_submit_flag',
	    name: 'is_submit_flag',
	    value: "1"
	}).appendTo('#div_is_submit_flag');

	target.method = 'get'
	target.submit();
    }
}

function update(){
    var st_date = $('#search_trade_date').val();
    var sdt_select = $('#search_dw_type_select').val();
    var sa_select = $('#search_at_select').val();

    $('<input>').attr({
	type: 'hidden',
	id: 'search_trade_date',
	name: 'search_trade_date',
	value: st_date
    }).appendTo('#div_search_trade_date');

    $('<input>').attr({
	type: 'hidden',
	id: 'search_dw_type_select',
	name: 'search_dw_type_select',
	value: sdt_select
    }).appendTo('#div_search_dw_type_select');

    $('<input>').attr({
	type: 'hidden',
	id: 'search_at_select',
	name: 'search_at_select',
	value: sa_select
    }).appendTo('#div_search_at_select');


    var target = document.getElementById("listform");
    $('<input>').attr({
	type: 'hidden',
	id: 'is_submit_flag',
	name: 'is_submit_flag',
	value: "2"
    }).appendTo('#div_is_submit_flag');

    target.method = 'get'
    target.submit();

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
	var target = document.getElementById("listform");
	target.method = 'get'
	target.submit();
    });
    
});
