__author__ = 'paolinux'

from Scraper import Scraper

def main():
    scraper = Scraper(threshold=3)
    scraper.run()

    for k, v in scraper.tree.out().items():
        print k,v


if __name__ == '__main__':
    main()