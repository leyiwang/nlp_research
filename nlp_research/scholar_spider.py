#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   google scholar spider
  Author: wangleyi
  Email: leyiwang.cn@gmail.com
  File:  scholar_spider.py
  Date: 2019-04-16 15:30
"""
import heapq
import logging
import random
import re
import time

import requests
from lxml import etree

from utils.common import UA
from utils.log import logger


class ScholarSpider(object):
    """
    Spider base class
    """

    def __init__(self):
        """init"""
        self.scholar_url = "https://x.zhoupen.cn"
        self.scholar_xpath_dict = {
            "paper_nodes": "//div[@id='gs_res_ccl_mid']/div/div[@class='gs_ri']",
            "paper_name_nodes": "h3/a",
            "abstract_node": "div[@class='gs_rs']",
            "ref_node": "div[@class='gs_fl']/a[starts-with(text(), '被引用次数：')]/text()",
        }

    @staticmethod
    def is_valid(paper_name, title):
        pattern = "[\\dA-Za-z\u4e00-\u9fa5]+"
        paper_name = " ".join(re.findall(pattern, paper_name))
        title = " ".join(re.findall(pattern, title))
        if re.findall(re.escape(title), paper_name, re.IGNORECASE):
            return True
        else:
            return False

    def response_parser(self, response, title):
        paper_info_list = []
        if response is None:
            return [""] * 2
        html = response.text
        selector = etree.HTML(html)

        paper_nodes = selector.xpath(self.scholar_xpath_dict["paper_nodes"])
        for node in paper_nodes:
            try:
                paper_name_nodes = node.xpath(self.scholar_xpath_dict["paper_name_nodes"])
                if not paper_name_nodes:
                    continue
                paper_name = paper_name_nodes[0].xpath("string(.)")
                if not self.is_valid(paper_name, title):
                    continue
                abstract_node = node.xpath(self.scholar_xpath_dict["abstract_node"])
                abstract = abstract_node[0].xpath("string(.)") if abstract_node else ""

                ref_node = node.xpath(self.scholar_xpath_dict["ref_node"])
                ref_num = re.findall("\\d+$", ref_node[0])[0] if ref_node else "0"

                paper_info = [abstract, ref_num]
                paper_info_list.append(paper_info)
            except Exception as err:
                logger.error(err)
        if paper_info_list:
            final_paper_info = heapq.nlargest(1, paper_info_list, key=lambda x: int(x[1]))[0]
        else:
            final_paper_info = [""] * 2
        return final_paper_info

    def get_response(self, url, headers):
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

    def get_reference(self, title):
        headers = {'User-Agent': UA.random}
        time.sleep(random.randint(9, 12))
        title = title
        search_keywords = '+'.join(title.split())
        url = '{}/scholar?q={}&hl=zh-CN'.format(self.scholar_url, search_keywords)
        response = self.get_response(url, headers)
        paper_info = self.response_parser(response, title)
        return paper_info
