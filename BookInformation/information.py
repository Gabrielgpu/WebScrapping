from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore, Back, Style



def book_title(navegador):
    try:
        titulo = navegador.find_element(By.ID, "productTitle").text
    except NoSuchElementException:
        return ''
    return titulo


def book_description(navegador):
    try:
        element = navegador.find_element(By.ID, 'bookDescription_feature_div').text
        return element
    except NoSuchElementException:
        print(Fore.RED + "Descrição, primeira tentativa falhou")
        
    try:
        element = navegador.find_element(By.ID, 'productInfoTabExpander0').text
        return element
    except NoSuchElementException:
        print(Fore.RED + "Descrição, segunda tentativa falhou")
        return ''
        

def book_price(navegador):
    try:
        inf_preco = navegador.find_element(By.XPATH, '//*[@id="mediaMatrixGridAODPopover"]/a/span').text
    except:
        return ''
    return inf_preco



def book_details(navegador, stop=False):
    editora = ''
    idioma = ''
    capa = ''
    isbn13 = ''
    comprimento = ''
    altura = ''
    largura = ''
    paginas = ''
    edicao = ''
    ano = ''

    if stop:
        return editora, idioma, capa, isbn13, comprimento, largura, altura, paginas, edicao, ano

    try:
        details = navegador.find_element(By.ID, 'detailBulletsWrapper_feature_div')
        details = details.text

        details = details.split('\n')


        for inf in details:

            if 'leitor de tela' in inf.lower():
                other_type(navegador)

            if 'editora' in inf.lower():
                inf = inf[inf.index(':')+1:].strip()
                inf = inf.replace('(', ';').replace(')', '')
                inf = inf.split(';')

                if len(inf) == 3:
                    editora = inf[0]
                    edicao = inf[1]
                    ano = inf[2]
                    ano = ano[-4:]
                
                else:
                    editora = inf[0]
                    ano = inf[1]
                    ano = ano[-4:]

            elif 'idioma' in inf.lower():
                inf = inf[inf.index(':')+1:].strip()
                idioma = inf

            elif 'isbn-13' in inf.lower():
                inf = inf[inf.index(':')+1:].strip()
                isbn13 = inf.replace('-' , '')

            elif 'dimensões' in inf.lower():
                inf = inf[inf.index(':')+1:].strip()
                inf = inf.split()
                comprimento = inf[0]
                largura = inf[2]
                altura = inf[4]

            elif 'capa' in inf.lower():
                inf = inf[inf.index(':')+1:].strip()
                inf = [pag_numeros for pag_numeros in inf if pag_numeros.isnumeric()]
                paginas = ''.join(inf)
                # print(paginas)
    except NoSuchElementException: 
        print('Não encontrei os detalhes do livro')



    

    return editora, idioma, capa, isbn13, comprimento, largura, altura, paginas, edicao, ano

def book_category(navegador):
    try:
        categoria = navegador.find_element(By.XPATH, '//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/ul/li/span/a').text
    except NoSuchElementException:
        return ''
    return categoria


def other_type(navegador):
    list_type = navegador.find_elements(By.CLASS_NAME, 'swatchElement')

    if len(list_type) > 1:
        for index, tipo in enumerate(list_type):
            tipo = tipo.text
            if 'capa comum' in tipo.lower():
                list_type[index].click()
                book_details(navegador)
    else:
        book_details(navegador, stop=True)

    return book_details(navegador, stop=True)



def search_for_book_author(navegador):
    try:
        autor = navegador.find_element(By.XPATH, '//*[@id="bylineInfo"]/span/a')
    except NoSuchElementException:
        print('Não encontrei o autor do livro')
        return None
    autor = autor.text
    # print(autor)
    return autor