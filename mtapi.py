import urllib2
import json
import os
import httplib
import logging
import requests

import orm

productversion="v2.2" #FIXME: hardcoded

# mtorigin = "https://moztrap.mozilla.org"
# mtorigin = "http://0.0.0.0:8080"
mtorigin = "http://requestb.in/1b8n1md1"

# Download
def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = mtorigin + "/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "/?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def downloadSuiteById(sid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = (mtorigin + "/api/v1/caseversion/"
           "?case__suites={sid}&productversion__version={productversion}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def clone(resource_type, sid, dirname="./"):
    output = ""
    if resource_type == "caseversion":
        query = str(sid)
        logging.info("Downloading CaseVersion " + query + " ...")
        result = downloadCaseversionById(query)
        output = orm.formatCaseversion(result)

    elif resource_type == "suite":
        query = str(sid)
        logging.info("Downloading Suite " + query + " ...")
        result = downloadSuiteById(query)
        output = orm.formatSuite(result, sid)

    filename = dirname + resource_type + "_" + str(sid) + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as file_:
            file_.write(output)
    logging.info(filename + " created")


def cloneByURL(url, dirname="./"):
    (resource_type, rid) = orm.parseURL(url)

    clone(resource_type, rid, dirname)


#Upload

def push(filename):
    # Read the file
    # Determine its type (caseversion? suite?)
    # Call forcePushCaseversion or forcePushSuite
    # http_connection = httplib.HTTPConnection(mtorigin, mtport)
    with open(filename, 'r') as f:
        caseversion = orm.parseCaseversion(''.join(f.readlines()))
        forcePushCaseversion(caseversion, requests)


def forcePushCaseversion(caseversion, requestlib):
    # http_connection(mtorigin, mtport)
    # http_connection.request("PUT", "/api/v1/caseversion/88", caseversion)
    # request = urllib2.Request(mtorigin, data=json.dumps(caseversion))

#    request = urllib2.Request(mtorigin, data=caseversion)
#    request.add_header('Content-Type', 'text/json')
#    request.get_method = lambda: 'PUT'
#    url = opener.open(request)
    requestlib.put(mtorigin, data=json.dumps(caseversion))

    # http_connection.request("GET", "/api/v1/caseversion/88", caseversion)
    # response = http_connection.getresponse();
    #logging.info(url)
