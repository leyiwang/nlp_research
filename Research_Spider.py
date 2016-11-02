#coding=utf8
import re, urllib2, csv, logging
class Spider():
    def __init__(self, url, seeds, conference_id):
        self.url = url
        self.seeds = seeds
    def research(self):
        for seed in self.seeds:
            url = self.url + seed
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read()
            patten = re.compile(r'<p.*?' + conference_id + '\d{2}-\d{4}.*?<b>(.*)?</b><br><i>(.*)?</i>')
            cand_paper_list = patten.findall(html)
            result = [item[::-1] for item in cand_paper_list if 'word' in item[1].lower() or 'sentence' in item[1].lower()]
            filename = "ACL_20" + seed.strip(conference_id) + '.csv'
            csv_writer(filename, result)

def csv_writer(filename,data):
    csvfile = file(filename,'wb')
    w = csv.writer(csvfile)
    w.writerows(data)
    csvfile.close()
#P/P14
if __name__ == '__main__':
    conference_id = 'D'
    url = r'https://www.aclweb.org/anthology/' + conference_id + '/'
    seeds = map(lambda x: conference_id + str(x), range(13, 17))
    acl_spider = Spider(url, seeds, conference_id)
    acl_spider.research()