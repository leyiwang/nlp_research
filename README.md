# Spider

> A toolkit for NLP researchers, which used to automatically grab papers' info. 
>
> Research Spider for Anthology **v0.5**

## Introduction

This toolkit can automatically grab the papers information by given keywords in title. 

You can set the search params: *the conference, publication date and the keywords in title* . Then it will automatically save these papers' title, authors, download link, Google Scholar cited number and abstracts information in a Excel file.

### Usage

- Parameters and Setting:

  Config parameters in the script Research_Spider.py

  |   Parameters   |                 Setting                  |       Description       |
  | :------------: | :--------------------------------------: | :---------------------: |
  | published year |             years = (13,16)              | years from 2013 to 2016 |
  |    keywords    | keywords = ['lexicon', 'dictionary', 'lexical'] |        keywords         |
  |  conferences   | events = ['ACL', 'CL', 'COLING', 'EACL', 'EMNLP', 'LREC', 'NAACL'] |       conferences       |


- Usage

  ```shell
  python Research_Spider.py
  ```

## Contibutor

Louie Wang

Email: leyiwang.cn@gmail.com(or wangleyi123@yeah.net)

Blog:https://leyiwang.github.io/

## Change History

Date: Last update 2016-12-22

Date: Update 2016-11-5




