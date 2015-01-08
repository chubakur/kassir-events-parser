# -*- coding: utf-8 -*-
# simple.py

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, QObject, Qt
import json
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from kassir.spiders import EventSpider
from scrapy.utils.project import get_project_settings
from threading import Thread
import webbrowser


class ListEditor(QtGui.QWidget):
    def __init__(self):
        super(ListEditor, self).__init__()
        self.setWindowTitle(u"Список событий")
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.list_widget = QtGui.QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.select_item)
        self.layout.addWidget(self.list_widget)
        self.list = []
        self.bottom_layout = QtGui.QHBoxLayout()
        self.event_textbox = QtGui.QLineEdit()
        self.add_button = QtGui.QToolButton()
        self.add_button.setIcon(QtGui.QIcon("add.png"))
        self.add_button.clicked.connect(self.add_to_list)
        self.bottom_layout.addWidget(self.event_textbox)
        self.bottom_layout.addWidget(self.add_button)
        self.layout.addLayout(self.bottom_layout)
        self.load_list()

    def select_item(self, item):
        self.list.remove(unicode(item.text()))
        self.update_list()

    def add_to_list(self):
        self.list.append(unicode(self.event_textbox.text()))
        self.event_textbox.clear()
        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.list)
        with open("events.json", "w") as f:
            f.write(json.dumps(self.list))

    def load_list(self):
        try:
            f = open("events.json", "r")
            self.list = json.loads(f.read())
            f.close()
        except IOError:
            self.list = []
        self.update_list()

    def show(self):
        self.load_list()
        super(ListEditor, self).show()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.btn_layout = QtGui.QHBoxLayout()
        self.loading_label = QtGui.QLabel()
        self.loading_movie = QtGui.QMovie("loading.gif")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_movie.start()
        self.setWindowTitle(u'Поиск концертов')
        self.setLayout(self.layout)
        self.loading_label.hide()
        self.layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(self.btn_layout)
        self.eventListBtn = QtGui.QPushButton(u"Список групп")
        self.checkListBtn = QtGui.QPushButton(u"Искать")
        self.btn_layout.addWidget(self.eventListBtn)
        self.btn_layout.addWidget(self.checkListBtn)
        self.eventListBtn.clicked.connect(self.edit_list)
        self.checkListBtn.clicked.connect(self.check)
        self.list_editor = ListEditor()

    @pyqtSlot()
    def edit_list(self):
        self.list_editor.show()

    @pyqtSlot()
    def check(self):
        print len(self.list_editor.list)
        if len(self.list_editor.list) == 0:
            return
        spider = EventSpider(self)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start()
        Thread(target=reactor.run, args=(False,)).start()

    def add_item(self, item):
        item_name = item['name'][0]
        result = QtGui.QMessageBox.question(None, u"Концерт", item_name, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            webbrowser.open_new(item['url'])


app = QtGui.QApplication(sys.argv)

main = MainWindow()
main.show()

sys.exit(app.exec_())