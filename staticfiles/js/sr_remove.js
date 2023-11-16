trash = document.querySelectorAll(".rule-remove .i");
	for(let i=0; i<trash.length;i++){
		trash[i].addEventListener("click",function(){
			document.querySelector(".rule-rm-btn").value=trash[i].id;
			document.querySelector(".remove").style.display="flex";
		})
		document.querySelector(".remove .s .top i").addEventListener("click",function () {
			document.querySelector(".remove").style.display="none";
		})
		document.querySelector(".cancel").addEventListener("click",function () {
			document.querySelector(".remove").style.display="none";
		})
	}
