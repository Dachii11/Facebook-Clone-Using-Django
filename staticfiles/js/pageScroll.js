$(document).ready(function(){
	if (localStorage.getItem("my_app_name_here_quote_scroll")!=null){
		$(window).scrollTop(localStorage.getItem('my_app_name_here_quote_scroll'));
	}
	$(window).on("scroll",function(){
		localStorage.setItem('my_app_name_here_quote_scroll',$(window).scrollTop());
	})
})