function search(){
    var project_select = $('#search_project_select').val();

    if(project_select!=''){
	var target = document.getElementById("search_form");
	target.method = 'get'
	target.submit();
    }else{
	alert('Projectが選択されていません')
    }
}

