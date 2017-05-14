# rss-miner

This project aims to be a collection of tools for taking content from RSS feeds and converting it
to Full Facts haystack format. 

### Authors

* cmusselle

## Status 

Early alpha software, development work in progress.

## Installation

1.  Download repository and navigate to its root directory
2.  Install dependencies with `pip install -r package/requirements.txt`
3.  Install library with `pip install package`

## Quick Start

This tool takes as input a file that specifies the RSS feed urls and other configuration options. To
generate an example of one, run. 

    rss-miner -g

This will create a `example_config.yml` in the current directory. Edit this to include/exclude feeds
and set the options (see more below)

You can then run the application with:

    rss-miner -c example_config.yml

## Features

Key features provided by this library

* A CLI application to download the content from multiple feeds and convert them to Full Facts haystack format
* Caching of the feed metadata so that re-running the application only processes new feeds. 
* Storage of all entry data in a local light weight document database. 

## Details

The format of the configuration YAML file has two top level sections: `config` and `feeds`.

Each feed to fetch is specified in the `feeds` section with a unique name, and which contains values
for a `url`, and optionally,  a `content-tag`. e.g. this is the entry for the bbc and guardian politics feed. 

```
feeds:
    bbc-politics:
        url: http://feeds.bbci.co.uk/news/politics/rss.xml
        content-tag: div.story-body__inner
    the-guardian-politics:
        url: https://www.theguardian.com/politics/rss
        content-tag: div.content__main
```

The `content-tag` takes the form of a [CSS selector](https://www.w3schools.com/cssref/css_selectors.asp), 
and is used to lookup the HTML element that contains the body of the article. Every 
paragraph tag that occurs within this element is then processed into sentences and stored in the 
haystack output. The `content-tag` should be as specific as possible if known to avoid including paragraph tags 
not related to the main article (e.g. headers/footers/side menus)

If the `content-tag` is omitted, or does match any tags in the article, the code will try to infer 
the main tag by doing the following:
1. Finding the tag that contains the title of the article from the feed, 
2.  Using its immediate parent as the main article tag.


