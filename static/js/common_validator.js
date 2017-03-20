function vdate(v_date){
    var replaced_date = v_date.replace(/-/g,'');
    var year  = replaced_date.substr(0,4);
    var month = replaced_date.substr(4,2);
    var day   = replaced_date.substr(6,2);
    var str_end = replaced_date.substr(8);

    var ymd = new Date(year,month,day);

    if(ymd.getFullYear()==year &&
       ymd.getMonth()==month &&
       ymd.getDate()==day &&
       str_end == ''){
	return true;
    }else{
	return false;
    }
}

function vmoney(v_money){
//    var replaced_money = v_money.replace(/,/g,'');
    var pattern = /^[-]?([1-9]\d*|0)(\.\d+)?$/;

    return pattern.test(v_money);
}



