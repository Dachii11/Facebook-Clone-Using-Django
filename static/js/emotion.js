let icons = document.querySelectorAll(".container");
body = document.querySelector("body");
let object = document.querySelectorAll(".main .center .friends_post .like .like_icon .emoji_list");

let events = ['mouseover','click'];
for (let i = 0; i < object.length; i++){
        object[i].addEventListener('mouseover',function(event) {
            event.preventDefault();
            for (let j of icons){
                if (j.id == object[i].id){
                    j.style.display = 'flex';
                } else {
                    j.style.display = 'none';
                }
            }
        })
}

body.addEventListener("click",function(){
    for(let emotions of icons){
        emotions.style.display = 'none';
    }
})