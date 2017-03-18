function vdate(v_date){
    var replaced_date = v_date.replace(/-/g,'');
    var year  = replaced_date.substr(0,4);
    var month = replaced_date.substr(4,2);
    var day   = replaced_date.substr(6,2);

    var ymd = new Date(year,month,day);

    if(ymd.getFullYear()==year &&
       ymd.getMonth()==month &&
       ymd.getDate()==day){

	return true;
    }else{
	return false;
    }
}




