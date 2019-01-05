# Mediacontroller Server

Server part of the remote media controller see the client [here](https://github.com/Nykseli/android-media-controller)

## How to run

```
git clone https://github.com/Nykseli/media-controller-server
cd media-controller-server
python3 src/controller.py
```

## Config

You can put the [config.json](https://github.com/Nykseli/media-controller-server/blob/master/config.json.example) file to the project root or in ~/.MediaControllerClient/config.json

### Config structure

| Key | Type | Description |
|-----| -----| ------      |
| vlc |Object| Contains vlc configs|
| vlc.allowedFilePaths | Array | Contains list of allowed paths that can browsed by client ( currently Android client supports only one path) |
| vlc.allowedFileTypes | Array | Contains list of allowed filetypes that can be browsed by client|

## Websocket API

Controlling divice with client works by sending text in json format to server.
Basic structure is:
```
{
    "interface": <Interface that command uses e.g. vlc>,
    "command": <Command string>,
    "additionalInfo": {
        <Object that contains additional info that the command can use>
    }
}
```

### Interfaces

Interfaces are as follows:

* audio
  * Used to control system audio
* config
  * Used to get configuration from server
* general
  * Used to control system settings e.g. volume, mouse and keyboard input, etc
* mouse
  * Used to emulate mouse functionality. e.g. movement and clicks

* vlc
  * Used to control Vlc mediaplayer

### Api doc

Currently following commands are implemented

|Interface|Command|Additional Info| Description|
| ------- | ----- | ----------- | ---------- |
| audio | decreaseMasterVolume | - | Decrease system volume |
| audio | increaseMasterVolume | - | Increase system volume |
| audio | muteMasterVolume | - | Mute system volume |
| config  | getConfig | - | Get config.json contents. <br /> Response format: ```{"config": <object from config.json>```
| general | getFilesAndFolders | "absolutePath": string | Get files and folders in ***absolutePath***. <br /> Response format: ```{"files": string[], "folders": string[], "currentPath": absolutePath}```|
| mouse | moveMouseX | "amount": int | Moves mouse on x axis by x amount that is defined by ***amount***. ***amount*** can be negative. |
| mouse | moveMouseY | "amount": int | Moves mouse on y axis by x amount that is defined by ***amount***. ***amount*** can be negative. |
| mouse | leftMouseClick | - | Click with left mouse button |
| mouse | setMousePosition | "x": int,  <br />"y": int | Set mouse position to ***x***,***y*** coordinate |
| vlc | pauseFile | - | Toggle vlc pause on/off |
| vlc | playFile | "absolutePath": string | Play file defined by ***absolutePath***|
