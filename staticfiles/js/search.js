document.querySelector("#search-input");
addEventListener("input",filterList);

function filterList(){
    const searchInput = document.querySelector("#search-input");
    const filter = searchInput.value.toLowerCase();
    const listItems = document.querySelectorAll(".list-group-item");
    if (filter==0){
        document.querySelector("#list-group").style.display = "none";
    } else {
        document.querySelector("#list-group").style.display = "block";
        listItems.forEach((item)=>{
            let text = item.textContent;
            let inp = filter.split(" ").slice(-1)[0].substr(1,);
            if (filter.split(" ").slice(-1)[0][0]=="@"){
                if (text.toLowerCase().includes(inp.toLowerCase())){
                    item.style.display = "";
                } else {
                    item.style.display = "none";
                }
            } else {
                document.querySelector("#list-group").style.display = "none";
            }
        });
    }
}