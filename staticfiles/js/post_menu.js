drops = document.querySelectorAll('.dropdown');
    $(document).on("click",".menu",function(){
        //this.style.display="none";
        let id = this.id.toString();
        for (let i = 0; i < drops.length; i++){
              if (drops[i].id==id){
                drops[i].style.display = "block";
            } else {
                drops[i].style.display ='none'; 
            }
        }
    })
body.addEventListener("click",function(){
    for(let drop of drops){
        drop.style.display = 'none';
    }
})