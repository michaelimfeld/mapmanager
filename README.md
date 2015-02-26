# mapy
Mapy is a simple tool to manage custom cs:go maps on your server. The maps will be downloaded from a fastdl server (webserver with directory listing enabled), which can be specified in the mapy config file.

## installation

    debuild -us -uc
    sudo dpkg -i ../mapy_0.00.01_amd64.deb

Don't forget to change the config file: /etc/mapy.conf!

    server: https://server.ch/csgo/maps/

You can also set the root dir of your cs:go server. However if you have more than one cs:go server, leave it empty! Relative paths will be used then.

You also need to set the fastdl server url in csgo/cfg/server.cfg:

    sv_downloadurl "https://server.ch/csgo/"

## usage

Navigate to your cs:go server's root dir:

    cd ~/server/csgo/

To add or remove maps simply do:

    mapy add surf_mesa
    mapy remove surf_mesa

To see a list of all available/installed maps:

    mapy list

Mapy will sync maplist.txt and mapcycle.txt!
