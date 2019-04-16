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


- Usage

  ```shell
  python3 research_spider.py
  ```

## Contibutor

Author: wang leyi

Email: leyiwang.cn@gmail.com

Blog:https://leyiwang.github.io/

## Change History

Date: Last update 2019-04-16 Description: Refactor code to adapt to Anthology site style changes

Date: Last update 2017-05-02 Description: Fix the invalid bug for the second bit of 0 for the year.

Data:Update 2016-12-22

Date: Update 2016-11-5
