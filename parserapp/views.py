from itertools import groupby
from urllib.request import urlopen
from django.shortcuts import render
from django.views import View
from bs4 import BeautifulSoup
import re


class Entry:
    def __init__(self, num, url, phones, emails):
        self.num = num
        self.url = url
        self.phones = phones
        self.emails = emails

    def get_emails(self):
        return self.emails

    def get_phones(self):
        return self.phones

    # def to_json(self):
    #     return {
    #         'url': self.url,
    #         'phones': self.phones,
    #         'emails': self.emails
    #     }


class ParserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'parserapp/parser_page.html', {})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        urls_row = request.POST['urls_row']
        return render(request, 'parserapp/parser_page_result.html', {
            'entrys': self.run_pars(urls_row)
        })

    def is_valid(self):
        if self.urls:
            return True
        return False

    def run_pars(self, urls_row: str):
        self.urls = self.transform_urls(urls_row)
        self.entrys = []
        if self.is_valid():
            return self.pars()
        return None

    def transform_urls(self, urls_row):
        if '\n' in urls_row:
            return urls_row.splitlines()
        return urls_row.split(' ')

    def pars(self):
        num = 0
        for url in self.urls:
            try:
                page = urlopen(url)
                page_code = BeautifulSoup(page, 'html.parser')
                match_phones = page_code.find_all(
                    string=re.compile(r'((8|\+7)[\- ]?){1}(\(?\d{3}\)?[\- ]?){1}[\d\- ]{7,10}'))
                match_emails = page_code.find_all(string=re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))
                phones = []
                for phone in match_phones:
                    if len(phone) <= 18:
                        phones.append(phone)
                phones = [el for el, _ in groupby(phones)]
                emails = [el for el, _ in groupby(match_emails)]
                num = num + 1
                self.entrys.append(Entry(num, url, phones, emails))
            except Exception as e:
                print(e)
        return self.entrys

    # def get_all_emails(self):
    #     emails = []
    #     for entry in self.entrys:
    #         emails += entry.get_emails()
    #     return emails
