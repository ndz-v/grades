from bs4 import BeautifulSoup
from mechanicalsoup.stateful_browser import StatefulBrowser
import click
import mechanicalsoup
import re


class PageService:

    LOGIN_URL = 'https://pos.fernuni-hagen.de/qisserver/rds?state=user&type=0'

    credential_file: str
    username: str
    password: str
    graduation: str
    subject: str
    data: list
    browser: StatefulBrowser

    def __init__(self, user_name='', password='', graduation='', subject=''):
        '''
        '''
        self.username = user_name
        self.password = password
        self.graduation = graduation
        self.subject = subject

        self.browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True
        )

    def get_grades_overview_page(self) -> BeautifulSoup:
        result = self.browser.open(self.LOGIN_URL)

        if result.status_code != 200:
            click.echo(' Internetverbindung nicht verfügbar oder Seite offline.')
            exit()

        self.browser.select_form('form[name="loginform"]')
        self.browser['asdf'] = self.username
        self.browser['fdsa'] = self.password
        self.browser['submit'] = 'Anmelden'
        result = self.browser.submit_selected()

        if result.status_code != 200:
            click.echo(' Anmelde Daten sind falsch!')
            return

        page = self.browser.get_current_page()
        link_list = page.find_all('a', text='Prüfungsverwaltung', href=True)
        self.browser.follow_link(link_list[0])
        page = self.browser.get_current_page()
        link_list = page.find_all('a', text='Notenübersicht', href=True)
        self.browser.follow_link(link_list[0])
        page = self.browser.get_current_page()
        link_list = page.find_all('a', title=re.compile(f'(?=.*{self.graduation})(?=.*{self.subject})'), href=True)
        self.browser.follow_link(link_list[0])
        page = self.browser.get_current_page()

        return page

    def get_statistics_page(self, link):
        self.browser.follow_link(link)
        statistics_page = self.browser.get_current_page()
        return statistics_page
