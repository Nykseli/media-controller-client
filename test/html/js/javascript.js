
let sock = new WebSocket("ws://localhost:9000");

sock.onopen = function(event){
    console.log(event);
}
sock.onmessage = function(event){
    console.log(JSON.parse(event.data));
}

function commandBuilder(interface, command, additionalInfo){
    if(additionalInfo){
        command = {
            "interface": interface,
            "command": command,
            "additionalInfo": additionalInfo
        }
    }else{
        command = {
            "interface": interface,
            "command": command,
        }
    }

    return JSON.stringify(command);
}

function moveMouseX(amount){
    sock.send(commandBuilder("general", "moveMouseX", {"amount": amount}));
}

function moveMouseY(amount){
    sock.send(commandBuilder("general", "moveMouseY", {"amount": amount}));
}

function leftMouseClick(){
    sock.send(commandBuilder("general", "leftMouseClick"));
}

function getFiles(path){
    sock.send(commandBuilder("general", "getFilesAndFolders", {"absolutePath": path}));
}

function increaseMasterVolume(){
    sock.send(commandBuilder("general", "increaseMasterVolume"));
}
function decreaseMasterVolume(){
    sock.send(commandBuilder("general", "decreaseMasterVolume"));
}

function playFile(filePath){
    sock.send(commandBuilder("vlc", "playFile", {"absolutePath": filePath}));
}

function pauseFile(filePath){
    sock.send(commandBuilder("vlc", "pauseFile"));
}
