# mapy
Mapy is a simple tool to manage custom cs:go maps on your server. The maps will be downloaded from a fastdl server (webserver with directory listing enabled), which can be specified in the mapy config file.

## installation

    debuild -us -uc
    sudo dpkg -i ../mapy_0.00.01_amd64.deb

Don't forget to change the config file: /etc/mapy.conf!

## usage

Navigate to your cs:go server's root dir:

    cd ~/server/csgo/

To add or remove maps simply do:

    mapy add surf_mesa
    mapy remove surf_mesa

You need to set the fastdl server url in csgo/cfg/server.cfg:

    sv_downloadurl "https://server.ch/csgo/"
