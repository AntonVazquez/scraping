import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define la cabecera HTTP adicional para indicar que nuestra solicitud proviene de un navegador web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Realiza la solicitud HTTP a la página de productos de Eroski con la cabecera definida
url = 'https://soysuper.com/c?page=1#products'
response = requests.get(url, headers=headers)

# Analiza el código HTML utilizando BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Encuentra todos los elementos de productos utilizando su clase
product_divs = soup.find_all('div', class_='conteiner')

# Inicializa las listas para almacenar los datos de cada producto
product_names = []
product_prices = []
product_priceCurrency = []
product_unitprice = []

# Extrae los datos de cada producto y los agrega a las listas
for product_div in product_divs:
    product_name = product_div.find('span', class_='productname', itemprop='name').text
    product_price = product_div.find('span', class_='price').text.strip()
    product_priceCurrency = product_div.find('meta', itemprop='priceCurrency')['content']
    product_unitprice = product_div.find('span', class_='product-unitprice').text.strip()
    product_names.append(product_name)
    product_prices.append(product_price)
    product_priceCurrency.append(product_priceCurrency)
    product_unitprice.append(product_unitprice)

# Crea un DataFrame con los datos de los productos y lo guarda como un archivo CSV
data = {'name': product_names, 'price': product_prices, 'priceCurrency': product_priceCurrency, 'unitprice': product_unitprice}
df = pd.DataFrame(data)
df.to_csv('productos.csv', index=False)
