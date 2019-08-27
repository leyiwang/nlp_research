# Spider

> A toolkit for NLP researchers, which used to automatically grab papers' info. 
>
> Research Spider for Anthology **v0.5**

## Introduction

This toolkit can automatically grab the papers information by given keywords in title. 

You can set the search params: *the conference, publication date and the keywords in title* . Then it will automatically save these papers' title, authors, download link, Google Scholar cited number and abstracts information in a 'Excel' format file.

### Usage

- Parameters and Setting:

  Config parameters in the script research_spider.py

  |   Parameters   |                 Setting                  |       Description       |
  | :------------: | :--------------------------------------: | :---------------------: |
  | published year |           years = (2013, 2016)           | years from 2013 to 2016 |
  |    keywords    | keywords = ['lexicon', 'dictionary', 'lexical'] |        keywords         |
  |  conferences   | events = ['ACL', 'CL', 'COLING', 'EACL', 'EMNLP', 'LREC', 'NAACL'] |       conferences       |

- configure file
  You can config the spider mode and google scholar website url in the configure file `conf/conf.ini`.
  - This toolkit support two mode, `selenium` and `requests`, and default mode is selenium.
  - We can not access Google Scholar website in China, so i use a mirror website.
  
 The `selenium` mode is recommended for use. Please download `chromedriver` and install the chrome browser to use the `selenium` mode. You can download the `chromedriver` from [mirror website](http://npm.taobao.org/mirrors/chromedriver/). Make sure your `chromedriver` version is consistent with your chrome browser.
 ```angular2
 ChromeDriver 76.0.3809.12 (2019-06-07)---------Supports Chrome version 76
 ChromeDriver 75.0.3770.8 (2019-04-29)---------Supports Chrome version 75
 ```

- Usage

  ```shell
  python3 research_spider.py
  ```

## Contibutor

Author: wang leyi

Email: leyiwang.cn@gmail.com

Blog:https://leyiwang.github.io/

## Change History
Date: Last update 2019-08-22 Description:
 1. Refactor code to adapt changes of Anthology
 2. Add the `selenium` mode to accelerate the efficiency and improving the stability of spider

Date: Update 2019-04-16 Description: Refactor code to adapt to Anthology site style changes

Date: Update 2017-05-02 Description: Fix the invalid bug for the second bit of 0 for the year.

Data: Update 2016-12-22

Date: Update 2016-11-5
