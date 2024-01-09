
from imports import modulos

import os
import pandas as pd



def manipular_categoria(categoria):
    if "religião" in categoria:
        categoria = categoria.replace("religião", "religião e espiritualidade")
    elif "espiritualidade" in categoria:
        categoria = categoria.replace("espiritualidade", "religião e espiritualidade")
    return categoria


def organizar_categoria(categoria):
    
    categoria_completa = ''
    for i, categoria_pai in enumerate(dict_categoria):
        if categoria_pai.lower() in categoria.lower():
            categoria_completa = categoria_pai
            break

    if categoria_completa:
        for i, filho in enumerate(dict_categoria[categoria_completa]):
            if i > 0:
                if filho.lower() in categoria.lower() and len(categoria) > 3:
                    if categoria_completa:
                        categoria_completa = categoria_completa + ">>" + filho
                        return manipular_categoria(categoria_completa)
                    else:
                        categoria_completa = categoria_filho[0] + ">>" + filho
                        return manipular_categoria(categoria_completa)
    else:        
        for categoria_pai in dict_categoria:    
            categoria_filho = dict_categoria[categoria_pai]
            for i, filho in enumerate(categoria_filho):
                if i > 0:
                    if filho.lower() in categoria.lower() and len(categoria) > 3:
                        if categoria_completa:
                            categoria_completa = categoria_completa + ">>" + filho
                            return manipular_categoria(categoria_completa)
                        else:
                            categoria_completa = categoria_filho[0] + ">>" + filho
                            return manipular_categoria(categoria_completa)

    return manipular_categoria(categoria_completa)    


chrome_options = modulos.Options()


chrome_options.add_argument("--start-maximized")


planilha = pd.read_excel(r'C:\Users\gabri\OneDrive\Área de Trabalho\robo\planilhasRelatório+de+inventário+12-14-2023.xlsx')


dict_categoria = {
                  "autoajuda": ["autoajuda"], 
                  "literatura": ["literatura","Infanto Juvenil", "Poesia", "Crônicas", "Fábulas"], 
                  "didáticos": ["didáticos"], 
                  "biografias": ["biografias"], 
                  "ficção": ["ficção", "Romance", "Fantasia", "Contos", "Terror", "Jogos", "Drama", "História em Quadrinhos", "Mangás"], 
                  "religião": ["religião", "Espiritismo", "Esoterismo", "Catolicismo", "Budismo", "Judaísmo", "Cristianismo", "Taoísmo", "Islamismo", "Afro-brasileiras"], 
                  "espiritualidade": ["espiritualidade", "Espiritismo", "Esoterismo", "Catolicismo", "Budismo", "Judaísmo", "Cristianismo", "Taoísmo", "Islamismo", "Afro-brasileiras"],
                  "Estudos": ["Estudos", "Teatro", "História", "Filosofia", "Ciência", "Política", "Psicologia", "Artes Marciais", "Matemática", "Administração", "Nutrição", "Artes e Fotografia", "Medicina Veterinária", "Medicina Alternativa", "Sociologia", "Saúde Mental", "Medicina", "Turismo", "Física", "Direito", "Biologia", "Marketing", "Culinária", "Saúde", "Economia", "Dicionário", "Química", "Psicanálise", "Finanças e Investimentos", "Empreender | Negócios", "Antropologia", "Linguagem", "Informática", "Geografia", "Sexologia", "Música", "Engenharia", "Educação", "Alfabetização", "Internet / Web", "Animais", "Mitologia", "Esportes", "Arquitetura"]
                  }


list_asin = planilha['asin'].to_list()
list_sku = planilha['sku'].to_list()
list_preco = planilha['preço'].to_list()
list_estoque = planilha['quantidade'].to_list()

quantidade_de_arquivos = os.listdir(r'C:\Users\gabri\OneDrive\Área de Trabalho\robo\planilhas prontas\dados')

iniciar = len(quantidade_de_arquivos) 
pular = 100
parar = len(list_asin)

iniciar = iniciar * pular + 78600
for index in range(iniciar, parar, pular):
    if index > iniciar:
        navegador.quit()

        
    navegador = modulos.webdriver.Chrome(options=chrome_options)

    navegador.get('https://www.amazon.com.br/')
    
    list_titulo = []
    list_argumentos = []
    list_autor = []
    list_image = []
    list_isbn13 = []
    list_editora = []
    list_idioma = []
    list_capa = []
    list_comprimento = []
    list_largura = []
    list_altura = []
    list_descricao = []
    list_paginas = []
    list_edicao = []
    list_ano = []
    list_categoria = []


    list_argumentos = [list_capa, list_editora, list_idioma, list_image, list_isbn13, list_comprimento, list_largura, list_altura, list_descricao, list_paginas, list_edicao, list_ano, list_autor, list_asin, list_titulo, list_preco, list_estoque, list_sku, list_categoria]
    stop = index + pular
    start = index
    for i in range(start, stop):

        while True:
            try:
                element = modulos.WebDriverWait(navegador, 5).until(
                    modulos.EC.presence_of_element_located((modulos.By.ID, 'twotabsearchtextbox'))
                )
                print(modulos.Fore.GREEN + "Passou")
                break
            except modulos.TimeoutException:
                print(modulos.Fore.RED + "Não encontrei o elemento de busca")
                navegador.refresh()


        modulos.search_book(list_asin[i], navegador.find_element(modulos.By.ID, 'twotabsearchtextbox'))

        imagem_livro = modulos.click_on_the_book(navegador)


        if 'livro não encontrado' in imagem_livro:
            modulos.element_empty(*list_argumentos, i)
            continue

        eh_livro = modulos.check_if_is_book(navegador)

        if 'Não é um livro' in eh_livro:
            modulos.element_empty(*list_argumentos, i)
            continue
        
        list_image.append(imagem_livro)

        autor = modulos.search_for_book_author(navegador)

        dados = modulos.book_details(navegador)

        tipo_preco = type(list_preco[i])

        if tipo_preco != str:
            inf_preco = modulos.book_price(navegador)
            preco = ""

            for number in inf_preco:
                if number.isnumeric() or number == ",":
                    preco += number

            list_preco[i] = preco.replace(",", ".")


        titulo = modulos.book_title(navegador)

        descricao = modulos.book_description(navegador)

        categoria = modulos.book_category(navegador)

        categoria_completa = organizar_categoria(categoria)

        list_categoria.append(categoria_completa)

        list_descricao.append(descricao)

        list_titulo.append(titulo)


        data_dict = {"editora": list_editora, "idioma": list_idioma, "capa": list_capa, "isbn13": list_isbn13, "comprimento": list_comprimento, "largura": list_largura, "altura": list_altura, "paginas": list_paginas, "edicao": list_edicao, "ano": list_ano}


        for i, data in enumerate(data_dict):
            data_dict[data].append(dados[i])

        list_autor.append(autor) if autor else list_autor.append(None)

    

    salvar_planilha = pd.DataFrame({
                                    'ID': '',
                                    'Código': list_isbn13, 
                                    'Descrição': list_titulo,
                                    'Unidade': '',
                                    'NCM': '',
                                    'Origem': '',
                                    'Preço': list_preco[start:stop],
                                    'Valor IPI fixo': '',
                                    'Observações': '',
                                    'Situação': '',
                                    'Estoque': list_estoque[start:stop],
                                    'Preço de custo': '',
                                    'Cód no fornecedor': '',
                                    'Fornecedor': '',
                                    'Localização': list_sku[start:stop],
                                    'Estoque maximo': '',
                                    'Estoque minimo': '',
                                    'Peso líquido (Kg)': '',
                                    'Peso bruto (Kg)': '',
                                    'GTIN/EAN': list_isbn13,
                                    'GTIN/EAN da embalagem': list_isbn13,
                                    'Largura do Produto': list_largura,
                                    'Altura do Produto': list_altura,
                                    'Profundidade do produto': list_comprimento,
                                    'Data Validade': '',
                                    'Descrição do Produto no Fornecedor': '',
                                    'Descrição Complementar': '',
                                    'Itens p/ caixa': '',
                                    'Produto Variação': '',
                                    'Tipo Produção': '',
                                    'Classe de enquadramento do IPI': '',
                                    'Código da lista de serviços': '',
                                    'Tipo do item': '',
                                    'Grupo de Tags/Tags': '',
                                    'Tributos': '',
                                    'Código Pai': '',
                                    'Código Integração': '',
                                    'Grupo de produtos': '',
                                    'Marca': list_editora,
                                    'CEST': '',
                                    'Volumes': '',
                                    'Descrição Curta': list_descricao,
                                    'Cross-Docking': '',
                                    'URL Imagens Externas': list_image,
                                    'Link Externo': '',
                                    'Meses Garantia no Fornecedor': '',
                                    'Clonar dados do pai': '',
                                    'Condição do produto': '',
                                    'Frete Grátis': '',
                                    'Número FCI': '',
                                    'Vídeo': '',
                                    'Departamento': '',
                                    'Unidade de medida': '',
                                    'Preço de compra': '',
                                    'Valor base ICMS ST para retenção': '',
                                    'Valor ICMS ST para retenção': '',
                                    'Valor ICMS próprio do substituto': '',
                                    "Categoria do produto": list_categoria,
                                    'Informações Adicionais': list_edicao,
                                    
                                    })
    
    planilha_custom = pd.DataFrame({
                            "ID": '',
                            "Código": list_isbn13,
                            "Descrição": list_descricao,
                            "anoDePublicacao": list_ano,
                            "numeroDePaginas": list_paginas,
                            "edicao": list_edicao,
                            "autor": list_autor,
    })


    indice = int(index / pular) + 1

    salvar_planilha.to_excel(r'C:\Users\gabri\OneDrive\Área de Trabalho\robo\planilhas prontas\principal-{}.xlsx'.format(indice), index=False)

    planilha_custom.to_excel(r'C:\Users\gabri\OneDrive\Área de Trabalho\robo\planilhas prontas\custom-{}.xlsx'.format(indice), index=False)

