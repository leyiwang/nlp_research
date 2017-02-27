#coding=utf8
'''
  Title: Research Spider for Anthology
  Version: V0.5
  Author: Leyi Wang
  Date: Last update 2016-12-22
  Email: leyiwang.cn@gmail.com
'''
import pandas as pd 
import urllib2, re, datetime
import logging, time, random
from cookielib import CookieJar

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level = logging.DEBUG)
class Spider(object):
    def __init__(self, keywords):
        self.cookie_jar = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}        
        self.header = ['Title', 'Author', 'Download_link', 'From', 'Year', 'Cited Num', 'Abstract']
        self.keywords = keywords

    def get_reference(self, title):
        '''
        get abstract, reference num from google of a paper
        '''
        res = ['','']
        try:
            time.sleep(random.randint(9, 12))
            title = title.lower()
            key_words = '+'.join(title.split())
            url = 'https://xueshu.glgoo.com/scholar?q=' + key_words + '&hl=zh-CN'
            req = urllib2.Request(url=url, headers = self.headers)
            html = self.opener.open(req).read().lower()
            abs_rgx = '<h3 class="gs_rt">.*?' + title + '\.{0,}</a></h3>.*?<div class="gs_rs">(.*)?</div><div class="gs_fl">'
            cited_rgx = '<h3 class="gs_rt">.*?' + title + '.*?<div class="gs_rs">.*?</div><div class="gs_fl"><a .*?>被引用次数：(\d{0,})</a>'
            abs_patten, cited_patten = re.compile(abs_rgx, re.S), re.compile(cited_rgx, re.S)
            abst, cited = abs_patten.findall(html), cited_patten.findall(html)
            if len(abst)!=0:
                res[0] = re.sub('<br>|</br>', '', abst[0].strip())
            if len(cited)!=0:
                res[1] = cited[0]
        except Exception, msg:
            logging.error(msg)
        finally:
            return res

class AnthologySpider(Spider):
    def __init__(self, keywords, years, events=None):
        Spider.__init__(self, keywords)
        self.base_url = r'https://www.aclweb.org/anthology/'
        self.conf_dic = {'ACL':'P','CL':'J', 'COLING':'C', 'EACL':'E', 'EMNLP':'D', 'LREC':'L', 'NAACL':'N'}
        if events==None:
            events = self.conf_dic.keys()
        self.seeds = [map(lambda x: '/'.join([self.conf_dic[conf]]*2) + str(x), range(years[0], years[1]+1)) for conf in events if conf in self.conf_dic.keys()]

    def __research(self):
        final_result = []
        self.id_conf_dic = {value: key for key,value in self.conf_dic.iteritems()}
        for seeds in self.seeds:
            for seed in seeds:
                url = self.base_url + seed
                conf_id = seed.split('/')[0]
                conf_name, year = self.id_conf_dic[seed.split('/')[0]], '20' + seed.strip(conf_id + '/' + conf_id)
                request = urllib2.Request(url)
                logging.info('Start to get papers list from ' + conf_name + year)
                try:
                    html = urllib2.urlopen(request).read()
                    cand_paper_list = self.patten.findall(html)
                    papers_list = [list(item[::-1]) for item in cand_paper_list if self.keywords_patten.findall(item[-1].lower())]#title author link 
                    for i, item in enumerate(papers_list):
                        if i+1 < len(papers_list):
                            print '%d%% |'%((i+1)*100/len(papers_list)),'#'*((i+1)*60/len(papers_list)),'\r',
                        else:
                            print '%d%% |'%((i+1)*100/len(papers_list)),'#'*((i+1)*60/len(papers_list)),'|\r\n',
                        item[-1] = url + r'/' + item[-1]
                        item[1] = re.sub('<first>|</first>|<last>|</last>', '', ' '.join(item[1].split()))
                        abstract, cite_num = self.get_reference(item[0])
                        item.extend([conf_name, year, cite_num, abstract])
                    final_result.extend(papers_list)
                    logging.info('The list of ' + conf_name + year + ' has been crawled.')
                except Exception, msg:
                    logging.error(msg)
        xlsx_writer('papers_' + get_current_date() + '.xlsx', final_result, self.header)

    def run(self):
        self.keywords_patten =re.compile('|'.join(self.keywords))
        self.patten = re.compile(r'([A-Z]\d{2}-\d{4}\.pdf).*?<b>(.*)?</b><br><i>(.*)?</i>')#link author title
        self.__research()

class DblpSpider(Spider):
    pass

def xlsx_writer(filename, data, header=None):
    df = pd.DataFrame(data=data, dtype=str)
    df.to_excel(filename, float_format=None, header=header, index=False)

def get_current_date():
    return datetime.datetime.now().strftime('%Y%m%d')

def start_demo(keywords, years, events):
    start_time = datetime.datetime.now()
    acl_spider = AnthologySpider(keywords, years, events)
    acl_spider.run()
    end_time = datetime.datetime.now()
    logging.info("\nDone! Seconds cost:"+str((end_time - start_time).seconds))
    
if __name__ == '__main__':
    years=(13,16)
    keywords = ['lexicon', 'dictionary', 'lexical']
    #keywords = ['sentence','word','embedding','representation']
    events = ['ACL', 'CL', 'COLING', 'EACL', 'EMNLP', 'LREC', 'NAACL']
    start_demo(keywords, years, events)
