from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import bitly_api

#API keys for Bitly
API_USER = "..."
API_KEY = "..."
bitly = bitly_api.Connection(API_USER, API_KEY)


base_url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description="

#Prompts user for the desired product
keyword = input("Enter the keyword you want to search for on Newegg: ")

#Combines product and base url
my_url = base_url + keyword

#Opening up connecting to page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#HTML parsing
page_soup = soup(page_html, "html.parser")

temp = page_soup.find("div",{"class":"items-view is-grid"})

#Grabs each Newegg product
containers = temp.findAll("div",{"class":"item-container"})

#Creates new csv file named with keyword
filename = keyword + ".csv"
#Writes to file
f = open(filename, 'w')

#Creates headers for csv file
headers = "Product Link, Product Name, Price, Shipping\n"

f.write(headers)

#Inserts data in spreadsheet
for container in containers:
    #Grabs product link
    product_link = container.a["href"]
    
    #Grabs product name
    product_name = container.img["title"]
    
    #Grabs product price
    price = container.find("li",{"class":"price-current"}).text.split()
    
    if price == []:
        price = "See price in cart."
    else:
        price = price[1]
    
    #Grabs shipping cost
    shipping_container = container.find("li", {"class":"price-ship"})
    shipping = shipping_container.text.strip()
    
    #Shortens the product link using Bitly API
    short_url = bitly.shorten(product_link)['url']
    print(short_url)
  
    print(product_name)
    print(price)
    print(shipping)
    print("")
    
    f.write(short_url + ", " + product_name.replace(",", "|") + ", " + price + ", " + shipping + "\n")
    
f.close()
    
