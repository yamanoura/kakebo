function search(){
    var st_year = $('#search_trade_year').val()

    if(vyear(st_year)){
	var target = document.getElementById("search_form");
	target.method = 'get'
	target.submit();
    }else{
	alert('利用できない年度が入力されました')
    }
}

