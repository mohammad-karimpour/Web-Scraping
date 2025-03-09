# https://www.crummy.com/software/BeautifulSoup/bs4/doc/    مستندات

import csv
import requests
from bs4 import BeautifulSoup

# آدرس مد نظر
url = "https://arbabacamp.com/allproducts/"

# گرفتن از صفحه
response = requests.get(url)


# بررسی موفقیت درخواست
if response.status_code == 200:
    # گرفتن داده ها از صفحه
    page_content = response.text
    
    # اسکرپینگ صفحه
    soup = BeautifulSoup(page_content, "html.parser")
    # print(soup.prettify()) چاپ زیبا

    P_L = [['نام محصول','قیمت']]

    product_list = soup.find_all("div", class_="titleAndtext")
    for I in product_list:
        title = I.find("p", class_="text-dark")
        price = I.find('button')
        print(title.text + '|' + price.text)
        print('--------------------------------')

        P_L.append([title.text,price.text])

    # ساخت فایل CSV
    with open("data.csv", mode="w", newline="", encoding="utf-8") as file:
         writer = csv.writer(file)
         writer.writerows(P_L)    

else:
    print("خطا در دریافت صفحه")

