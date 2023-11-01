const nextBtn = document.querySelector(".stories-container .next-btn");
const previousBtn = document.querySelector(".stories-container .previous-btn");
const storiesContent = document.querySelector(".stories-container .content");

nextBtn.addEventListener('click',()=>{
	storiesContent.scrollLeft+=300;
});

previousBtn.addEventListener('click',()=>{
	storiesContent.scrollLeft-=300;
});

storiesContent.addEventListener("scroll",()=>{
	if(storiesContent.scrollLeft<=0){
		previousBtn.classList.remove("active");
	} else {
		previousBtn.classList.add("active");
	}
	let maxScrollValue = storiesContent.scrollWidth-storiesContent.clientWidth-0;
	if(storiesContent.scrollLeft>=maxScrollValue){
		nextBtn.classList.remove("active");
	} else {
		nextBtn.classList.add("active");
	}
})