const storiesFullView = document.querySelector(".stories-full-view");
const closeBtn = document.querySelector(".close-btn");
const stories = document.querySelector(".stories");
const AllStories = document.querySelectorAll(".stories .story");
const storyImageFull = document.querySelector(".stories-full-view .story");
const storyAuthorFull = document.querySelector(".stories-full-view .story .author");
const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
const previousBtnFull = document.querySelector(".stories-full-view .previous-btn");

let currentActive = 0;
const OpenStories = () => {
	for(let i=0; i<AllStories.length; ++i){
		AllStories[i].addEventListener("click",()=>{
			showFullView(i);
		})
	}
}
OpenStories();
const showFullView = (index) => {
	currentActive = index;
	updateFullView();
	storiesFullView.classList.add("active");
}
closeBtn.addEventListener("click",()=>{
	storiesFullView.classList.remove("active");
	removeImgVid();
})
const updateFullView = ()=>{
	removeImgVid();    
	let node;
	chatSocket.send(JSON.stringify({
            "story_id":AllStories[currentActive].id,
            "my_profile":my_profile,
        }));
	AllStories[currentActive].childNodes[1].childNodes[1].style.borderColor = 'rgba(0,0,0,0.8)';
	if (AllStories[currentActive].children[1].nodeName=="VIDEO") {
		node = document.createElement("video");
		node.setAttribute("autoplay","autoplay");
	} else {
	 	node = document.createElement("img");
	 }
	node.src = AllStories[currentActive].children[1].currentSrc;
	storyAuthorFull.innerHTML = AllStories[currentActive].children[2].innerHTML;
	storyImageFull.appendChild(node);
	
}
nextBtnFull.addEventListener("click",()=>{
	if(currentActive>=AllStories.length-1) return;
	currentActive++;
	updateFullView();
})
previousBtnFull.addEventListener("click",()=>{
	if(currentActive<=0) return;
	currentActive--;
	updateFullView();
})

const removeImgVid = () => {
	let data = new Set([
			...previous_images = storyImageFull.getElementsByTagName("img"),
			...previous_videos = storyImageFull.getElementsByTagName("video")
		]);
	data.forEach(a=>{storyImageFull.removeChild(a)});
}