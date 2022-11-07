from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

link = "https://www.airbnb.co.id/s/Yogyakarta--Indonesia/homes"
driver.set_window_size(1300,800)
driver.get(link)

time.sleep(5)
driver.save_screenshot("home.png")
content = driver.page_source
driver.quit()

data = BeautifulSoup(content,'html.parser')
#print(data.encode("utf-8"))

list_nama,list_location,list_harga,list_link,list_rating,list_desc=[],[],[],[],[],[]

i = 1

for area in data.find_all('div',class_="c1l1h97y dir dir-ltr"):
    print('proses data ke-'+str(i))
    
    harga = area.find('span',class_="a8jt5op dir dir-ltr").get_text()
    linknext = "https://www.airbnb.co.id" + area.find('a',class_="ln2bl2p dir dir-ltr")['href']

    driver = webdriver.Chrome(service=servis, options=opsi)
    driver.set_window_size(1300,800)
    driver.get(linknext)
    time.sleep(5)
    content = driver.page_source
    driver.quit()

    data2 = BeautifulSoup(content,'html.parser')
    nama = data2.select('h1._fecoyn4')[0].text.strip()
    location = data2.find('span',class_="_9xiloll").get_text()
    desc = data2.find('div',class_="d1isfkwk dir dir-ltr")
    if desc != None:
        desc = desc.get_text()
    rating = data2.find('span',class_="_12si43g")
    if rating != None:
        rating = rating.get_text()
    print(nama)
    print(location)
    print(harga)
    print(rating)
    print(desc)
    print("-----------")

    list_nama.append(nama)
    list_location.append(location)
    list_harga.append(harga)
    list_link.append(link)
    list_rating.append(rating)
    list_desc.append(desc)

    i+=1
    
df = pd.DataFrame({'Nama':list_nama,'Lokasi':list_location,'Harga':list_harga,'Link':list_link,'Rating':list_rating,'Deskripsi':list_desc})
writer = pd.ExcelWriter('Homestay Jogja Airbnb.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()
