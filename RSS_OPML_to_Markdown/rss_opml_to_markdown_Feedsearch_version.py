# -*- coding: UTF-8 -*-
import listparser
import tabulate
import requests
import sys

# if feeds are no more than 10, this .py works fine. This is due to API limitation of FeedSearch.Dev.
name = "rss-opml-to-markdown"

def get_feed_metadata(feed_url):
  response = requests.get(feed_url)
  if response.status_code == 200:
    return response.json()
  else:
    return None

def parse(file_name):
    # result = listparser.parse(file_name)
    # result = listparser.parse(open(file_name).read())
    with open(file_name, encoding='utf-8') as f:
        result = listparser.parse(f.read())
    rst = []
    for feed in result['feeds']:
        api_url = 'https://feedsearch.dev/api/v1/search?url=' + feed['url']
        metadata = get_feed_metadata(api_url)
        if metadata and metadata != '{}':
            # print(metadata)
            last_updated = metadata[0]['last_updated']
            content_length = metadata[0]['content_length']
            is_podcast = metadata[0]['is_podcast']
            item_count = metadata[0]['item_count']
            velocity = metadata[0]['velocity']
            version = metadata[0]['version']
            rst.append([feed['title'], feed['url'],last_updated,is_podcast,item_count,content_length,velocity,version])
        else:
            rst.append([feed['title'], feed['url'],'fetch failed','fetch failed','fetch failed','fetch failed','fetch failed','fetch failed'])
        # print(tabulate.tabulate(rst, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    return rst

def print_to_std(feeds_list):
    print(tabulate.tabulate(feeds_list, headers=['Title', 'URL','Last Updated','Podcast','Item Count','Content Length','The mean number of items per day','Detected feed type version'], tablefmt='pipe'))
    # for tag, feed_list in feeds_list.items():
    # for feed_list in feeds_list.items():
        # print("# " + tag + "\n")
        # print(tabulate.tabulate(feed_list, headers=["title", "url"], tablefmt="pipe"))
        # print("\n")


def print_to_file(feeds_list, filename):
    with open(filename, 'wt', encoding="utf-8") as f:
        f.write(tabulate.tabulate(feeds_list, headers=["Title", "URL","Last Updated","Podcast","Item Count","Content Length","The mean number of items per day","Detected feed type version"], tablefmt="pipe"))
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
        print_to_std(feeds_list)
    elif len(sys.argv) == 3:
        feeds_list = parse(sys.argv[1])
        print_to_file(feeds_list, sys.argv[2])
    else:
        print("Error: argv number doesn't match")
        exit(-1)


if __name__ == "__main__":
    main()