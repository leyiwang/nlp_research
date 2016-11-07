#coding=utf8
'''
  Title: Research Spider for Anthology
  Version: V0.3
  Author: Leyi Wang
  Date: Last update 2016-11-5
'''

import logging, time, random
import urllib2, urllib
import re, csv, datetime
from cookielib import CookieJar

cookie_jar = CookieJar()
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level = logging.DEBUG)
class Spider():
    def __init__(self, base_url, seeds, event, keywords):
        self.base_url = base_url
        self.seeds = seeds
        self.conf_name = event[0]
        self.conf_id = event[1]
        self.keywords = keywords

    def research(self):
        keywords_patten =re.compile('|'.join(keywords)) 
        patten = re.compile(r'([A-Z]\d{2}-\d{4}\.pdf).*?<b>(.*)?</b><br><i>(.*)?</i>')
        for seed in self.seeds:
            url = self.base_url + seed
            request = urllib2.Request(url)
            try:
                html = urllib2.urlopen(request, timeout = 10).read()
                cand_paper_list = patten.findall(html)
                result = [list(item[::-1]) for item in cand_paper_list if keywords_patten.findall(item[-1].lower())]
                for i, item in enumerate(result):
                    print '%d%% |'%(i*100/len(result)),'#'*(i*100/len(result)),'\r',
                    item[-1] = url + r'/' + item[-1]
                    item[1] = re.sub('<first>|</first>|<last>|</last>', '', item[1].strip())
                    ref = self.get_reference(item[0])
                    if ref:
                        abstract, reference = ref[0]
                    else:
                        abstract, reference = "",""
                    item.extend([reference, abstract])
                filename = self.conf_name + '20' + seed.strip(conf_id) + '_' + get_current_date() + '.csv'
                csv_writer(filename, result)
                logging.info( self.conf_name + '20' + seed.strip(conf_id) + ' file saved.')
            except:
                logging.debug('url not exist or timeout')

    def get_reference(self, title):
        '''
        get abstract, reference num from google of a paper
        '''
        res = []
        try:
            time.sleep(random.randint(5, 8))
            title = title.lower()
            key_words = '+'.join(title.split())
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            url = 'https://scholar.guso.ml/scholar?q=' + key_words + '&hl=zh-CN'
            req = urllib2.Request(url=url, headers = headers)
            html = opener.open(req).read().lower()
            rgx = '<h3 class="gs_rt">.*?' + title + '\.{0,}</a></h3>.*?<div class="gs_rs">(.*)?</div><div class="gs_fl"><a .*?>被引用次数：(\d{0,})</a>'
            patten = re.compile(rgx, re.S)
            res = patten.findall(html)
        except:
            logging.debug('no paper find')
        finally:
            return res

def csv_writer(filename, data):
    csvfile = file(filename,'wb')
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()
    
def get_current_date():
    return datetime.datetime.now().strftime('%Y%m%d')

if __name__ == '__main__':
    acl_event = {'ACL':'P','CL':'J', 'EMNLP':'D', 'COLING':'C', 'EACL':'E','NAACL':'N'}
    keywords = {'sentence','word','embedding','representation'}
    start_time = datetime.datetime.now()
    for event in acl_event.items():
        logging.info('Start to get paper list from ' + event[0])
        conf_id = event[1]
        base_url = r'https://www.aclweb.org/anthology/' + conf_id + '/'
        seeds = map(lambda x: conf_id + str(x), range(13, 17))
        acl_spider = Spider(base_url, seeds, event, keywords)
        acl_spider.research()
    end_time = datetime.datetime.now()
    logging.info("\nDone! Seconds cost:"+str((end_time - start_time).seconds))