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

