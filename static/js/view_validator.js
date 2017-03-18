function ab_sum_search(){
    var st_date = $('#search_trade_date').val()

    if(vdate(st_date)){
	var target = document.getElementById("ab_sum_form");
	target.method = 'get'
	target.submit();
    }else{
	alert('利用できない日付が入力されました')
    }
}
