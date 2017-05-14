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

