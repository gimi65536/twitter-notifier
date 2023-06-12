from scrapy.crawler import CrawlerProcess

from yaml import safe_load
from decouple import config
from datetime import datetime
from time import sleep

from spider import TweetSpider
from pipeline import TweetPipeline

from json import load, dump
from pathlib import Path

with open(config('GRAB_INFO')) as f:
    data = safe_load(f)

history_path = Path('history/history.json')
history = [set() for _ in data['instance']]
if(history_path.exists()):
	with open(history_path) as f:
		try:
			j = load(f)
		except:
			pass
		else:
			history = [set(l) for l in j]

process = CrawlerProcess(
    settings={
        "DOWNLOAD_HANDLERS": {
			"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
			"https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
		},
		"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
		"ITEM_PIPELINES": {
			TweetPipeline: 100,
		},
    }
)

# Main
while True:
	sleep(data['period'])
	print(datetime.now().strftime('%Y%m%d %H:%M'))
	for index, i in enumerate(data['instance']):
		process.crawl(TweetSpider, instance = i, history = history[i])

	process.start(stop_after_crawl = False)
	# All processes are done
	with open(history_path, 'w') as f:
		dump(history, f)
