
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

function getConfig(){
    sock.send(commandBuilder("config", "getConfig"));
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

function playFiles(filePath){
    sock.send(commandBuilder("vlc", "playFiles", {"absolutePaths": filePath}));
}

function playNext(filePath){
    sock.send(commandBuilder("vlc", "playNextMedia"));
}

function playPrev(filePath){
    sock.send(commandBuilder("vlc", "playPreviousMedia"));
}

function getCurrentlyPlaying(filePath){
    sock.send(commandBuilder("vlc", "getCurrentlyPlaying", {"absolutePath": filePath}));
}

function increaseVlcVolume(){
    sock.send(commandBuilder("vlc", "increaseVolume"));
}

function decreaseVlcVolume(){
    sock.send(commandBuilder("vlc", "decreaseVolume"));
}

function muteVlcVolume(){
    sock.send(commandBuilder("vlc", "muteVolume"));
}

function pauseFile(filePath){
    sock.send(commandBuilder("vlc", "pauseFile"));
}
function fastForward(){
    sock.send(commandBuilder("vlc", "fastForward"));
}
function rewind(){
    sock.send(commandBuilder("vlc", "rewind"));
}

const ALL_ASCII_CHARS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~';
function inputString(message){
    sock.send(commandBuilder("keyboard", 'inputString', {'input': message}));
}
function pressEnter(){
    sock.send(commandBuilder("keyboard", 'pressEnter'));
}

function pressTab(){
    sock.send(commandBuilder("keyboard", 'pressTab'));
}
function pressBackSpace(){
    sock.send(commandBuilder("keyboard", 'pressBackSpace'));
}
