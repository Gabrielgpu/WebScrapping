from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
def click_on_the_book(navegador):
    try:
      imagem = navegador.find_element(By.CLASS_NAME, 's-image').get_attribute('src')
      navegador.find_element(By.CLASS_NAME, 's-image').click()
    except NoSuchElementException:
       return 'livro não encontrado'
    
    return imagem