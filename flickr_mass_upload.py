#! /usr/bin/env python2

import sys, os
import flickrapi
import xml.etree.ElementTree

if len(sys.argv) < 2:
  sys.stderr.write("usage: %s <filename> ..." % sys.argv[0])
  sys.exit(1)

def auth():
    api_key = "87af34fe62dafd3c5d6d4959ca92c193"
    api_secret = "18ecfc909af569af"
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    
    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token: raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))

    return flickr

def tags(filename):
    dirname = os.path.dirname(filename)
    res = ""
    while len(dirname) > 0:
        res = "%s %s" % (res, os.path.basename(dirname))
        dirname = os.path.dirname(dirname)
    return res

def upload(flickr, filename, tags):
    response = flickr.upload(filename=filename, tags=tags, is_public=0)

    if response.attrib["stat"] == "ok":
        photoid = response.find("photoid").text
        print("%s: stat:OK id:%s"% (filename, photoid))
    else:
        print("%s: stat:FAIL\n%s" % (filename, xml.etree.ElementTree.tostring(response)))

flickr = auth()
for filename in sys.argv[1:len(sys.argv)]:
    upload(flickr, filename, tags(filename))

