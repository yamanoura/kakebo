function vdate(v_date){
    var replaced_date = v_date.replace(/-/g,'');
    var in_year  = replaced_date.substr(0,4);
    var in_month = replaced_date.substr(4,2);
    var in_day   = replaced_date.substr(6,2);
    var str_end = replaced_date.substr(8);

    var ymd = '';
    var w_year = '';
    var w_month = '';
    var w_day = '';

    //monthは0〜11で12か月を表現する
    //0:1月、2:2月となる。11:12月となる
    ymd = new Date(in_year,in_month-1,in_day);

    w_year = ymd.getFullYear();
    w_month = ymd.getMonth()+1;
    w_day = ymd.getDate();

    if(w_year==in_year &&
       w_month==in_month &&
       w_day == in_day &&
       str_end == ''
      ){
	return true;
    }else{
	return false;
    }
}

function vmonth(v_year_month){
    v_date = v_year_month + '-01'
    var replaced_date = v_date.replace(/-/g,'');
    var in_year  = replaced_date.substr(0,4);
    var in_month = replaced_date.substr(4,2);
    var in_day   = replaced_date.substr(6,2);
    var str_end = replaced_date.substr(8);

    var ymd = new Date(in_year,in_month,in_day);

    var chk_year = '';
    var chk_month = '';
    
    if(in_month=='12'){
	// monthが12のとき、ymd.getFullYear()はyear+1となる
	w_year = ymd.getFullYear()-1;
	w_month = ymd.getMonth()+12;
	w_day = ymd.getDate();
    }else{
	w_year = ymd.getFullYear();
	w_month = ymd.getMonth();
	w_day = ymd.getDate();
    }

    if(w_year==in_year &&
       w_month==in_month &&
       w_day == in_day &&
       str_end == ''){
	return true;
    }else{
	return false;
    }
}


function vyear(v_year){
    v_date = v_year + '-01-01'
    var replaced_date = v_date.replace(/-/g,'');
    var in_year  = replaced_date.substr(0,4);
    var in_month = replaced_date.substr(4,2);
    var in_day   = replaced_date.substr(6,2);
    var str_end = replaced_date.substr(8);

    var ymd = new Date(in_year,in_month,in_day);

    var chk_year = '';
    var chk_month = '';
    
    if(in_month=='12'){
	// monthが12のとき、ymd.getFullYear()はyear+1となる
	w_year = ymd.getFullYear()-1;
	w_month = ymd.getMonth()+12;
	w_day = ymd.getDate();
    }else{
	w_year = ymd.getFullYear();
	w_month = ymd.getMonth();
	w_day = ymd.getDate();
    }

    if(w_year==in_year &&
       w_month==in_month &&
       w_day == in_day &&
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

