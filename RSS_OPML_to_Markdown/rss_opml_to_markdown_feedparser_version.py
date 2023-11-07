# -*- coding: UTF-8 -*-
import listparser
import tabulate
import feedparser
# import datetime
import sys
# import urllib3
import ssl
import requests
import json
import re
from time import mktime
# from datetime import datetime, timezone, date, timedelta
import datetime

# this part of code below comes from https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
# it is highly discouraged.
# try:
#    _create_unverified_https_context = ssl._create_unverified_context
#except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
#    pass
#else:
    # Handle target environment that doesn't support HTTPS verification
#    ssl._create_default_https_context = _create_unverified_https_context

name = "rss-opml-to-markdown"

def humanize_date_difference(now, otherdate=None, offset=None):
    # This part of code below comes from https://gist.github.com/nzjrs/207624
    if otherdate:
        dt =  now - otherdate
        offset = dt.seconds + (dt.days * 60*60*24)
    if offset:
        delta_s = offset % 60
        #print(delta_s)
        offset /= 60
        delta_m = offset % 60
        #print(delta_m)
        offset /= 60
        delta_h = offset % 24
        #print(delta_h)
        offset /= 24
        delta_d = offset
        #print(delta_d)
    else:
        raise ValueError("Must supply otherdate or offset (from now)")

    if delta_d > 1:
        if delta_d > 6:
            date = now + datetime.timedelta(days=-delta_d)
            #print(date)
            #print(date.strftime('%Y %B %d, %H:%M'))
            return date.strftime('%Y %B %d, %H:%M')
        else:
            # wday = now + datetime.timedelta(days=-delta_d, hours=-delta_h, minutes=-delta_m)
            # print(wday.strftime('%A'))
            # return wday.strftime('%A')
            return "%dd%dh ago" % (delta_d, delta_h)
    if delta_d == 1:
        return "Yesterday"
    if delta_h > 1:
        return "%dh%dm ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%dm%ds ago" % (delta_m, delta_s)
    else:
        return "%ds ago" % delta_s

def is_fetch_failed(item):
    return item[4] == 'fetch failed'

def is_no_entry(item):
    return item[4] == 'no entry'

# def duration(item)

def sort_rst(rst):
    # rst.sort(key=duration)
    rst.sort(key=is_no_entry)
    rst.sort(key=is_fetch_failed)
    return rst

def get_feed_content_using_requests(feed_url):
    try:
        # This part of code comes from https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
        # if hasattr(ssl, '_create_unverified_https_context'):
        #    ssl._create_default_https_context = ssl._create_unverified_https_context

        # This part of code comes from https://github.com/uvacw/inca/issues/162#issuecomment-318019000
        session = requests.Session()
        session.cookies['cookiewall'] = 'yes'
        feedpage = session.get(feed_url)
        response = feedparser.parse(feedpage.text)

        # print(response)
        if response.bozo is False:
           # if response.status == 200:
            return response
        else:
            return None
        # return None
    except Exception as e:
        print(e)
        return None
    
def get_feed_content(feed_url):
    try:
        
        response = feedparser.parse(feed_url)

        # print(response)
        if response.bozo is False:
            if response.status == 200:
                return response
            else:
                return None
        return None
    except Exception as e:
        print(e)
        return None

def is_url(url):
    """
    确认一个字符串是不是一个网页链接地址。

    Args:
        url: 要确认的字符串。

    Returns:
        True 表示是网页链接地址，False 表示不是网页链接地址。
    """

    url_pattern = re.compile(r'https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]+/?')
    match = url_pattern.match(url)

    return match is not None

def parse(file_name):
    # result = listparser.parse(file_name)
    # result = listparser.parse(open(file_name).read())
    with open(file_name, encoding='utf-8') as f:
    # with open(file_name) as f:
        result = listparser.parse(f.read())
    rst = []
    # 获取总数
    total = len(result['feeds'])
    feed_index = 0
    for feed in result['feeds']:
        # 获取当前循环次数
        feed_index = feed_index + 1

        # 计算百分比
        percentage = feed_index / total * 100

        # 打印百分比
        print(f"{percentage:.2f}%")
        # api_url = 'https://feedsearch.dev/api/v1/search?url=' + feed['url']
        print(feed['url'])
        feedcontent = get_feed_content(feed['url'])
        # print(feedcontent.headers['content-length'])
        if feedcontent and feedcontent != '{}':
            # print(feedcontent)
            item_count = len(feedcontent['entries'])
            if item_count > 0:
                #if 'published' in feedcontent.entries[0]:
                #    last_updated = feedcontent.entries[0]['published']
                #else:
                #    if 'updated' in feedcontent.feed:
                #        last_updated = feedcontent.feed['updated']
                #    else:
                #        last_updated = 'not found'
                if 'published_parsed' in feedcontent.entries[0] and feedcontent.entries[0].published_parsed != None:
                    if feedcontent.entries[0].published_parsed.tm_year >= 1971:
                        last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed)))
                        # duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed))
                    else:
                        last_updated = 'not found'
                elif 'updated_parsed' in feedcontent.entries[0] and feedcontent.entries[0].updated_parsed != None:
                    if feedcontent.entries[0].updated_parsed.tm_year >= 1971:
                        last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed)))
                        #duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed))
                    else:
                        last_updated = 'not found'
                else:
                    if 'published_parsed' in feedcontent.feed and feedcontent.feed.published_parsed != None:
                        temp = feedcontent.feed.published_parsed.tm_year
                        if temp >= 1971:
                            last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.feed.published_parsed)))
                            # duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.feed.published_parsed))
                        else:
                            last_updated = 'not found'
                    elif 'updated_parsed' in feedcontent.feed and feedcontent.feed.updated_parsed != None:
                        temp = feedcontent.feed.updated_parsed.tm_year
                        if temp >= 1971:
                            last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.feed.updated_parsed)))
                            # duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.feed.updated_parsed))
                        else:
                            last_updated = 'not found'
                    else:
                        last_updated = 'not found'

                if item_count > 1:
                    if 'published_parsed' in feedcontent.entries[0] and 'published_parsed' in feedcontent.entries[-1]:
                        if feedcontent.entries[0].published_parsed != None and feedcontent.entries[-1].published_parsed != None:
                            if feedcontent.entries[-1].published_parsed.tm_year >= 1971 and feedcontent.entries[0].published_parsed.tm_year >= 1971:
                                velocity = datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed))-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[-1].published_parsed))
                                # velocity = velocity.seconds/3600/24 + velocity.days
                                #print(feedcontent.entries[0].published_parsed)
                                #print(feedcontent.entries[-1].published_parsed)
                                if (velocity.seconds/3600/24 + velocity.days) > 0:
                                    velocity = '{:.2f}'.format(item_count/(velocity.seconds/3600/24 + velocity.days)) # item count per day, interpreted as publishing frequency
                                else:
                                    velocity = 'Not able to calculate'
                            else:
                                velocity = 'Not able to calculate'
                        else:
                            velocity = 'Not able to calculate'
                    elif 'updated_parsed' in feedcontent.entries[0] and 'updated_parsed' in feedcontent.entries[-1]:
                        if feedcontent.entries[0].updated_parsed != None and feedcontent.entries[-1].updated_parsed != None:
                            if feedcontent.entries[-1].updated_parsed.tm_year >= 1971 and feedcontent.entries[0].updated_parsed.tm_year >= 1971:
                                velocity = datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed))-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[-1].updated_parsed))
                                # velocity = velocity.seconds/3600/24 + velocity.days
                                #print(feedcontent.entries[0].updated_parsed)
                                #print(feedcontent.entries[-1].updated_parsed)
                                if (velocity.seconds/3600/24 + velocity.days) > 0:
                                    velocity = '{:.2f}'.format(item_count/(velocity.seconds/3600/24 + velocity.days)) # item count per day, interpreted as publishing frequency
                                else:
                                    velocity = 'Not able to calculate'
                            else:
                                velocity = 'Not able to calculate'
                        else:
                            velocity = 'Not able to calculate'
                    else:
                        velocity = 'Timestamp fetch failed'
                else:
                    velocity = 'Not able to calculate'
                
                if 'content-length' in feedcontent.headers:
                    content_length = feedcontent.headers['content-length']
                    print(content_length)
                else:
                    content_length = len(json.dumps(feedcontent))

                if 'language' in feedcontent.feed:
                    language = feedcontent.feed['language']
                else:
                    language = 'not found'
                
                # is_podcast = feedcontent[0]['is_podcast']
                if 'links' in feedcontent.entries[0]:
                  for key, value in feedcontent.entries[0].links[0].items():
                    if value == "enclosure":
                        is_podcast = True
                        break
                    else:
                        is_podcast = False
                else:
                  is_podcast = False
                
                for key in feedcontent.entries[0].keys():
                    if key.find("itunes") != -1:
                        is_podcast = is_podcast + True
                        break
                    else:
                        is_podcast = is_podcast + False
                
                if is_podcast >= 1:
                    is_podcast = True
                else:
                    is_podcast = False
                
                version = feedcontent.version
               
                titlestr=feed['title']
                titlestr=re.sub(r"\|", r"-", titlestr)
                
                # rst.append([feed['title'], feed['url'],last_updated,is_podcast,item_count,content_length,velocity,version])
                if len(feed['tags']) == 1:
                    if 'link' in feedcontent.feed:
                        if is_url(feedcontent.feed['link']):
                            rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                    elif 'links' in feedcontent.feed:
                        if 'href' in feedcontent.feed.links[0]:
                            if is_url(feedcontent.feed.links[0].href):
                                rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr,  'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                    else:
                        rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                else:
                    if 'link' in feedcontent.feed:
                        if is_url(feedcontent.feed['link']):
                            rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                    elif 'links' in feedcontent.feed:
                        if 'href' in feedcontent.feed.links[0]:
                            if is_url(feedcontent.feed.links[0].href):
                                rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                    else:
                        rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
            else:
                titlestr=feed['title']
                titlestr=re.sub(r"\|", r"-", titlestr)
                if len(feed['tags']) == 1:
                    if 'link' in feedcontent.feed:
                        if is_url(feedcontent.feed['link']):
                            rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                    elif 'links' in feedcontent.feed:
                        if 'href' in feedcontent.feed.links[0]:
                            if is_url(feedcontent.feed.links[0].href):
                                rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                    else:
                        rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                else:
                    if 'link' in feedcontent.feed:
                        if is_url(feedcontent.feed['link']):
                            rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                    elif 'links' in feedcontent.feed:
                        if 'href' in feedcontent.feed.links[0]:
                            if is_url(feedcontent.feed.links[0].href):
                                rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                    else:
                        rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
        else:
            feedcontent = get_feed_content_using_requests(feed['url'])
            if feedcontent and feedcontent != '{}':
            # print(feedcontent)
                item_count = len(feedcontent['entries'])
                if item_count > 0:
                    if 'published_parsed' in feedcontent.entries[0] and feedcontent.entries[0].published_parsed != None:
                        temp = feedcontent.entries[0].published_parsed.tm_year
                        if temp >= 1971:
                            last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed)))
                            #duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed))
                        else:
                            last_updated = 'not found'
                    elif 'updated_parsed' in feedcontent.entries[0] and feedcontent.entries[0].updated_parsed != None:
                        temp = feedcontent.entries[0].updated_parsed.tm_year
                        if temp >= 1971:
                            last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed)))
                            #duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed))
                        else:
                            last_updated = 'not found'
                    else:
                        if 'published_parsed' in feedcontent.feed and feedcontent.feed.published_parsed != None:
                            temp = feedcontent.feed.published_parsed.tm_year
                            if temp >= 1971:
                                last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.feed.published_parsed)))
                                #duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.feed.published_parsed))
                            else:
                                last_updated = 'not found'
                        elif 'updated_parsed' in feedcontent.feed and feedcontent.feed.updated_parsed != None:
                            temp = feedcontent.feed.updated_parsed.tm_year
                            if temp >= 1971:
                                last_updated = humanize_date_difference(datetime.datetime.now(),datetime.datetime.fromtimestamp(mktime(feedcontent.feed.updated_parsed)))
                                #duration = datetime.datetime.now()-datetime.datetime.fromtimestamp(mktime(feedcontent.feed.updated_parsed))
                            else:
                                last_updated = 'not found'
                        else:
                            last_updated = 'not found'

                    if item_count > 1:
                        if 'published_parsed' in feedcontent.entries[0] and 'published_parsed' in feedcontent.entries[-1]:
                            if  feedcontent.entries[0].published_parsed != None and feedcontent.entries[-1].published_parsed != None:
                                if feedcontent.entries[0].published_parsed.tm_year >= 1971 and feedcontent.entries[-1].published_parsed.tm_year >= 1971:
                                    #print(feedcontent.entries[0].published_parsed)
                                    #print(feedcontent.entries[-2].published_parsed)
                                    velocity = datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].published_parsed))-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[-1].published_parsed))
                                    # velocity = velocity.seconds/3600/24 + velocity.days
                                    if (velocity.seconds/3600/24 + velocity.days) > 0:
                                        velocity = '{:.2f}'.format(item_count/(velocity.seconds/3600/24 + velocity.days)) # item count per day, interpreted as publishing frequency
                                    else:
                                        velocity = 'Not able to calculate'
                                else:
                                    velocity = 'Not able to calculate'
                            else:
                                velocity = 'Not able to calculate'
                        elif 'updated_parsed' in feedcontent.entries[0] and 'updated_parsed' in feedcontent.entries[-1]:
                            if feedcontent.entries[0].updated_parsed != None and feedcontent.entries[-1].updated_parsed != None:
                                if feedcontent.entries[0].updated_parsed.tm_year >= 1971 and feedcontent.entries[-1].updated_parsed.tm_year >= 1971:
                                    velocity = datetime.datetime.fromtimestamp(mktime(feedcontent.entries[0].updated_parsed))-datetime.datetime.fromtimestamp(mktime(feedcontent.entries[-1].updated_parsed))
                                    # velocity = velocity.seconds/3600/24 + velocity.days
                                    #print(feedcontent.entries[0].updated_parsed)
                                    #print(feedcontent.entries[-1].updated_parsed)
                                    if (velocity.seconds/3600/24 + velocity.days) > 0:
                                        velocity = '{:.2f}'.format(item_count/(velocity.seconds/3600/24 + velocity.days)) # item count per day, interpreted as publishing frequency
                                    else:
                                        velocity = 'Not able to calculate'
                                else:
                                    velocity = 'Not able to calculate'
                            else:
                                velocity = 'Not able to calculate'
                        else:
                            velocity = 'Timestamp fetch failed'
                    else:
                        velocity = 'Not able to calculate'

                    if 'content-length' in feedcontent.headers:
                        content_length = feedcontent.headers['content-length']
                        print(content_length)
                    else:
                        content_length = len(json.dumps(feedcontent))

                    if 'language' in feedcontent.feed:
                        language = feedcontent.feed['language']
                    else:
                        language = 'not found'

                    # is_podcast = feedcontent[0]['is_podcast']
                    if 'links' in feedcontent.entries[0]:
                      for key, value in feedcontent.entries[0].links[0].items():
                        if value == "enclosure":
                            is_podcast = True
                            break
                        else:
                            is_podcast = False
                    else:
                      is_podcast = False
                
                    for key in feedcontent.entries[0].keys():
                        if key.find("itunes") != -1:
                            is_podcast = is_podcast + True
                            break
                        else:
                           is_podcast = is_podcast + False
                
                    if is_podcast >= 1:
                        is_podcast = True
                    else:
                        is_podcast = False
                
                    version = feedcontent.version

                    titlestr=feed['title']
                    titlestr=re.sub(r"\|", r"-", titlestr)

                    # rst.append([feed['title'], feed['url'],last_updated,is_podcast,item_count,content_length,velocity,version])
                    if len(feed['tags']) == 1:
                        if 'link' in feedcontent.feed:
                            if is_url(feedcontent.feed['link']):
                                rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        elif 'links' in feedcontent.feed:
                            if 'href' in feedcontent.feed.links[0]:
                                if is_url(feedcontent.feed.links[0].href):
                                    rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                                else:
                                    rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                    else:
                        if 'link' in feedcontent.feed:
                            if is_url(feedcontent.feed['link']):
                                rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        elif 'links' in feedcontent.feed:
                            if 'href' in feedcontent.feed.links[0]:
                                if is_url(feedcontent.feed.links[0].href):
                                    rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                                else:
                                    rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                            else:
                                rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],last_updated,item_count,content_length,velocity,language,version,is_podcast])
                else:
                    titlestr=feed['title']
                    titlestr=re.sub(r"\|", r"-", titlestr)
                    if len(feed['tags']) == 1:
                        if 'link' in feedcontent.feed:
                            if is_url(feedcontent.feed['link']):
                                rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        elif 'links' in feedcontent.feed:
                            if 'href' in feedcontent.feed.links[0]:
                                if is_url(feedcontent.feed.links[0].href):
                                    rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                                else:
                                    rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['tags'][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                    else:
                        if 'link' in feedcontent.feed:
                            if is_url(feedcontent.feed['link']):
                                rst.append([titlestr, feedcontent.feed['link'],feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        elif 'links' in feedcontent.feed:
                            if 'href' in feedcontent.feed.links[0]:
                                if is_url(feedcontent.feed.links[0].href):
                                    rst.append([titlestr, feedcontent.feed.links[0].href,feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                                else:
                                    rst.append([titlestr, 'not found or not a url starts with "http(s)://"',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                            else:
                                rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
                        else:
                            rst.append([titlestr, 'not found',feed['url'],feed['categories'][0][0],'no entry','no entry','no entry','no entry','no entry','no entry','no entry'])
            else:
                titlestr=feed['title']
                titlestr=re.sub(r"\|", r"-", titlestr)
                if len(feed['tags']) == 1:
                    rst.append([titlestr, 'fetch failed',feed['url'],feed['tags'][0],'fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed'])
                else:
                    rst.append([titlestr, 'fetch failed',feed['url'],feed['categories'][0][0],'fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed'])
        # print(tabulate.tabulate(rst, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    return rst

def print_to_std(feeds_list):
    # print(tabulate.tabulate(feeds_list, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length (bytes)','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    print(tabulate.tabulate(feeds_list, headers=['Sequence Number','Title', 'Site URL','Feed URL','Category','Last Updated','Item Count','Content Length (bytes)','The mean number of items per day','Language','Detected feed type version','Podcast feed or not'], tablefmt='pipe'))
    # for tag, feed_list in feeds_list.items():
    # for feed_list in feeds_list.items():
        # print("# " + tag + "\n")
        # print(tabulate.tabulate(feed_list, headers=["title", "url"], tablefmt="pipe"))
        # print("\n")


def print_to_file(feeds_list, filename):
    with open(filename, 'wt', encoding="utf-8") as f:
        # f.write(tabulate.tabulate(feeds_list, headers=["Title", "URL","Last Updated","Podcast","Item Count","Content Length (bytes)","The mean number of items per day","Detected feed type version"], tablefmt="pipe"))
        f.write(tabulate.tabulate(feeds_list, headers=["Sequence Number","Title","Site URL", "Feed URL","Category","Last Updated","Item Count","Content Length (bytes)","The mean number of items per day","Language","Detected feed type version","Podcast feed or not"], tablefmt="pipe"))
        # for tag, feed_list in feeds_list.items():
        # for feed_list in feeds_list.items():
            # f.write("# " + tag + "\n")
            # f.write(tabulate.tabulate(feed_list, headers=["title", "url"], tablefmt="pipe"))
            # f.write("\n")


def main():
    intro = """
    this is a help message
    """
    if len(sys.argv) == 1:
        print(intro)
        sys.exit()
    elif len(sys.argv) == 2:
        feeds_list = parse(sys.argv[1])
        feeds_list = sort_rst(feeds_list)
        feeds_list = [[i + 1] + item for i, item in enumerate(feeds_list)]
        print_to_std(feeds_list)
    elif len(sys.argv) == 3:
        feeds_list = parse(sys.argv[1])
        feeds_list = sort_rst(feeds_list)
        feeds_list = [[i + 1] + item for i, item in enumerate(feeds_list)]
        print_to_file(feeds_list, sys.argv[2])
        print("Finished !")
    else:
        print("Error: argv number doesn't match")
        exit(-1)


if __name__ == "__main__":
    main()