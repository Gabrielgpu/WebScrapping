from BookInformation.check_book import check_if_is_book
from BookInformation.information import  book_details, book_description, search_for_book_author, book_price, book_title, book_category
from BookInformation.seach import search_book
from BookInformation.click_book import click_on_the_book
from BookInformation.void import element_empty


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, Style


