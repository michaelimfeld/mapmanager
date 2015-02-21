#!/usr/bin/python

from optparse import OptionParser
import re
import urllib2
import pycurl
import shutil
import subprocess
import os


def main():
    parser = OptionParser()
    parser.add_option("-f", "--fastdl", dest="fastdl", help="fastdl url to search for maps")
    parser.add_option("-r", "--rootdir", dest="root_dir", help="csgo server root dir")
    parser.add_option("-s", "--search", dest="search", help="only include maps which contain <search>")

    (options, args) = parser.parse_args()
    if not options.root_dir:
        print "please specify your server csgo root dir"
        return()

    if not options.fastdl:
        print "please specify a fastdl server url"
        return()

    options.search = (options.search if options.search else '')
    map_dir = options.root_dir + 'csgo/maps/'

    pattern = r'href=[\'"]?([^\'" >]+)'
    response = urllib2.urlopen(options.fastdl).read()
    maplist_file = options.root_dir + "csgo/maplist.txt"

    if os.path.isfile(maplist_file):
        os.remove(maplist_file)

    for fn in re.findall(pattern, response):
        if 'bz2' in fn and options.search in fn:
            print "downloading", fn

            fp = open(fn, "wb")
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, options.fastdl + '/' + fn)
            curl.setopt(pycurl.WRITEDATA, fp)
            curl.perform()
            curl.close()
            fp.close()
            shutil.move(fn, map_dir + fn)
            subprocess.call(['bzip2', '-d', map_dir + fn])


            map_name = fn.split('.')[0]
            with open(maplist_file, 'a') as maplist:
                maplist.write(map_name + '\n')

    shutil.copyfile(maplist_file, options.root_dir + 'csgo/mapcycle.txt')


if __name__ == '__main__':
    main()
