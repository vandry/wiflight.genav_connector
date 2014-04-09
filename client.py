#!/usr/bin/python

import urllib
import pycurl
import cStringIO as StringIO
import json
import datetime

def format_datetime(datetime, milliseconds):
    """Return a date stamp with milliseconds in the format in which
    GenAV requires it."""
    return (
        datetime.strftime("%Y/%m/%d"),
        datetime.strftime("%H:%M"),
        datetime.strftime("%S") + ("%03d" % (milliseconds,))
    )

def parse_datetime(entry):
    """Reverse of format_datetime"""
    d = datetime.datetime.strptime(entry['EntryDate'], "%Y/%m/%d")
    t = datetime.datetime.strptime(entry['EntryTime'], "%H:%M")
    s = int(entry['EntrySecs'][0:2])
    ms = int(entry['EntrySecs'][2:])
    return d.replace(hour=t.hour, minute=t.minute, second=s), ms

class HTTPError(Exception):
    def __init__(self, url, code, message):
        if message:
            Exception.__init__(self, "%d %s" % (code, message))
        else:
            Exception.__init__(self, str(code))
        self.url = url
        self.code = code
        self.message = message

class GenAVClient(object):
    def __init__(self, baseurl, CompCode):
        self.baseurl = baseurl
        self.CompCode = CompCode
        self.curl_handle = pycurl.Curl()

    def request(self, url_tail, **kwargs):
        args = dict(kwargs)
        args['sCompCode'] = self.CompCode
        url = self.baseurl + url_tail + "?" + urllib.urlencode(args)
        req = self.curl_handle
        req.setopt(pycurl.URL, url)
        outbody = StringIO.StringIO()
        req.setopt(pycurl.WRITEFUNCTION, outbody.write)
        header = []
        req.setopt(pycurl.HEADERFUNCTION, header.append)
        req.setopt(pycurl.SSL_VERIFYPEER, 1)
        req.perform()
        code = req.getinfo(pycurl.RESPONSE_CODE)
        if code >= 200 and code < 300:
            content_type = req.getinfo(pycurl.CONTENT_TYPE)
            req.reset()
            return json.loads(outbody.getvalue())
        req.reset()
        status_line = None
        while True:
            tok = header[0].split(None, 2)
            if tok[0].startswith('HTTP/') and not ':' in tok[0] and tok[1] == '100':
                header.pop(0)
                if header[0] == '\r\n' or header[0] == '\n':
                    header.pop(0)
            else:
                break
        tok = header[0].split(None, 2)
        if tok[0].startswith('HTTP/') and not ':' in tok[0]:
            status_line = tok[2]
        if status_line.endswith('\r\n'):
            status_line = status_line[:-2]
        elif status.endswith('\n'):
            status_line = status_line[:-1]
        raise HTTPError(self.baseurl + url, code, status_line)

    def ActivityUpdates(self, datetime, milliseconds):
        dDate, sTime, sSecs = format_datetime(datetime, milliseconds)
        return self.request("ActivityUpdates", dDate=dDate, sTime=sTime, sSecs=sSecs)

    def DataUpdates(self, table, datetime, milliseconds):
        dDate, sTime, sSecs = format_datetime(datetime, milliseconds)
        return self.request(
            "DataUpdates", sTable=table,
            dDate=dDate, sTime=sTime, sSecs=sSecs
        )

    def DataFull(self, table):
        return self.request("DataFull", sTable=table)
