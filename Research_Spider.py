#coding=utf8
import re, urllib2, csv, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level = logging.DEBUG)

class Spider():
    def __init__(self, base_url, seeds, event):
        self.base_url = base_url
        self.seeds = seeds
        self.conf_name = event[0]
        self.conf_id = event[1]
        
    def research(self):
        for seed in self.seeds:
            url = self.base_url + seed
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                html = response.read()
                patten = re.compile(r'<p.*?(' + conf_id + '\d{2}-\d{4}.pdf)*?<b>(.*)?</b><br><i>(.*)?</i>')
                cand_paper_list = patten.findall(html)
                
                result = [item[::-1] for item in cand_paper_list if 'word' in item[1].lower() or 'sentence' in item[1].lower()]
                filename = self.conf_name + '20' + seed.strip(conf_id) + '.csv'
                csv_writer(filename, result)
                logging.info( self.conf_name + '20' + seed.strip(conf_id) + ' file saved.')
            except:
                logging.debug('URL not exit')
            finally:
                pass

def csv_writer(filename,data):
    csvfile = file(filename,'wb')
    w = csv.writer(csvfile)
    w.writerows(data)
    csvfile.close()

if __name__ == '__main__':
    acl_event = {'CL':'J', 'ACL':'P','EMNLP':'P', 'COLING':'C', 'EACL':'E', 'NAACL':'N'}
    for event in acl_event.items():
        conf_id = event[1]
        base_url = r'https://www.aclweb.org/anthology/' + conf_id + '/'
        seeds = map(lambda x: conf_id + str(x), range(13, 17))
        acl_spider = Spider(base_url, seeds, event)
        acl_spider.research()
    logging.info("Done!")