#!/usr/bin/python

import argparse
import pycurl
import shutil
import subprocess
import os
import yaml


class Mapy():

    def __init__(self):
        config_file = open('/etc/mapy.conf', 'r')
        config_yaml = yaml.load(config_file)

        self.server_url = config_yaml["server"]

    def get_map(self, url):
        map_dir = 'csgo/maps/'
        file_name = url.split('/')[-1]

        fp = open(file_name, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.server_url + '/' + file_name)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()
        shutil.move(file_name, map_dir + file_name)
        subprocess.call(['bzip2', '-d', map_dir + file_name])

    def sync_mapfiles(self):
        shutil.copyfile('csgo/maplist.txt', 'csgo/mapcycle.txt')

    def add_map(self, args):
        print "adding", args.name
        self.get_map(self.server_url + args.name + '.bsp.bz2')

        with open('csgo/maplist.txt', 'ab+') as f:
            if args.name not in f.read():
                f.write(args.name + '\n')
            else:
                print args.name, "already in maplist.txt!"

        print args.name, "successfully added!"
        self.sync_mapfiles()


    def remove_map(self, args):
        print "removing", args.name
        output = []

        map_file = 'csgo/maps/' + args.name + '.bsp'

        if os.path.isfile(map_file):
            print "deleting", map_file
            os.remove(map_file)

        with open('csgo/maplist.txt', 'ab+') as maplist_file:
            for line in maplist_file:
                if line.strip() != args.name:
                    output.append(line)

        with open('csgo/maplist.txt', 'w') as maplist_file:
            maplist_file.writelines(output)

        print args.name, "successfully removed!"
        self.sync_mapfiles()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('name')
    parser_add.set_defaults(func=Mapy().add_map)

    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('name')
    parser_remove.set_defaults(func=Mapy().remove_map)

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

    #shutil.copyfile(maplist_file, options.root_dir + 'csgo/mapcycle.txt')


if __name__ == '__main__':
    main()
