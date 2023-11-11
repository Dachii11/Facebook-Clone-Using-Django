const my_profile = JSON.parse(document.getElementById("json-username").textContent);    
const chatSocket = new WebSocket('wss://'+window.location.host+"/ws/accounts/profile/"+my_profile+'/');

console.log("h");

chatSocket.onclose = function(e){
    console.log("WebSocket Closed!");
}

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);
    document.querySelector(".new-msg").innerHTML=data.new_notification;
    document.querySelector(".not").innerHTML=data.new_notification_count;
    if(data.new_notification_count){
        document.querySelector(".home-not-disp").innerHTML=data.new_notification_count;
    }
}

setInterval(function(){
    chatSocket.send(JSON.stringify({
        "ask_for_new_message":"ask_for_new_message",
        "my_profile":my_profile,
    }));
    return false;
},1000);