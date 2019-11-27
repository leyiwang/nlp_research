#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  anthology spider
  Author: wangleyi
  Email: leyiwang.cn@gmail.com
  File:  anthology_spider.py
  Date: 2019-04-16 15:32
"""
import itertools
import logging
import re

import requests
from lxml import etree
from tqdm import tqdm

from nlp_research.scholar_spider import ScholarSpider
from nlp_research.scholar_spider import SeleniumScholarSpider
from utils.common import Utils
from utils.log import logger


class AnthologySpider(object):
    """
    antholgy website spider
    """
    TOTAL_EVENTS = {'ACL', 'CL', 'COLING', 'EACL', 'EMNLP', 'LREC', 'NAACL', 'SemEval', 'IJCNLP'}

    def __init__(self, keywords, years, events=None):
        """
        init
        :param keywords: list, keywords
        :param years: tuple, starting and ending year information
        :param events: list, list of event name
        """
        self.base_url = 'https://www.aclweb.org/anthology/events/'
        self.anthology_xpath_dict = {
            "papers_nodes": "//section/div/p[position()>1]",
            "paper_name_node": "span/strong/a[@class='align-middle']",
            "author_node": "span[2]/a/text()",
            "links_node": "span[1]/a[starts-with(text(),'pdf')]/@href"
        }
        mode = Utils.CONFIG["scholar"].get("mode")
        if mode == "selenium":
            self.scholar_spider = SeleniumScholarSpider()
        else:
            self.scholar_spider = ScholarSpider()

        self.keywords_pattern = re.compile("|".join(keywords), re.IGNORECASE)
        self.seeds_list = self.make_seeds_list(events, years)

    def make_seeds_list(self, events, years):
        """
        make seeds
        :param events:  list, list of event name
        :param years: tuple, starting and ending year information
        :return:
        """
        invalid_events = None
        if events is None:
            valid_envent = self.TOTAL_EVENTS
        else:
            invalid_events = list(filter(lambda x: x.upper() not in self.TOTAL_EVENTS, events))
            valid_envent = filter(lambda x: x.upper() in self.TOTAL_EVENTS, events)

        if invalid_events:
            logging.error("invalid event: {}".format(invalid_events))
        valid_event_info = list(itertools.product(valid_envent, range(years[0], years[1])))
        seeds_list = map(lambda x: "{}-{}".format(x[0].lower(), x[1]), valid_event_info)
        return seeds_list

    def response_parser(self, response):
        """
        parse response
        :param response: http response
        :return: list,
        """
        html = response.text
        selector = etree.HTML(html)
        papers_nodes = selector.xpath(self.anthology_xpath_dict["papers_nodes"])
        papers = map(lambda x: x.xpath(self.anthology_xpath_dict["paper_name_node"])[0].xpath("string(.)"),
                     papers_nodes)
        authors = map(lambda x: "; ".join(x.xpath(self.anthology_xpath_dict["author_node"])),
                      papers_nodes)
        links = map(lambda x: x.xpath(self.anthology_xpath_dict["links_node"])[0],
                    papers_nodes)
        papers_list = filter(lambda x: self.keywords_pattern.findall(x[0]),
                             zip(papers, authors, links))
        papers_info_list = list(map(lambda x: list(x), papers_list))
        return papers_info_list

    def get_response(self, url, headers):
        """
        get a http response
        :param url: str, url to visited
        :param headers: headers of http request
        :return:
        """
        try:
            logging.disable(logging.ERROR)
            response = requests.get(url=url, headers=headers)
            response.encoding = response.apparent_encoding
        except Exception as err:
            logging.error(err)
            response = None
        finally:
            logging.disable(logging.NOTSET)
        return response

    def _research(self):
        final_result = []
        for seeds in self.seeds_list:
            headers = {
                'User-Agent': "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us)"
                              " AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
            url = "{}{}".format(self.base_url, seeds)

            conf_name, year = seeds.split('-')
            logger.info('Start to get papers list from {}'.format(seeds))
            response = self.get_response(url, headers=headers)
            papers_list = self.response_parser(response)
            for i in tqdm(range(len(papers_list)), desc="Processing"):
                item = papers_list[i]
                abstract, cite_num = self.scholar_spider.get_reference(item[0])
                item.extend([conf_name, year, cite_num, abstract])
            final_result.extend(papers_list)
            logger.info('The list of {} has been crawled.'.format(seeds))

        return final_result

    def run(self, save_dir="."):
        final_result = self._research()
        header = ['Title', 'Author', 'Download_link', 'From', 'Year', 'Cited Num', 'Abstract']
        fname = 'papers_{}.xlsx'.format(Utils.get_current_date())
        Utils.xlsx_writer(save_dir, fname, final_result, header)
