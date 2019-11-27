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
import re
import time
import requests
from lxml import etree
from selenium import webdriver

from utils.common import Utils
from utils.log import logger


class ScholarSpider(object):
    """
    Spider base class
    """

    def __init__(self, interval=9):
        """init"""
        self.scholar_url = Utils.CONFIG["scholar"].get("google_scholar")
        self.scholar_xpath_dict = {
            "paper_nodes": "//div[@id='gs_res_ccl_mid']/div/div[@class='gs_ri']",
            "paper_name_nodes": "h3/a",
            "abstract_node": "div[@class='gs_rs']",
            "ref_node": "div[@class='gs_fl']/a[starts-with(text(), '被引用次数：')]/text()",
        }
        self.interval = interval

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
        if response.status_code != 200:
            logger.warning("code: {}, google scholar website is forbidden!"
                           "".format(response.status_code))
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
            print(response.status_code)
            response.encoding = response.apparent_encoding
        except Exception as err:
            logging.disable(logging.NOTSET)
            logging.error(err)
            response = None
        finally:
            logging.disable(logging.NOTSET)
        return response

    def get_reference(self, title):
        headers = {'User-Agent': Utils.UA.random,
                   "Pragma": "no-cache",
                   'DNT': '1',
                   'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0'}
        time.sleep(self.interval)
        search_keywords = '+'.join(title.split())
        url = '{}/scholar?q={}&hl=zh-CN'.format(self.scholar_url, search_keywords)
        response = self.get_response(url, headers)
        paper_info = self.response_parser(response, title)
        return paper_info


class SeleniumScholarSpider(ScholarSpider):
    def __init__(self, interval=3):
        ScholarSpider.__init__(self)
        self.driver = self.init_webdriver()
        self.interval = interval

    @staticmethod
    def init_webdriver():
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;" \
                     " rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("lang=zh_CN.UTF-8")
        options.add_argument("user-agent={}".format(user_agent))
        options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=options)
        # driver.maximize_window()
        # current=driver.window_handles[0]
        driver.set_page_load_timeout(16)
        return driver

    def get_response(self, url):
        try:
            logging.disable(logging.ERROR)
            response = requests.Response()
            self.driver.get(url)
            response.url = url
            response._content = self.driver.page_source.encode()
            response.status_code = 200
        except Exception as err:
            logging.disable(logging.NOTSET)
            logging.error(err)
            response = None
        finally:
            logging.disable(logging.NOTSET)
        return response

    def get_reference(self, title):
        search_keywords = '+'.join(title.split())
        url = '{}/scholar?q={}&hl=zh-CN'.format(self.scholar_url, search_keywords)
        response = self.get_response(url)
        paper_info = self.response_parser(response, title)
        return paper_info
