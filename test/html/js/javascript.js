
let sock = new WebSocket("ws://localhost:9000");

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

function increaseMasterVolume(){
    sock.send('{"command": "increaseMasterVolume"}')
}
function decreaseMasterVolume(){
    sock.send('{"command": "decreaseMasterVolume"}')
}

function playFile(filePath){
    sock.send('{"command": "playFile", "absolutePath": "'+filePath+'"}');
}

function pauseFile(filePath){
    sock.send('{"command": "pauseFile", "absolutePath": "'+filePath+'"}');
}
