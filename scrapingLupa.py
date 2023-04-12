import requests
from bs4 import BeautifulSoup
import csv

url = 'https://soysuper.com/c?page=1#products'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('li', {'data-pid': True})

# abrir archivo csv en modo escritura
with open('Productos.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    # escribir encabezados de las columnas
    writer.writerow(['Name', 'Brand', 'Price', 'Currency', 'Price per unit'])

    for product in products:
        name = product.find('span', {'class': 'productname'}).text.strip()
        brand = product.find('span', {'class': 'brand'})
        if brand is not None:
            brand = brand.text.strip()
        else:
            brand = ""
        price = product.find('meta', {'itemprop': 'price'})['content']
        currency = product.find('meta', {'itemprop': 'priceCurrency'})['content']
        price_unit = product.find('span', {'class': 'unitprice'})
        if price_unit is not None:
            price_unit = price_unit.text.strip()
        else:
            price_unit = ""

        # escribir fila en el archivo csv
        writer.writerow([name, brand, price, currency, price_unit])

        print('Name:', name)
        print('Brand:', brand)
        print('Price:', price, currency)
        print('Price per unit:', price_unit)
        print('-----------------------')

print('Resultados guardados en Productos.csv')
