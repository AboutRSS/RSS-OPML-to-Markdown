# RSS-OPML-to-Markdown

- [ReadMe of this forked repo](#readme-of-this-forked-repo)
- [ReadMe of the original repo](#readme-of-the-origional-repo)

---

## ReadMe of this forked repo

### Intro

Turn OPML into a Markdown table with key infomation of RSS feeds such as publish frequency etc.

### Pro and Con

| Functions or known issues | rss_opml_to_markdown_Feedsearch_version.py | rss_opml_to_markdown_feedparser_version.py | 
|------------:|:----------:|:-------------|
|Sequence Number (to tell how many feeds in the OPML)|❌ | ✅ |
|Feed Title | ✅ | ✅ |
|Detect Site URL from RSS feed URL | ❌ | ✅ but might not be correct due to that some feeds put other link address rather than site url in the namespace of `link` |
|Feed URL | ✅ | ✅ |
|If the outermost level of `outline` signifies the Feed Category, extract it|   ❌ | ✅ |
|Works with OPML with more than 2 levels of `outline` | ❌ | ❌ |
|Show the time of Last Updated | ✅ | ✅ |
|Humanize the time difference between last updated and now | ❌ | ✅ |
|Show Item Count| ✅ | ✅ |
|Show Content Length (bytes of the RSS xml file) | ✅ | ✅ |
|Show the mean number of items per day (or be interpreted as publish frequency)| ✅ | ✅ |
|Show Language if RSS feed has language namespace| ❌ | ✅ |
|Show feed type version | ✅  | ✅ |
|Tell whether it's a Podcast feed| ✅ | ✅ Simple detection according to `enclosure` and `itunes`-related namespace |
|Able to handle OPML with huge amount of RSS Feeds| ❌ due to API limitation | ✅ |
| SSLError Problem like `EOF occurred in violation of protocol` or `SSL: CERTIFICATE_VERIFY_FAILED` | Seldom | Partially resolved as `requests.Session()` has been involved. It seems still [an open issue](https://github.com/kurtmckee/feedparser/issues/84) for `feedparser` |
| Put those 'Fetch failed' RSS Feeds together at the bottom of the generated Markdown table | ❌ | ✅ |

### Usage

```python rss_opml_to_markdown_Feedsearch_version.py {The name and path of the OPML file} {the name and path of the outputed .MD file}```

Or

```python rss_opml_to_markdown_feedparser_version.py {The name and path of the OPML file} {the name and path of the outputed .MD file}```

### Bonus

[*opml_merge.py*](/RSS_OPML_to_Markdown/opml_merge.py): merge all OPML files (that has no more than 2 levels of `outline` fields) in a certain folder into one OPML file.

Usage: ```python opml_mergy.py {The path of the folder containing OPML files} {the name and the path of the outputed OPML file or the path of the folder for the outputed file}```

### Demo 

OPML content:

```
<opml version="2.0">
  <head>
    <title>My Subscriptions</title>
  </head>
  <body>
    <outline title="News" type="rss">
      <outline title="BBC News" type="rss" xmlUrl="https://feeds.bbci.co.uk/news/rss.xml"/>
    </outline>
    <outline title="Tech" type="rss">
      <outline title="The Verge" type="rss" xmlUrl="https://www.theverge.com/rss/index.xml"/>
    </outline>
  </body>
</opml>
```

> P.S. [the above sample OPML file is provided by Google Bard](https://g.co/bard/share/f2a0db3b818e).

### If using [rss_opml_to_markdown_Feedsearch_version.py](/RSS_OPML_to_Markdown/rss_opml_to_markdown_Feedsearch_version.py)

[OPML](/sample_provided.opml) -> [Markdown](/sample_Feedsearch_version.md)

Markdown preview:

| Title     | URL                                    | Last Updated              | Podcast   |   Item Count |   Content Length |   The mean number of items per day | Detected feed type version   |
|:----------|:---------------------------------------|:--------------------------|:----------|-------------:|-----------------:|-----------------------------------:|:-----------------------------|
| BBC News  | https://feeds.bbci.co.uk/news/rss.xml  | 2023-10-17T15:01:41+00:00 | False     |           94 |            52924 |                              0.459 | rss20                        |
| The Verge | https://www.theverge.com/rss/index.xml | 2023-10-17T15:00:00+00:00 | False     |           10 |            23496 |                             96.583 | atom10                       |

### If using [rss_opml_to_markdown_feedparser_version.py](/RSS_OPML_to_Markdown/rss_opml_to_markdown_feedparser_version.py)

Markdown preview:

|   Sequence Number | Title          | Site URL                            | Feed URL                                   | Category   | Last Updated           | Item Count   | Content Length (bytes)   | The mean number of items per day   | Language     | Detected feed type version   | Podcast feed or not   |
|------------------:|:---------------|:------------------------------------|:-------------------------------------------|:-----------|:-----------------------|:-------------|:-------------------------|:-----------------------------------|:-------------|:-----------------------------|:----------------------|
|                 1 | 小众软件           | https://www.appinn.com              | https://feed.appinn.com/                   | 网络资源🥗      | 14h6m ago              | 10           | 123248                   | 2.63                               | zh-CN        | rss20                        | False                 |
|                 2 | 异次元软件世界        | https://www.iplaysoft.com           | http://feed.iplaysoft.com/                 | 网络资源🥗      | 1d11h ago              | 60           | 483834                   | 0.75                               | zh-CN        | rss20                        | False                 |
|                 3 | 電腦玩物           | http://www.playpcesor.com/          | http://feeds.feedburner.com/playpc         | 网络资源🥗      | 4d9h ago               | 15           | 1201013                  | 0.40                               | not found    | atom10                       | False                 |
|                 4 | 免費資源網路社群       | https://free.com.tw                 | http://feeds.feedburner.com/freegroup      | 网络资源🥗      | 19h14m ago             | 10           | 151280                   | 1.11                               | zh-TW        | rss20                        | False                 |
|                 5 | 反斗软件 » 反斗软件    | https://www.apprcn.com              | http://www.apprcn.com/feed                 | 网络资源🥗      | 2023 August 07, 15:59  | 10           | 53380                    | 0.08                               | zh-CN        | rss20                        | False                 |
|                 6 | 少数派            | https://sspai.com                   | https://sspai.com/feed                     | 网络资源🥗      | 11h10m ago             | 10           | 22283                    | 9.51                               | zh-CN        | rss20                        | False                 |
|                 7 | 编程随想           | https://program-think.blogspot.com/ | https://feeds2.feedburner.com/programthink | 网络资源🥗      | 2021 May 09, 15:43     | 5            | 1788545                  | 0.10                               | not found    | atom10                       | False                 |
|                 8 | Rat's Blog     | https://www.moerats.com/            | https://www.moerats.com/feed               | 网络资源🥗      | 2022 January 22, 15:04 | 10           | 140622                   | 0.01                               | zh-CN        | rss20                        | False                 |
|                 9 | 如有乐享           | https://51.ruyo.net                 | https://51.ruyo.net/feed/                  | 网络资源🥗      | 20h34m ago             | 10           | 125712                   | 0.42                               | zh-CN        | rss20                        | False                 |
|                10 | 活动优惠           | https://jike.info/category/5        | https://jike.info/category/5.rss           | 网络资源🥗      | 8h8m ago               | 25           | 45493                    | 10.33                              | not found    | rss20                        | False                 |
|                11 | 神代綺凜の萌化小基地     | https://moe.best/                   | https://moe.best/feed                      | 网络资源🥗      | 2023 July 17, 08:57    | 10           | 20053                    | 0.01                               | zh-CN        | rss20                        | False                 |
|                12 | 不死鸟            | https://iui.su/                     | https://hao.su/feed/                       | 网络资源🥗      | 1d5h ago               | 20           | 177629                   | 0.90                               | zh-CN        | rss20                        | False                 |
|                13 | Anyway.FM 设计杂谈 | https://anyway.fm                   | http://anyway.fm/rss.xml                   | 网络资源🥗      | 2023 October 23, 18:21 | 177          | 1855842                  | 0.06                               | zh-CN        | rss20                        | True                  |
|                14 | 老殁 - 殁漂遥       | https://www.mpyit.com               | https://www.mpyit.com/feed                 | 网络资源🥗      | 16h5m ago              | 10           | 23891                    | 33.52                              | zh-CN        | rss20                        | False                 |
|                15 | Windows软件破解    | fetch failed                        | https://downloadly.ir/feed/                | 网络资源🥗      | fetch failed           | fetch failed | fetch failed             | fetch failed                       | fetch failed | fetch failed                 | fetch failed          |
|                16 | Saodaye        | fetch failed                        | https://saodaye.com/feed                   | 网络资源🥗      | fetch failed           | fetch failed | fetch failed             | fetch failed                       | fetch failed | fetch failed                 | fetch failed          |         |

### Motivation

When I'm interested in a new found RSS feed, I'd like to know more about it. For example, a property or index indicates how often a certain RSS feed is publishing its new items would be much better for me to determine subscribing to it or not. Thus, I first combined [RSS-OPML-to-Markdown](https://github.com/idealclover/RSS-OPML-to-Markdown) with [Feedsearch API](https://feedsearch.dev/). Now, by utilizing the power of [Feedsearch API](https://feedsearch.dev/), one can easily type ```python rss_opml_to_markdown_Feedsearch_version.py {The name and path of the OPML file} {the name and path of the outputed .MD file}``` to obtain 'Title', 'URL','Last Updated','Is Podcast','Item Count','Content Length','The mean number of items per day' and 'Detected feed type version' of a certain RSS feed listed in the OPML file. Notice that one might encounter the API usage limitation if there are more than 10 feeds contained in the OPML file.

In order to bypass the limitation of Feedsearch API, another approach utilizing [feedparser](https://github.com/kurtmckee/feedparser) has been developed. Hence, it does not matter if there are a plenty of RSS feeds in an OPML file.

### Acknowledgement

Inspired by 

- [RSS-OPML-to-Markdown](https://github.com/idealclover/RSS-OPML-to-Markdown) by @idealclover
- [Feedsearch API](https://feedsearch.dev/)
- [feedparser](https://github.com/kurtmckee/feedparser)
- [opyml](https://pypi.org/project/opyml/)

---

## Readme of the origional repo

> 🎁 Please take my RSS list!

RSS-OPML-to-Markdown 可以将从平台导出的 OPML 文件转化为易读的 Markdown 表格的形式，便于分享与展示

目前已在 [inoreader](https://www.inoreader.com) 与 [tiny tiny RSS](https://tt-rss.org/) 上进行测试

### Demo

转换前 [OPML](/sample.opml) -> 转换后 [Markdown](/sample.md)

### How to Use

本项目基于 Python3 构建，依赖包 [listparser](https://pypi.org/project/listparser/) 与 [tabulate](https://pypi.org/project/tabulate/)

### 使用pip安装

1. 下载项目

```
pip install RSS-OPML-to-Markdown
```

2. 使用项目

```
rss_opml_to_markdown {OPML文件的位置与名称} {期望输出markdown文件的位置与名称}
```

> 注：后一参数为空则输出结果到控制台

### Planned Features

- [ ] 表格源代码美化

- [ ] 更多选项支持

### Contribute

如果有任何想法或需求，可以在 [issue](https://github.com/idealclover/RSS-OPML-to-Markdown/issues) 中告诉我们，同时欢迎各种 pull requests

### Open-source Licenses

This project is under MIT license, feel free to use it under the license.