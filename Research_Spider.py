#coding=utf8
'''
  Title: Research Spider for Anthology
  Version: V0.2
  Author: Louie Wang
  Date: Last update 2016-11-3
'''
import re, urllib2, csv, logging, datetime
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
                html = urllib2.urlopen(request, timeout=5).read()
                cand_paper_list = patten.findall(html)
                result = [list(item[::-1]) for item in cand_paper_list if keywords_patten.findall(item[-1].lower())]
                for item in result:
                    item[-1] = url + r'/' + item[-1] 
                filename = self.conf_name + '20' + seed.strip(conf_id) + '.csv'
                csv_writer(filename, result)
                logging.info( self.conf_name + '20' + seed.strip(conf_id) + ' file saved.')
            except:
                logging.debug( self.conf_name + '20' + seed.strip(conf_id) +' URL not exit')
            finally:
                pass

def csv_writer(filename,data):
    csvfile = file(filename,'wb')
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

if __name__ == '__main__':
    acl_event = {'CL':'J', 'ACL':'P','EMNLP':'D', 'COLING':'C', 'EACL':'E', 'NAACL':'N'}
    keywords = {'sentence','word','embedding'}
    start_time = datetime.datetime.now()
    for event in acl_event.items():
        logging.info('Start to get paper list from '+event[0])
        conf_id = event[1]
        base_url = r'https://www.aclweb.org/anthology/' + conf_id + '/'
        seeds = map(lambda x: conf_id + str(x), range(13, 17))
        acl_spider = Spider(base_url, seeds, event, keywords)
        acl_spider.research()
    end_time = datetime.datetime.now()
    logging.info("\nDone! Seconds cost:"+str((end_time - start_time).seconds))