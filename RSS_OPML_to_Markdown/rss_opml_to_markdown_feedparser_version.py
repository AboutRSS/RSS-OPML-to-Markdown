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

def is_fetch_failed(item):
    return item[2] == 'fetch failed'

def is_no_entry(item):
    return item[2] == 'no entry'

def sort_rst(rst):
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
                if 'updated' in feedcontent.feed:
                    last_updated = feedcontent.feed['updated']
                else:
                    if 'published' in feedcontent.entries[0]:
                        last_updated = feedcontent.entries[0]['published']
                    else:
                        last_updated = 'not found'
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
                for key, value in feedcontent.entries[0].links[0].items():
                    if value == "enclosure":
                        is_podcast = True
                        break
                    else:
                        is_podcast = False
                
                for key in feedcontent.entries[0].keys():
                    if key.find("itunes") != -1:
                        is_podcast = is_podcast + True
                        break
                    else:
                        is_podcast = is_podcast + False
                
                if is_podcast == 2:
                    is_podcast = True
                else:
                    is_podcast = False
                
                # velocity = feedcontent[0]['velocity']
                version = feedcontent.version
                # rst.append([feed['title'], feed['url'],last_updated,is_podcast,item_count,content_length,velocity,version])
                rst.append([feed['title'], feed['url'],last_updated,item_count,content_length,language,version,is_podcast])
            else:
                rst.append([feed['title'], feed['url'],'no entry','no entry','no entry','no entry','no entry','no entry'])
        else:
            feedcontent = get_feed_content_using_requests(feed['url'])
            if feedcontent and feedcontent != '{}':
            # print(feedcontent)
                item_count = len(feedcontent['entries'])
                if item_count > 0:
                    if 'updated' in feedcontent.feed:
                        last_updated = feedcontent.feed['updated']
                    else:
                        if 'published' in feedcontent.entries[0]:
                            last_updated = feedcontent.entries[0]['published']
                        else:
                            last_updated = 'not found'
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
                    for key, value in feedcontent.entries[0].links[0].items():
                        if value == "enclosure":
                            is_podcast = True
                            break
                        else:
                            is_podcast = False
                
                    for key in feedcontent.entries[0].keys():
                        if key.find("itunes") != -1:
                            is_podcast = is_podcast + True
                            break
                        else:
                           is_podcast = is_podcast + False
                
                    if is_podcast == 2:
                        is_podcast = True
                    else:
                        is_podcast = False
                
                    # velocity = feedcontent[0]['velocity']
                    version = feedcontent.version
                    # rst.append([feed['title'], feed['url'],last_updated,is_podcast,item_count,content_length,velocity,version])
                    rst.append([feed['title'], feed['url'],last_updated,item_count,content_length,language,version,is_podcast])
                else:
                    rst.append([feed['title'], feed['url'],'no entry','no entry','no entry','no entry','no entry','no entry'])
            else:
                rst.append([feed['title'], feed['url'],'fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed'])
        # print(tabulate.tabulate(rst, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    return rst

def print_to_std(feeds_list):
    # print(tabulate.tabulate(feeds_list, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length (bytes)','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    print(tabulate.tabulate(feeds_list, headers=['Title', 'URL','Last Updated','Item Count','Content Length (bytes)','Language','Detected feed type version','Podcast feed or not'], tablefmt='pipe'))
    # for tag, feed_list in feeds_list.items():
    # for feed_list in feeds_list.items():
        # print("# " + tag + "\n")
        # print(tabulate.tabulate(feed_list, headers=["title", "url"], tablefmt="pipe"))
        # print("\n")


def print_to_file(feeds_list, filename):
    with open(filename, 'wt', encoding="utf-8") as f:
        # f.write(tabulate.tabulate(feeds_list, headers=["Title", "URL","Last Updated","Podcast","Item Count","Content Length (bytes)","The mean number of items per day","Detected feed type version"], tablefmt="pipe"))
        f.write(tabulate.tabulate(feeds_list, headers=["Title", "URL","Last Updated","Item Count","Content Length (bytes)","Language","Detected feed type version","Podcast feed or not"], tablefmt="pipe"))
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
        print_to_std(feeds_list)
    elif len(sys.argv) == 3:
        feeds_list = parse(sys.argv[1])
        feeds_list = sort_rst(feeds_list)
        print_to_file(feeds_list, sys.argv[2])
        print("Finished !")
    else:
        print("Error: argv number doesn't match")
        exit(-1)


if __name__ == "__main__":
    main()