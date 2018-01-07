PATHSPIDER="./scraper/scraperspider/spiders"
PATHPROCESSED="../spiders/output"

#start crawling
cd $PATHSPIDER
scrapy crawl comundi

#start processed_data
cd $PATHPROCESSED
python wrang.py