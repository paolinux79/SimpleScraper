# -*- coding: utf-8 -*-
__author__ = 'paolinux'


import requests
from bs4 import BeautifulSoup, SoupStrainer
from ScrapeTree import Tree
from ScrapeTree import Node
import json
from random import randint

class Scraper:


    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        }

    ENGINE_URL = "https://www.google.iq/search"

    BAD_WORDS = {"وسائل إعلام المجاهدين":5,
                " إعلام البلاتفورم":5,
                " إعلام الزهراء":7,
                " القاعدة في المغرب الاسلامي":2,
                " منتدى اليقظة الإسلامي":1}

    tree = None
    counter = 0
    threshold = 0


    def __init__(self,threshold):
        self.tree = Tree.Tree()
        self.threshold = threshold

    def get_pattern(self):
        return self.BAD_WORDS.keys()[randint(0,len(self.BAD_WORDS)-1)]


    def run(self):
        word = self.get_pattern()
        print "word is  " + word
        payload = self.search_on_google(pattern=word, start=10)
        links = self.find_links_on_google_search(payload)
        print "found " + str(len(links)) + " on google page"
        self.process(links=links, parent_id=0)


    def process(self, links, parent_id):
        print "found " + str(len(links)) + " links for parent_id " + str(parent_id)
        for link in links:
            print "processing " + link
            page = self.fetch_a_link(link=link)
            if page is not None:
                res = self.find_matchings(page=page)
                score = self.compute_score(res)
                if score > 0:
                    print "score is " + str(score)
                    new_node =self.add_a_node(link=link,res=res,parent_id=parent_id, score=score)
                    print "node level is " + str(new_node.get_level()) + " child of " + str(new_node.get_parent_id())
                    if new_node.get_level() < self.threshold:
                        print "getting links",
                        new_links = self.get_links_from_page(page)
                        print str(len(new_links))
                        self.process(new_links,parent_id=new_node.get_node_id())


    def add_a_node(self, link, res, parent_id, score):
        new_node = Node.Node(url=link, score=score, matchings=res, tree=self.tree)
        node_id = self.tree.add_node(new_node)
        new_node.set_node_id(node_id)
        new_node.add_parent(parent_id=parent_id)
        return new_node

    def search_on_google(self,pattern, start):
        diz = {}
        diz['start'] = start
        diz['q'] = pattern
        out = requests.get(self.ENGINE_URL, params=diz, headers=self.headers)
        if out.status_code == 200:
            return out.text
        return None


    def find_links_on_google_search(self,payload):
        links = []
        soup = BeautifulSoup(payload)
        h3s = soup.find_all('h3',class_="r")
        for h3 in h3s:
            x = h3.find('a')['href'].split('q=')[1].split('&')[0]
            links.append(x)
        return links

    def fetch_a_link(self,link):
        try:
            got = requests.get(link)
            page = got.text
        except:
            return None
        return page

    def get_links_from_page(self,page):
        links = []
        soup = BeautifulSoup(page)
        for tag in soup.findAll('a', href=True):
            if tag['href'].startswith('http'):
                links.append(tag['href'])
        return links

    def find_matchings(self,page):
        results = {}
        for k, v in self.BAD_WORDS.items():
            if k in page.encode('UTF-8'):
                count = page.count(k)
                results[k] = count
        # print results
        return results


    def compute_score(self,matchings):
        score = 0
        for k,v in matchings.items():
            score += self.BAD_WORDS[k] * v
        return score



