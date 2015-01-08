# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, QObject


class ItemNotify(QObject):
    new_item = pyqtSignal(object)

    def process_item(self, item, spider):
        item_name = item['name'][0]
        with codecs.open("trace.log", "a", encoding="utf-8") as f:
            for elem in self.list:
                if elem.lower() in item_name.lower():
                    self.new_item.emit(item)
                    f.write("%s in %s %s\n" % (item_name, elem, item['url']))
                else:
                    f.write("%s not in %s\n" % (item_name, elem))
        return item

    def open_spider(self, spider):
        spider.gui.loading_label.show()
        self.list = spider.gui.list_editor.list
        self.new_item.connect(spider.gui.add_item)
        with codecs.open("trace.log", "w", encoding="utf-8") as f:
            f.write("Array length: %d\n" % len(self.list))

    def close_spider(self, spider):
        spider.gui.loading_label.hide()
        self.new_item.disconnect(spider.gui.add_item)