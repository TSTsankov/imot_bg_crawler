# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import datetime
import json
import os


class ImotBgCrawlerPipeline:
    result = []
    start_time = None

    def open_spider(self, spider):
        self.start_time = datetime.datetime.now()

    def get_results_file(self):
        current_path = os.path.dirname(__file__)
        _date = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M")
        return os.path.join(
            current_path,
            'output_files',
            f'result_{_date}.json',
        )

    def process_item(self, item, spider):
        self.result.append(item)
        return item

    def close_spider(self, spider):
        end_time = datetime.datetime.now()

        crawled_data = {
            'totalFound': len(self.result),
            'stated': self.start_time.isoformat(),
            'ended': end_time.isoformat(),
            'tookSeconds': (end_time - self.start_time).seconds,
        }

        self.result.append(crawled_data)

        with open(self.get_results_file(), "a", encoding="utf-8") as f:
            f.write(json.dumps(
                self.result,
                ensure_ascii=False,
            ))
