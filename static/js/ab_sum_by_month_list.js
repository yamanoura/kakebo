function search(){
    var st_month = $('#search_trade_month').val()

    if(vmonth(st_month)){
	var target = document.getElementById("search_form");
	target.method = 'get'
	target.submit();
    }else{
	alert('利用できない年月が入力されました')
    }
}

