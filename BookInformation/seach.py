from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_book(isbn, navegador):
  barra_de_pesquisa = navegador
  barra_de_pesquisa.clear()
  barra_de_pesquisa.send_keys(isbn)
  time.sleep(1)
  barra_de_pesquisa.send_keys(Keys.ENTER)
