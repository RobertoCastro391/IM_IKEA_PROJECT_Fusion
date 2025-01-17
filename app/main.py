import http.client
import json
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unicodedata
import time

import webbrowser
import os

from os import system
import xml.etree.ElementTree as ET
import ssl
import websockets

from tts import TTS

not_quit = True
intent_before = ""
products_retrived = []

intents_list = ["ASK_HELP", "SHOW_PRODUCTS", "OPEN_WEBSITE", "SCROLL_UP", "SCROLL_DOWN", "SELECT_PRODUCT_BY_POSITION", "ADD_TO_CART", "ADD_TO_FAVORITES", "SHOW_CART", "SHOW_FAVORITES", "REMOVE", "remove_cart", "remove_favorites", "GO_BACK", "SHOW_MORE", "FINALIZE_ORDER", "MAIN_PAGE", "CLOSE_WEB", "NLU_FALLBACK", "GO_UP", "GO_DOWN","GO_LEFT", "GO_RIGHT", "EXIT", "SELECT", "ORDER_PRODUCTS"]

driver = None

# Função para abrir o site (exemplo, IKEA) usando o Selenium
def open_website():
    """
    Função que usa o Selenium para abrir o site do IKEA e tentar clicar no botão de aceitação de cookies.
    """
    global driver
    website = "https://www.ikea.com/pt/pt/"  # URL do site para abrir

    try:
        # Verifica se o driver já está ativo ou precisa ser reiniciado
        if driver is None or not is_driver_alive():
            # Caminho do driver do Selenium (atualize conforme necessário)
            service = Service("C:\\Users\\Usuario\\Downloads\\chromedriver-win64\\chromedriver.exe")  # Atualize para o caminho correto
            # service = Service("C:\\Users\\rober\\Downloads\\chromedriver-win64\\chromedriver.exe")  # Atualize para o caminho correto
            driver = webdriver.Chrome(service=service)
        
        # Abre o site
        driver.get(website)
        driver.maximize_window()  # Maximiza a janela do navegador

        # Espera e tenta clicar no botão de aceitação de cookies
        try:
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
        except Exception:
            print("Não foi possível encontrar o botão de aceitação de cookies.")
        
        print(f"Abrindo o site do IKEA Portugal...")

    except Exception as e:
        print(f"Erro ao abrir o site: {str(e)}")

def remove_accents(input_str):
    if input_str is not None:
        # Transforma em formato Unicode Normalizado e remove caracteres acentuados
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return None

def show_product(category, tts):

    #remove acentos qualquer tipo de acento
    category2 = remove_accents(category)

    global driver

    if driver is None:
        print("Driver não foi inicializado.")
        return
      
    if not category:
        tts(text="Não consegui entender a categoria que gostaria de procurar.")
        return []

    try:
            
        print("A iniciar pedido:")
        tts(f"A procurar por {category}!")
            
        # Conexão com a API do IKEA
        conn = http.client.HTTPSConnection("ikea-api.p.rapidapi.com")
        # Headers para autenticação
        headers = {
            'x-rapidapi-key': "f6ac7694f0mshad1a1e112b29308p1def65jsn84a5131e4970",
            'x-rapidapi-host': "ikea-api.p.rapidapi.com"
        }

        # Endpoint da API com o termo de busca
        endpoint = f"/keywordSearch?keyword={category2}&countryCode=pt&languageCode=pt"

        # Faz a requisição à API
        conn.request("GET", endpoint, headers=headers)

        print(f"Requisição GET para {endpoint}")
        

        res = conn.getresponse()
        data = res.read()
        products = json.loads(data.decode("utf-8"))  # Decodifica a resposta JSON

        products_retrived.clear()
        
        for product in products:
                products_retrived.append(product)

            # Verifica se há produtos na resposta
        if not products:
            tts(f"Não encontrei produtos na categoria '{category}'.")
            return []

        # Prepara a lista de produtos
        product_list = "\n".join([
            f"- {item['name']} (Preço: {item['price']['currentPrice']} {item['price']['currency']})"
            for item in products[:5]  # Mostra os 5 primeiros produtos
        ])

        tts(f"Aqui estão alguns produtos da categoria '{category}'!")

    except Exception as e:
        # Tratamento de erros
        tts("Desculpe, houve um problema ao procurar os produtos. Tente novamente mais tarde.")
        print(f"Erro na integração com a API do IKEA: {e}")

    try:
        print("Buscando no site da IKEA com Selenium...")

        driver.execute_script("window.scrollTo({ top: 0, behavior: 'smooth' });")

        time.sleep(1)

        # Localiza o campo de busca
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-field__input"))
            )            
        search_box.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto
        search_box.send_keys(Keys.BACKSPACE)  # Apaga o texto selecionado
        search_box.send_keys(category2)

        # Aciona o botão de busca
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-box__searchbutton"))  # Ajuste conforme o ID correto
        )
        search_button.click()

        # Highlight and store the first product
        time.sleep(1)  # Allow time for the page to load

        # Inject CSS for highlighting
        driver.execute_script("""
            const style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `
                .selected {
                    border: 2px solid red;
                    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                }
            `;
            document.head.appendChild(style);
        """)

        driver.execute_script("""
            let selectedDiv = null;

            // Highlight the first product
            let firstProduct = document.querySelector('div[data-testid="plp-product-card"]');
            if (firstProduct) {
                if (selectedDiv) {
                    selectedDiv.classList.remove('selected');
                }
                firstProduct.classList.add('selected');
                selectedDiv = firstProduct;

                // Store selected product globally
                window.selectedDiv = selectedDiv;

                firstProduct.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        """)


    except Exception as e:
            tts("Houve um problema ao realizar a busca no site. Tente novamente mais tarde.")
            print(f"Erro no Selenium: {e}")

    return []


def is_driver_alive() -> bool:
    """
    Verifica se o driver do Selenium ainda está ativo.
    """
    try:
        driver.title  # Verifica se o driver ainda tem acesso à página
        return True
    except:
        close_driver()  # Fecha o driver se não estiver mais ativo
        return False

def close_driver(tts):
    """
    Fecha o driver se ele estiver inicializado.
    """
    global driver
    if driver:
        try:
            tts("A fechar o IKEA! Volte Sempre!")
            driver.quit()  # Fecha o driver do Selenium
        except Exception:
            pass  # Ignora exceções durante o fechamento
        driver = None  # Define o driver como None após fechá-lo

def scroll_down():
    """
    Rola a página para baixo usando o Selenium.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Rola a página suavemente para baixo (500px)
        driver.execute_script("window.scrollBy({top: 500, behavior: 'smooth'});")  # Ajuste o valor conforme necessário
        print("A página foi rolada para baixo.")
    
    except Exception as e:
        print(f"Houve um problema ao rolar a página: {e}")

def scroll_up():
    """
    Rola a página para cima usando o Selenium.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Rola a página suavemente para cima (500px)
        driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")  # Ajuste o valor conforme necessário
        print("A página foi rolada para cima.")
    
    except Exception as e:
        print(f"Houve um problema ao rolar a página: {e}")
    
def open_cart(tts):
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Open the IKEA shopping cart page
        driver.get("https://www.ikea.com/pt/pt/shoppingcart/")
        print("O carrinho foi aberto.")
        tts("O carrinho foi aberto.")

        # Wait for the page to load and locate the product container
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_product_j61sc_1"))
        )

        # Inject CSS for highlighting if not already present
        driver.execute_script("""
            if (!document.querySelector('style#cart-selection-style')) {
                const style = document.createElement('style');
                style.id = 'cart-selection-style';
                style.type = 'text/css';
                style.innerHTML = `
                    .selected {
                        border: 2px solid red;
                        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
        """)

        # Highlight and store the first product div
        driver.execute_script("""
            let productDiv = document.querySelector('div._product_j61sc_1');
            if (productDiv) {
                productDiv.classList.add('selected'); // Add highlighting
                productDiv.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Scroll into view
                
                // Store the selectedDiv globally for future operations
                window.selectedDiv = productDiv;
            }
        """)

        print("O carrinho foi aberto e o primeiro produto foi selecionado!")
    except Exception as e:
        tts("Não foi possível abrir o carrinho.")
        print(f"Erro ao abrir o carrinho: {e}")

    return []

def open_favourites(tts):
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Open the IKEA favourites page
        driver.get("https://www.ikea.com/pt/pt/favourites/")

        # Wait for the favourites list to load
        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ListThumbnail_container__tCqlx"))
        )

        # Click the list thumbnail button
        select_list_button = driver.find_element(By.CSS_SELECTOR, "button.ListThumbnail_container__tCqlx")
        driver.execute_script("arguments[0].click();", select_list_button)

        # Wait for the product cards to appear
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductCard_listProductCard__sr7fg"))
        )

        # Ensure the CSS for the 'selected' class is added
        driver.execute_script("""
            if (!document.querySelector('style#favourites-selection-style')) {
                const style = document.createElement('style');
                style.id = 'favourites-selection-style';
                style.type = 'text/css';
                style.innerHTML = `
                    .selected {
                        border: 2px solid red;
                        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
        """)

        # Highlight and store the first product div
        driver.execute_script("""
            let productDiv = document.querySelector('div.ProductCard_listProductCard__sr7fg');
            
            if (productDiv) {
                productDiv.classList.add('selected'); // Add highlighting
                productDiv.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Scroll into view
                
                // Store the selectedDiv globally for future operations
                window.selectedDiv = productDiv;
            }
        """)

        print("A lista dos favoritos foi aberta e o primeiro produto foi selecionado!")
        tts("A lista dos favoritos foi aberta!")
    except Exception as e:
        tts("Não foi possível abrir os favoritos ou selecionar o produto.")
        print(f"Erro ao abrir os favoritos: {e}")

    return []


def add_to_cart(tts):

    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return
    
    try:
        # Localiza o botão de adicionar ao carrinho
        wait = WebDriverWait(driver, 15)
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pip-btn.pip-btn--emphasised.pip-btn--fluid"))
        )

        print("A clicar no botão de adicionar ao carrinho...")
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        
        wait = WebDriverWait(driver, 15)
        close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.rec-modal-header__close"))
        )

        print("A clicar no botão de fechar...")
        driver.execute_script("arguments[0].click();", close_button)
        tts("O produto foi adicionado ao carrinho.")

    except Exception as e:
        tts("Não foi possível adicionar o produto ao carrinho.")
        print(f"Erro ao adicionar ao carrinho: {e}")
    
    return []

def add_to_favorites(tts):
    
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Localiza o botão de adicionar aos favoritos
        wait = WebDriverWait(driver, 15)
        add_to_favorites_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-favourite-button"))
        )

        print("A clicar no botão de adicionar aos favoritos...")
        driver.execute_script("arguments[0].click();", add_to_favorites_button)
        tts("O produto foi adicionado aos favoritos.")
    except Exception as e:
        tts("Não foi possível adicionar o produto aos favoritos.")
        print(f"Erro ao adicionar aos favoritos: {e}")

    return []

def go_back(tts):
    """
    Função para voltar à página anterior no navegador.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        tts("O navegador não foi iniciado. Por favor, tente novamente.")
        return

    try:
        # Comando do Selenium para voltar à página anterior
        driver.back()

        time.sleep(1)  # Espera para a página carregar
        current_url = driver.current_url.lower()


        # Inject CSS for highlighting
        driver.execute_script("""
            const style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `
                .selected {
                    border: 2px solid red;
                    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                }
            `;
            document.head.appendChild(style);
        """)

    
        if "search" in current_url or "products" in current_url:
            driver.execute_script("""
                let selectedDiv = null;

                // Highlight the first product
                let firstProduct = document.querySelector('div[data-testid="plp-product-card"]');
                if (firstProduct) {
                    if (selectedDiv) {
                        selectedDiv.classList.remove('selected');
                    }
                    firstProduct.classList.add('selected');
                    selectedDiv = firstProduct;

                    // Store selected product globally
                    window.selectedDiv = selectedDiv;

                    firstProduct.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            """)
            

        elif "favourites" in current_url or "favorites" in current_url:

            # Highlight and store the first product div
            driver.execute_script("""
                let productDiv = document.querySelector('div.ProductCard_listProductCard__sr7fg');
                
                if (productDiv) {
                    productDiv.classList.add('selected'); // Add highlighting
                    productDiv.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Scroll into view
                    
                    // Store the selectedDiv globally for future operations
                    window.selectedDiv = productDiv;
                }
            """)

        elif "shoppingcart" in current_url or "cart" in current_url:

            # Highlight and store the first product div
            driver.execute_script("""
                let productDiv = document.querySelector('div._product_j61sc_1');
                if (productDiv) {
                    productDiv.classList.add('selected'); // Add highlighting
                    productDiv.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Scroll into view
                    
                    // Store the selectedDiv globally for future operations
                    window.selectedDiv = productDiv;
                }
            """)

        print("Página anterior.")
        tts("Página anterior.")
    except Exception as e:
        tts("Não foi possível voltar à página anterior.")
        print(f"Erro ao voltar à página anterior: {e}")
    
    return []

def show_more(tts):

    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return
    
    try:

        # Localiza o botão "Mostrar mais"
        wait = WebDriverWait(driver, 15)
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a [aria-label='Mostrar mais produtos']"))
        )

        print("A clicar no botão de mostrar mais...")
        driver.execute_script("arguments[0].click();", show_more_button)
        tts("Mostrando mais produtos.")
    except Exception as e:
        tts("Não foi possível mostrar mais produtos.")
        print(f"Erro ao mostrar mais produtos: {e}")
    
    return []

# FALTA AQUI O FINALIZAR A COMPRA

def finalize_order(tts):

    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Localiza o botão de finalizar a compra
        wait = WebDriverWait(driver, 15)
        checkout_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'cart-ingka-jumbo-btn--emphasised')]"))
        )

        print("A clicar no botão de finalizar a compra...")
        driver.execute_script("arguments[0].click();", checkout_button)


        print("A clicar no botão de confirmar a finalização da compra...")
        wait = WebDriverWait(driver, 15)
        confirm_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'cart-ingka-btn--emphasised')]"))
        )

        print("A clicar no botão de confirmar a compra...")
        driver.execute_script("arguments[0].click();", confirm_button)

        tts("A finalizar a compra.")
    except Exception as e:
        tts("Não foi possível finalizar a compra.")
        print(f"Erro ao finalizar a compra: {e}")
    
    return []

def main_page(tts):

    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        tts("O navegador não foi iniciado. Por favor, tente novamente.")
        return

    try:
        # Define a URL da página inicial
        homepage_url = "https://www.ikea.com/pt/pt/"  # Substitua pela URL desejada

        # Navega para a página inicial
        driver.get(homepage_url)
        print("Voltando à página inicial.")
        tts("A voltar à página inicial do site.")
    except Exception as e:
        tts("Não foi possível voltar à página inicial.")
        print(f"Erro ao voltar à página inicial: {e}")
    
    return []


def order_products(criterio, tts):

    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return
    
    try:

        print(f"Ordenando produtos por '{criterio}'...")
        wait = WebDriverWait(driver, 15)
        # Usando XPath com texto
        # all_filters_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Todos os filtros')]"))
        # )

        # Alternativa usando as classes
        all_filters_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Todos os filtros']]"))
        )

        print("A clicar no botão de todos os filtros...")
        driver.execute_script("arguments[0].click();", all_filters_button)


        # Localiza o botão de ordenar produtos
        wait = WebDriverWait(driver, 15)
        sort_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'plp-accordion__heading plp-accordion-item-header plp-accordion-item-header--large')]"))
        )

        print("A clicar no botão de ordenar produtos...")
        driver.execute_script("arguments[0].click();", sort_button)


        # Ajusta o critério para "Preço: mais elevado ao mais baixo" ou "Preço: mais baixo ao mais elevado"
        if criterio == "mais elevado ao mais baixo" or criterio == "do mais elevado ao mais baixo":
            criterio = "Preço: mais elevado ao mais baixo" 
        if criterio == "mais baixo ao mais elevado" or criterio == "do mais baixo ao mais elevado":
            criterio = "Preço: mais baixo ao mais elevado"
            
        # Localiza a opção de ordenação desejada

        if criterio == "Preço: mais elevado ao mais baixo":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[3]'))
            )
        
        if criterio == "Preço: mais baixo ao mais elevado":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[2]'))
            )

        if criterio == "Mais Recente":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[4]'))
            )
        
        if criterio == "Mais Populares":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[7]'))
            )

        if criterio == "Largura":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[8]'))
            )
        
        if criterio == "Altura":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[9]'))
            )

        if criterio == "Comprimento":
            sort_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="SEC_sort"]/div/div/fieldset/label[10]'))
            )
            

        print(f"A clicar na opção de ordenação por '{criterio}'...")
        driver.execute_script("arguments[0].click();", sort_option)


        print("A clicar no botão de ver!")

        ver_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[3]/div/div[3]/button[1]'))
        )

        driver.execute_script("arguments[0].click();", ver_button)

        tts(f"Os produtos foram ordenados por '{criterio}'.")

    except Exception as e:
        tts("Não foi possível ordenar os produtos.")
        print(f"Erro ao ordenar produtos: {e}")

import os

def ask_help(tts):
    """
    Opens a help HTML file in the same browser window controlled by the driver and provides help messages via TTS.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        tts("O navegador não foi inicializado. Não é possível exibir a ajuda.")
        return

    try:
        # Path to the HTML file
        help_file_path = os.path.join(os.getcwd(), "help", "help.html")  # Adjust the path as needed

        # Check if the file exists
        if not os.path.exists(help_file_path):
            raise FileNotFoundError(f"Help file not found at {help_file_path}")

        # Convert the file path to a file:// URL
        file_url = f"file://{help_file_path}"

        # Open the HTML file in the current browser window
        driver.get(file_url)

        # Provide an additional message via TTS
        tts("Abri o arquivo de ajuda no navegador. Confira as instruções exibidas.")
        print("Help file opened successfully in the current browser window.")

    except FileNotFoundError as fnf_error:
        tts("Desculpe, o arquivo de ajuda não foi encontrado.")
        print(fnf_error)

    except Exception as e:
        tts("Desculpe, houve um erro ao tentar fornecer ajuda.")
        print(f"Erro ao abrir o arquivo de ajuda: {e}")

## Funciona no produtos e nao nos outros
def move_selection_products(direction, tts):
    """
    Moves the selected area in the specified direction (up, down, left, right).

    Args:
        direction (str): The direction to move ("up", "down", "left", "right").
        tts (function): Text-to-speech function for feedback.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Inject CSS for highlighting if not already present
        driver.execute_script("""
            if (!document.querySelector('style#selection-style')) {
                const style = document.createElement('style');
                style.id = 'selection-style';
                style.type = 'text/css';
                style.innerHTML = `
                    .selected {
                        border: 2px solid red;
                        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
        """)

        # Execute JavaScript to move the selection
        driver.execute_script(f"""
            (function moveSelection() {{
                if (window.selectedDiv) {{
                    const selectedDiv = window.selectedDiv;
                    const productList = Array.from(document.querySelectorAll('div[data-testid="plp-product-card"]'));

                    if (productList.length === 0) {{
                        console.error("No products found on the page.");
                        return;
                    }}

                    // Calculate grid dimensions
                    const gridColumns = Math.max(1, Math.floor(window.innerWidth / selectedDiv.offsetWidth));
                    const index = productList.indexOf(selectedDiv);

                    let newIndex = -1;

                    if (index !== -1) {{
                        if ('{direction}' === 'left' && index % gridColumns !== 0) {{
                            // Move to the left
                            newIndex = index - 1;
                        }} else if ('{direction}' === 'right' && (index + 1) % gridColumns !== 0) {{
                            // Move to the right
                            newIndex = index + 1;
                        }} else if ('{direction}' === 'up' && index - gridColumns >= 0) {{
                            // Move up
                            newIndex = index - gridColumns;
                        }} else if ('{direction}' === 'down' && index + gridColumns < productList.length) {{
                            // Move down
                            newIndex = index + gridColumns;
                        }}

                        if (newIndex !== -1 && productList[newIndex]) {{
                            const newSelectedDiv = productList[newIndex];

                            // Update classes
                            selectedDiv.classList.remove('selected');
                            newSelectedDiv.classList.add('selected');

                            // Scroll into view
                            newSelectedDiv.scrollIntoView({{ behavior: "smooth", block: "center" }});

                            // Update global reference
                            window.selectedDiv = newSelectedDiv;
                        }} else {{
                            console.log("No valid movement for direction: {direction}");
                        }}
                    }}
                }} else {{
                    console.error("No selectedDiv found.");
                }}
            }})();
        """)
        print(f"Moved the selection {direction}.")

    except Exception as e:
        tts(f"Houve um problema ao mover para {direction}. Tente novamente.")
        print(f"Erro ao mover para {direction}: {e}")

## Funciona nos favoritos e nos outro nao
def move_selection_favorites(direction, tts):
    """
    Moves the selected area in the specified direction (up, down, left, right).

    Args:
        direction (str): The direction to move ("up", "down", "left", "right").
        tts (function): Text-to-speech function for feedback.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Inject CSS for highlighting if not already present
        driver.execute_script("""
            if (!document.querySelector('style#selection-style')) {
                const style = document.createElement('style');
                style.id = 'selection-style';
                style.type = 'text/css';
                style.innerHTML = `
                    .selected {
                        border: 2px solid red;
                        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
        """)

        # Execute JavaScript to move the selection
        driver.execute_script(f"""
            (function moveSelection() {{
                if (window.selectedDiv) {{
                    const selectedDiv = window.selectedDiv;

                    // Determine the container and product list
                    const container = document.querySelector('ul.ProductList_marginBottom__s_0MQ') || 
                                      document.querySelector('div[data-testid="product-list"]') || 
                                      document.querySelector('div._product_j61sc_1');

                    if (!container) {{
                        console.error("No valid product container found.");
                        return;
                    }}

                    // Gather all product items in the container
                    const productList = Array.from(container.querySelectorAll('.ProductCard_listProductCard__sr7fg, ._product_j61sc_1'));
                    
                    if (productList.length === 0) {{
                        console.error("No products found in the container.");
                        return;
                    }}

                    // Get the index of the currently selected div
                    const index = productList.indexOf(selectedDiv);

                    if (index === -1) {{
                        console.error("Selected div not found in the product list.");
                        return;
                    }}

                    let newIndex = -1;

                    // Determine the new index based on the direction
                    if ('{direction}' === 'up' && index > 0) {{
                        newIndex = index - 1;
                    }} else if ('{direction}' === 'down' && index < productList.length - 1) {{
                        newIndex = index + 1;
                    }} else if ('{direction}' === 'left' && index > 0) {{
                        newIndex = index - 1;
                    }} else if ('{direction}' === 'right' && index < productList.length - 1) {{
                        newIndex = index + 1;
                    }}

                    if (newIndex !== -1) {{
                        const newSelectedDiv = productList[newIndex];

                        // Update classes
                        selectedDiv.classList.remove('selected');
                        newSelectedDiv.classList.add('selected');

                        // Scroll into view
                        newSelectedDiv.scrollIntoView({{ behavior: "smooth", block: "center" }});

                        // Update global reference
                        window.selectedDiv = newSelectedDiv;
                    }} else {{
                        console.log("No valid movement for direction: {direction}");
                    }}
                }} else {{
                    console.error("No selectedDiv found.");
                }}
            }})();
        """)
        print(f"Moved the selection {direction}.")
    except Exception as e:
        tts(f"Houve um problema ao mover para {direction}. Tente novamente.")
        print(f"Erro ao mover para {direction}: {e}")


def select(tts):
    """
    Selects the product name link or span within the currently highlighted product or item.

    Args:
        tts (function): Text-to-speech function for feedback.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Locate and click the target span or link within the selected product
        clicked = driver.execute_script("""
            if (window.selectedDiv) {
                const selectedDiv = window.selectedDiv;

                // List of selectors to identify the target element
                const selectors = [
                    'span.cart-ingka-price-module__name-decorator > a',
                    'span.plp-price-module__name-decorator > span',
                    'span.list-ingka-price-module__name-decorator > a'
                ];

                let targetElement = null;

                // Loop through selectors to find a matching element
                for (const selector of selectors) {
                    targetElement = selectedDiv.querySelector(selector);
                    if (targetElement) break;
                }

                if (targetElement) {
                    // Log the found element for debugging
                    console.log("Target element found:", targetElement);

                    targetElement.click();
                    return true; // Indicate success
                } else {
                    console.error("Target element not found inside the selected product div.");
                    return false; // Indicate failure
                }
            } else {
                console.error("No selectedDiv found.");
                return false; // Indicate failure
            }
        """)

        if clicked:
            tts("O produto foi selecionado.")
            print("The product has been selected.")
        else:
            tts("Não foi possível encontrar o nome do produto para selecionar.")
            print("Product name element not found.")
    except Exception as e:
        tts("Não foi possível selecionar o produto.")
        print(f"Erro ao selecionar o produto: {e}")


def remove(tts):
    """
    Removes the currently highlighted product by clicking the associated decrement or trash button.

    Args:
        tts (function): Text-to-speech function for feedback.
    """
    global driver
    if driver is None:
        print("Driver não foi inicializado.")
        return

    try:
        # Execute JavaScript to locate and click the decrement or trash button for the selected product
        removed = driver.execute_script("""
            if (window.selectedDiv) {
                const selectedDiv = window.selectedDiv;

                // Log the selectedDiv for debugging
                console.log("Selected div:", selectedDiv);

                // Attempt to find the decrement or trash button within the selected product
                const removeButtons = [
                    'button.cart-ingka-btn--icon-tertiary.cart-ingka-quantity-stepper__decrease',
                    'button.list-ingka-btn--icon-tertiary.list-ingka-quantity-stepper__decrease'
                ];
                let trashButton = null;

                // Loop through selectors to find the button
                for (const selector of removeButtons) {
                    trashButton = selectedDiv.querySelector(selector);
                    if (trashButton) break;
                }

                if (trashButton) {
                    // Log the found button for debugging
                    console.log("Remove button found:", trashButton);

                    trashButton.click();
                    return true;  // Indicate success
                } else {
                    console.error("Remove button not found inside the selected product div.");
                    return false;  // Indicate failure
                }
            } else {
                console.error("No selectedDiv found.");
                return false;  // Indicate failure
            }
        """)

        if removed:
            tts("O produto foi removido.")
            print("The product has been removed.")
        else:
            tts("Não foi possível encontrar o botão de remoção.")
            print("Remove button not found.")
    except Exception as e:
        tts("Não foi possível remover o produto.")
        print(f"Erro ao remover o produto: {e}")



    
async def voice_message_handler(message, tts):
    # Processa a mensagem e extrai o intent
    
    print(f"Message: {message}")

    if message['recognized'][1]:
        intent = message['recognized'][1]
        print(f"Intent: {intent}")
    

    if message == "OK":
        return "OK"
    
    elif intent in intents_list:

        if intent == "ASK_HELP":
            print("Pedindo ajuda...")
            ask_help(tts)
        
        if intent == "OPEN_WEBSITE":
            print("Abrindo o site...")
            tts("A abrir o site da IKEA!")
            open_website()

        elif intent == "SHOW_FAVORITES":
            print("A abrir os favoritos...")
            open_favourites(tts)

        elif intent == "SHOW_CART":
            print("A abrir ao carrinho...")
            open_cart(tts)

        elif intent == "ADD_TO_CART":
            print("A adicionar ao carrinho...")
            add_to_cart(tts)

        elif intent == "ADD_TO_FAVORITES":
            print("A adicionar aos favoritos...")
            add_to_favorites(tts)

        elif intent == "SHOW_PRODUCTS":
            category = message['recognized'][2]
            print(f"Mostrando produtos de {category} ...")
            show_product(category, tts)
        
        elif intent == "SCROLL_DOWN":
            print("A descer a pagina")
            tts("A descer a página")
            scroll_down()

        elif intent == "SCROLL_UP":
            print("A subir a pagina")
            tts("A subir a página")
            scroll_up()
        
        elif intent == "GO_BACK":
            print("A voltar para trás")
            go_back(tts)
        
        elif intent == "SHOW_MORE":
            print("A mostrar mais produtos")
            show_more(tts)

        elif intent == "FINALIZE_ORDER":
            print("A finalizar a compra")
            finalize_order(tts)

        elif intent == "ORDER_PRODUCTS":
            criterio = message['recognized'][2]
            print(f"Ordenando produtos por {criterio}")
            order_products(criterio, tts)

        else:
            print(f"Intent não reconhecido: {intent}")
            tts("Por favor repita o comando!")

async def gestures_message_handler(message, tts):
    
    print(f"Message: {message}")

    if message['recognized'][1]:
        intent = message['recognized'][1]
        print(f"Intent: {intent}")
    

    if message == "OK":
        return "OK"

    elif intent in intents_list:

        if intent == "SCROLL_DOWN":
            print("A descer a pagina")
            tts("A descer a página")
            scroll_down()
        
        elif intent == "SCROLL_UP":
            print("A subir a pagina")
            tts("A subir a página")
            scroll_up()

        elif intent == "GO_BACK":
            print("A voltar para trás")
            go_back(tts)

        elif intent == "MAIN_PAGE":
            print("Voltar à Página Inicial")
            main_page(tts)
        
        elif intent == "GO_UP":
            print("A Mover Área Selecionada para Cima")

            # Check the URL and call the appropriate function
            current_url = driver.current_url.lower()

            print(f"Current URL: {current_url}")

            if "search" in current_url or "products" in current_url:
                # If the URL indicates a search or products page
                move_selection_products("up", tts)
            elif "favourites" in current_url or "favorites" in current_url:
                # If the URL indicates a favorites page
                move_selection_favorites("up", tts)
            else:
                print("Página desconhecida. Nenhuma ação realizada.")
                tts("Não foi possível determinar a página para mover para cima.")
        
        elif intent == "GO_DOWN":
            print("A Mover Area Selecionada para Baixo")
            
            # Check the URL and call the appropriate function
            current_url = driver.current_url.lower()

            print(f"Current URL: {current_url}")

            if "search" in current_url or "products" in current_url:
                # If the URL indicates a search or products page
                move_selection_products("down", tts)
            elif "favourites" in current_url or "favorites" in current_url:
                # If the URL indicates a favorites page
                move_selection_favorites("down", tts)
            else:
                print("Página desconhecida. Nenhuma ação realizada.")
                tts("Não foi possível determinar a página para mover para baixo.")

        elif intent == "GO_LEFT":
            print("A Mover Area Selecionada para Left")
            # Check the URL and call the appropriate function
            current_url = driver.current_url.lower()

            print(f"Current URL: {current_url}")

            if "search" in current_url or "products" in current_url:
                # If the URL indicates a search or products page
                move_selection_products("left", tts)
            elif "favourites" in current_url or "favorites" in current_url:
                # If the URL indicates a favorites page
                move_selection_favorites("left", tts)
            else:
                print("Página desconhecida. Nenhuma ação realizada.")
                tts("Não foi possível determinar a página para mover para baixo.")

        elif intent == "GO_RIGHT":
            print("A Mover Area Selecionada para Right")
            # Check the URL and call the appropriate function
            current_url = driver.current_url.lower()

            print(f"Current URL: {current_url}")

            if "search" in current_url or "products" in current_url:
                # If the URL indicates a search or products page
                move_selection_products("right", tts)
            elif "favourites" in current_url or "favorites" in current_url:
                # If the URL indicates a favorites page
                move_selection_favorites("right", tts)
            else:
                print("Página desconhecida. Nenhuma ação realizada.")
                tts("Não foi possível determinar a página para mover para baixo.")

        elif intent == "EXIT":
            print("A Fechar o Navegador")
            close_driver(tts)

        else:
            print(f"Intent não reconhecido: {intent}")
            tts("Por favor repita o comando!")


async def fusion_message_handler(message, tts):
    
    print(f"Message: {message}")

    if message['recognized'][1]:
        intent = message['recognized'][1]
        print(f"Intent: {intent}")
    

    if message == "OK":
        return "OK"

    elif intent in intents_list:

        if intent == "SCROLL_DOWN":
            print("A descer a pagina")
            tts("A descer a página")
            scroll_down()
        
        elif intent == "SCROLL_UP":
            print("A subir a pagina")
            tts("A subir a página")
            scroll_up()

        elif intent == "GO_BACK":
            print("A voltar para trás")
            go_back(tts)
        
        elif intent == "MAIN_PAGE":
            print("Voltar à Página Inicial")
            main_page(tts)

        elif intent == "SELECT":
            print("Selecionar")
            select(tts)

        elif intent == "REMOVE":
            print("Remover")
            remove(tts)
    
        else:
            print(f"Intent não reconhecido: {intent}")
            tts("Por favor repita o comando!")

async def message_handler(message:str, tts):
    
    message, status = process_message(message)
    
    if message == "OK" and status == None:
        return "OK"
    
    elif status == "voice":
        print(f"Voice command received: {message}")
        await voice_message_handler(message, tts)

    elif status == "gesture":
        print(f"Gesture command received: {message}")
        await gestures_message_handler(message, tts)

    elif status == "fusion":
        await fusion_message_handler(message, tts)

    else:
        return "OK"

def process_message(message):
    if message == "OK":
        return "OK", None
    else:
        json_command = ET.fromstring(message).find(".//command").text
        if "recognized" in json_command:
            recognized = json.loads(json_command)["recognized"]
            modalidade = recognized[0]
            
            if "GESTURES" == modalidade:
                gesture = json.loads(json_command)
                return gesture, "gesture"
            elif "SPEECH" == modalidade:
                command = json.loads(json_command)
                return command, "voice"
            elif "FUSION" == modalidade:
                command = json.loads(json_command)
                return command, "fusion"    
            else:
                print("Not recognized")
                print(f"Modalities: {modalidade}")
                return "OK", None
        else:
            return "OK", None

async def main():
    tts = TTS(FusionAdd="https://127.0.0.1:8000/IM/USER1/APPSHEECH").sendToVoice
    mmi_client_out_add = "wss://127.0.0.1:8005/IM/USER1/APP"

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(mmi_client_out_add, ssl=ssl_context) as websocket:

        print("Connected to MMI Client")

        while not_quit: 
            try:
                msg = await websocket.recv()
                print(f"Received message: {msg}")
                await message_handler(message=msg, tts=tts)
            except Exception as e:
                tts("Por Favor repita o comando!")
                print(f"Error: {e}")
        
        print("Closing connection")
        await websocket.close()
        print("Connection closed")
        exit(0)

if __name__ == "__main__":
    asyncio.run(main())
