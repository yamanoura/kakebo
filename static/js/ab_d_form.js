function addupd(){
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
