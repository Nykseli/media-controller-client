#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "Please run as root"
    exit 1
fi

if [[ ! -f "media-controller" ]]
then
    echo "Create media-controller file from media-controller.sh.template"
    exit 1
fi

cp media-controller /etc/init.d/
chown root:root /etc/init.d/media-controller
chmod a+x /etc/init.d/media-controller
cd /etc/init.d/
update-rc.d media-controller defaults
