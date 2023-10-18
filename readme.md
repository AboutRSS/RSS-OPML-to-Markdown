# RSS-OPML-to-Markdown

- [ReadMe of this forked repo](#readme-of-this-forked-repo)
- [ReadMe of the original repo](#readme-of-the-origional-repo)

## ReadMe of this forked repo

When I'm interested in a new found RSS feed, I'd like to know more about it. For example, a property or index indicates how often a certain RSS feed is publishing its new items would be much better for me to determine subscribing to it or not. Thus, I first combined [RSS-OPML-to-Markdown](https://github.com/idealclover/RSS-OPML-to-Markdown) with [Feedsearch API](https://feedsearch.dev/). Now, by utilizing the power of [Feedsearch API](https://feedsearch.dev/), one can easily type ```python rss_opml_to_markdown_Feedsearch_version.py {The name and path of the OPML file} {the name and path of the outputed .MD file}``` to obtain 'Title', 'URL','Last Updated','Is Podcast','Item Count','Content Length','The mean number of items per day' and 'Detected feed type version' of a certain RSS feed listed in the OPML file. Notice that one might encounter the API usage limitation if there are more than 10 feeds contained in the OPML file.

In order to bypass the limitation of Feedsearch API, another approach utilizing [feedparser](https://github.com/kurtmckee/feedparser) has been developed. Hence, it does not matter if there are a plenty of RSS feeds in an OPML file.

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

- If using [rss_opml_to_markdown_Feedsearch_version.py](/RSS_OPML_to_Markdown/rss_opml_to_markdown_Feedsearch_version.py)

[OPML](/sample_provided.opml) -> [Markdown](/sample_Feedsearch_version.md)

Markdown preview:

| Title     | URL                                    | Last Updated              | Podcast   |   Item Count |   Content Length |   The mean number of items per day | Detected feed type version   |
|:----------|:---------------------------------------|:--------------------------|:----------|-------------:|-----------------:|-----------------------------------:|:-----------------------------|
| BBC News  | https://feeds.bbci.co.uk/news/rss.xml  | 2023-10-17T15:01:41+00:00 | False     |           94 |            52924 |                              0.459 | rss20                        |
| The Verge | https://www.theverge.com/rss/index.xml | 2023-10-17T15:00:00+00:00 | False     |           10 |            23496 |                             96.583 | atom10                       |

- If using [rss_opml_to_markdown_feedparser_version.py](/RSS_OPML_to_Markdown/rss_opml_to_markdown_feedparser_version.py)

[OPML](/sample_provided.opml) -> [Markdown](/sample_feedparser_version.md)

Markdown preview:

| Title     | URL                                    | Last Updated                  |   Item Count |   Content Length (bytes) | Language   | Detected feed type version   |
|:----------|:---------------------------------------|:------------------------------|-------------:|-------------------------:|:-----------|:-----------------------------|
| BBC News  | https://feeds.bbci.co.uk/news/rss.xml  | Wed, 18 Oct 2023 14:48:36 GMT |           79 |                     9169 | en-gb      | rss20                        |
| The Verge | https://www.theverge.com/rss/index.xml | 2023-10-18T10:16:16-04:00     |           10 |                     7429 | en         | atom10                       |

### Acknowledgement

Inspired by 

- [RSS-OPML-to-Markdown](https://github.com/idealclover/RSS-OPML-to-Markdown)
- [Feedsearch API](https://feedsearch.dev/)
- [feedparser](https://github.com/kurtmckee/feedparser)

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