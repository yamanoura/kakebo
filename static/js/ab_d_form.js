function addupd(){

}

window.onload = function(){
    var flag = $('#id_ab_create_flag').val();

    if(flag==1){
	$('#id_plan_year_month').prop("disabled",true);
	$('#id_at').prop("disabled",true);
	$('#id_dwm').prop("disabled",true);
	$('#id_project').prop("disabled",true);
	$('#id_ab_desc').prop("disabled",true);
	$('#id_ab_money').prop("disabled",true);
    }
}


$(function() {
  // テキストボックスにフォーカス時、フォームの背景色を変化
    $('#id_trade_date,#id_at,#id_dwm,#id_project,#id_ab_desc,#id_ab_money')
    .focusin(function(e) {
      $(this).css('background-color', '#ffc');
    })
    .focusout(function(e) {
      $(this).css('background-color', '');
    });
});
