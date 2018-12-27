
let sock = new WebSocket("ws://192.168.0.19:9000");

sock.onopen = function(event){
    console.log(event);
}
sock.onmessage = function(event){
    console.log(JSON.parse(event.data));
}

function moveMouseX(amount){
    sock.send('{"command": "moveMouseX", "amount": '+amount+'}');
}

function moveMouseY(amount){
    sock.send('{"command": "moveMouseY", "amount": '+amount+'}');
}

function leftMouseClick(){
    sock.send('{"command": "leftMouseClick"}')
}

function getFiles(path){
    sock.send('{"command": "getFilesAndFolders", "absolutePath": "'+path+'"}')
}
