from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def check_if_is_book(navegador):
    try:
        type_book = navegador.find_element(By.CLASS_NAME, 'swatchElement')
        type_book = type_book.text

        if 'capa comum' in type_book.lower() or 'capa dura' in type_book.lower() or 'kindle' in type_book.lower() or 'encadernação' in type_book.lower() or 'livro cartonado' in type_book.lower() or 'capa flexível' in type_book.lower() or 'livro com brinde' in type_book.lower() or 'livro didático' in type_book.lower() or 'edição econômica' in type_book.lower() or 'capa clássica com blocagem' in type_book.lower() or 'livro de bolso' in type_book.lower() or 'audiolivro' in type_book.lower():
            return "É um Livro"
    except NoSuchElementException:
        print('Não foi possivel encontrar o tipo do livro')

    try:
        have_isbn = navegador.find_element(By.ID, 'detailBulletsWrapper_feature_div')
        have_isbn = have_isbn.text

        if 'isbn' in have_isbn.lower():
            return "É um livro"
    except NoSuchElementException:
        print('Não encontrei o ISBN do livro')

    return "Não é um livro"