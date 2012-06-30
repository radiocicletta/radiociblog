#!/bin/env python

import urllib2
import json
import sys, os

# {
#            "url": "http://www.mixcloud.com/radiocicletta/playlists/orcotrio/",
#            "owner": {
#                "url": "http://www.mixcloud.com/radiocicletta/",
#                "username": "radiocicletta",
#                "name": "radiocicletta",
#                "key": "/radiocicletta/",
#                "pictures": {
#                    "medium": "http://d27ylsxkm6728c.cloudfront.net/w/100/h/100/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "extra_large": "http://d27ylsxkm6728c.cloudfront.net/w/600/h/600/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "large": "http://d27ylsxkm6728c.cloudfront.net/w/300/h/300/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "medium_mobile": "http://d27ylsxkm6728c.cloudfront.net/w/80/h/80/q/75/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "small": "http://d27ylsxkm6728c.cloudfront.net/w/25/h/25/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "thumbnail": "http://d27ylsxkm6728c.cloudfront.net/w/50/h/50/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524"
#                }
#            },
#            "name": "OrcoTrio",
#            "key": "/radiocicletta/playlists/orcotrio/",
#            "slug": "orcotrio"
#        }
#
#         {
#            "listener_count": 0,
#            "name": "L'ultima Mezzorca-27/10/11",
#            "tags": [
#                {
#                    "url": "http://www.mixcloud.com/tag/chillout/",
#                    "name": "Chillout",
#                    "key": "/tag/chillout/"
#                },
#                {
#                    "url": "http://www.mixcloud.com/tag/reading/",
#                    "name": "Reading",
#                    "key": "/tag/reading/"
#                }
#            ],
#            "url": "http://www.mixcloud.com/radiocicletta/lultima-mezzorca-271011/",
#            "pictures": {
#                "medium": "http://d1lolb6yyp8wyu.cloudfront.net/w/100/h/100/q/85/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg",
#                "extra_large": "http://d1lolb6yyp8wyu.cloudfront.net/w/600/h/600/q/85/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg",
#                "large": "http://d1lolb6yyp8wyu.cloudfront.net/w/300/h/300/q/85/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg",
#                "medium_mobile": "http://d1lolb6yyp8wyu.cloudfront.net/w/80/h/80/q/75/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg",
#                "small": "http://d1lolb6yyp8wyu.cloudfront.net/w/25/h/25/q/85/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg",
#                "thumbnail": "http://d1lolb6yyp8wyu.cloudfront.net/w/50/h/50/q/85/upload/images/extaudio/5fc6c2f9-0ca7-4fbb-adee-2c6e0cbade47.jpg"
#            },
#            "updated_time": "2011-11-14T00:00:27Z",
#            "play_count": 8,
#            "comment_count": 0,
#            "percentage_music": 54,
#            "user": {
#                "url": "http://www.mixcloud.com/radiocicletta/",
#                "username": "radiocicletta",
#                "name": "radiocicletta",
#                "key": "/radiocicletta/",
#                "pictures": {
#                    "medium": "http://d27ylsxkm6728c.cloudfront.net/w/100/h/100/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "extra_large": "http://d27ylsxkm6728c.cloudfront.net/w/600/h/600/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "large": "http://d27ylsxkm6728c.cloudfront.net/w/300/h/300/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "medium_mobile": "http://d27ylsxkm6728c.cloudfront.net/w/80/h/80/q/75/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "small": "http://d27ylsxkm6728c.cloudfront.net/w/25/h/25/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524",
#                    "thumbnail": "http://d27ylsxkm6728c.cloudfront.net/w/50/h/50/q/85/upload/images/profile/6881a983-9e67-434b-859b-d06a5ab07524"
#                }
#            },
#            "key": "/radiocicletta/lultima-mezzorca-271011/",
#            "created_time": "2011-10-28T12:55:44Z",
#            "audio_length": 1938,
#            "slug": "lultima-mezzorca-271011",
#            "favorite_count": 0
#        }
#    ],
#
#
# foreach item in http://api.mixcloud.com/radiocicletta/playlists/ 
#       foreach cloud in http://api.mixcloud.com/radiocicletta/playlists/$item/cloudcasts/
#           store title, url, created_time, pictures, audio_length



def harvest(path, idxname):

    base_url = "http://api.mixcloud.com"
    username = "radiocicletta"

    jsonidx = open("%s/%s.json" % (path, idxname), 'w')
    jsonidxobj = { "name": idxname, "playlists":{} }
    
    try:
        result = urllib2.urlopen("%s/%s/playlists/" % (base_url, username))
        playlists = json.loads(result.read())
    except:
        playlists =  { data:[] }


    for plist in playlists["data"]:
        js = open("%s/%s/%s.json" % (path, idxname, plist['slug']), 'w')
        try:
            result = urllib2.urlopen("%s/%s/playlists/%s/cloudcasts/" % (base_url, username, plist['slug']))
            js.write(result.read())
            jsonidxobj["playlist"][plist["slug"]] = "%s/%s" % (idxname, plist['slug'])
        except:
            pass
        finally:
            js.close()

    jsonidx.write(json.dumps(jsonidxobj))
    jsonidx.close()

if __name__ == "__main__":
    if not len(sys.argv):
        sys.exit(0)

    path = sys.argv[1]
    idx = sys.argv[2]
    harvest(path, idx)
