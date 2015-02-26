#!/usr/bin/python

import argparse
import pycurl
import shutil
import subprocess
import os
import yaml
import urllib2
import re


class Mapy():

    SUCCESS = '\033[92m'
    WARN = '\033[93m'
    ENDC = '\033[0m'

    def __init__(self):
        config_file = open('/etc/mapy.conf', 'r')
        config_yaml = yaml.load(config_file)

        self.server_url = config_yaml["server"]
        self.root_dir = config_yaml["rootdir"]
        self.map_dir = self.root_dir + 'csgo/maps/'

    def get_map(self, url):
        file_name = url.split('/')[-1]

        fp = open(file_name, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.server_url + '/' + file_name)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()
        shutil.move(file_name, self.map_dir + file_name)
        subprocess.call(['bzip2', '-d', self.map_dir + file_name])

    def sync_mapfiles(self):
        shutil.copyfile(self.root_dir + 'csgo/maplist.txt', self.root_dir + 'csgo/mapcycle.txt')

    def add_map(self, args):
        print('downloading ' + args.name)
        self.get_map(self.server_url + args.name + '.bsp.bz2')

        with open(self.root_dir + 'csgo/maplist.txt', 'ab+') as f:
            if args.name not in f.read():
                f.write(args.name + '\n')
            else:
                print(Mapy.WARN + args.name + 'already in maplist.txt!' + Mapy.ENDC)

        print(Mapy.SUCCESS + args.name + ' successfully added!' + Mapy.ENDC)
        self.sync_mapfiles()


    def remove_map(self, args):
        print "removing", args.name
        output = []

        map_file = self.map_dir + args.name + '.bsp'

        if os.path.isfile(map_file):
            print "deleting", map_file
            os.remove(map_file)

        with open(self.root_dir + 'csgo/maplist.txt', 'ab+') as maplist_file:
            for line in maplist_file:
                if line.strip() != args.name:
                    output.append(line)

        with open(self.root_dir + 'csgo/maplist.txt', 'w') as maplist_file:
            maplist_file.writelines(output)

        print args.name, "successfully removed!"
        self.sync_mapfiles()

    def list_maps(self, args):

        installed = []
        for file in os.listdir(self.map_dir):
            if file.endswith(".bsp"):
                installed.append('.'.join(file.split('.')[:-1]))

        for map_url in self.get_map_urls():
            map_name = '.'.join(map_url.split('.')[:-2])
            if map_name in installed:
                print(Mapy.SUCCESS + "[INSTALLED] " + map_name + Mapy.ENDC)
            else:
                print "[AVAILABLE]", map_name


    def get_map_urls(self):
        pattern = r'href=[\'"]?([^\'" >]+)'
        response = urllib2.urlopen(self.server_url).read()

        urls = []
        for map_link in re.findall(pattern, response):
            if 'bz2' in map_link:
                urls.append(map_link)
        return urls


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add', help='add map to cs:go server')
    parser_add.add_argument('name', help='map name')
    parser_add.set_defaults(func=Mapy().add_map)

    parser_remove = subparsers.add_parser('remove', help='remove map from cs:go server')
    parser_remove.add_argument('name', help='map name')
    parser_remove.set_defaults(func=Mapy().remove_map)

    parser_list = subparsers.add_parser('list', help='list all installed maps')
    parser_list .set_defaults(func=Mapy().list_maps)

    args = parser.parse_args()
    args.func(args)

    #pattern = r'href=[\'"]?([^\'" >]+)'
    #response = urllib2.urlopen(options.fastdl).read()
    #maplist_file = options.root_dir + "csgo/maplist.txt"

    #for fn in re.findall(pattern, response):
        #if 'bz2' in fn and options.search in fn:
            #print "downloading", fn

            #fp = open(fn, "wb")
            #curl = pycurl.Curl()
            #curl.setopt(pycurl.URL, options.fastdl + '/' + fn)
            #curl.setopt(pycurl.WRITEDATA, fp)
            #curl.perform()
            #curl.close()
            #fp.close()
            #shutil.move(fn, map_dir + fn)
            #subprocess.call(['bzip2', '-d', map_dir + fn])

            #map_name = fn.split('.')[0]
            #with open(maplist_file, 'a') as maplist:
                #maplist.write(map_name + '\n')



if __name__ == '__main__':
    main()
