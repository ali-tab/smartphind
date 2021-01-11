import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import pygubu
import os

class product:

    def __init__(self, provider, name, price, mprice):
        self.provider = provider
        self.name = name
        self.price = price
        self.mprice = mprice

    def getName(self):
        return name

    def getPrice(self):
        return price

    def getmprice(self):
        return mprice

    def getprovider(self):
        return provider

    def __str__(self):
        return self.provider + " - " + self.name + " for " + str(self.price) + " or " + self.mprice

    def __repr__(self):
        return self.name

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "appgui.ui")

class TestingApp:

    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'smartphind')
        img_path = os.path.abspath(img_path)
        builder.add_resource_path(img_path)

        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

        self.applebutton = self.builder.get_object('applebutton')
        self.samsbutton = self.builder.get_object('samsbutton')

        self.searchbutton = self.builder.get_object('searchbutton')

        self.phonelist = self.builder.get_object('phonelist')
        self.searchlist = self.builder.get_object('searchlist')

        self.add = self.builder.get_object('moveright')
        self.remove = self.builder.get_object('moveleft')

        self.bellcheck = self.builder.get_variable("bellcheck")
        self.telcheck = self.builder.get_variable("telcheck")

        self.searchbutton['state'] = tk.DISABLED

        self.results = self.builder.get_object('results')

        self.avail_label = self.builder.get_object("avail_label")

        self.status = self.builder.get_object("statuslabel")
        self.progress = self.builder.get_object("progressbar")

    def on_apple_click(self):

        self.phonelist.delete(0, tk.END)
        self.searchlist.delete(0, tk.END)

        self.applebutton['state'] = tk.DISABLED
        self.samsbutton['state'] = tk.NORMAL
        
        self.searchbutton['state'] = tk.NORMAL
        

        iphoneList = []

        AppleURL = "https://www.apple.com/ca/iphone/"
        Apage = requests.get(AppleURL)
        soup = BeautifulSoup(Apage.content, "html.parser")
        products = soup.find("ul", class_="chapternav-items")
        
        for i in products.find_all("li"):
        
            tobeadded = i.find("span").string
            if (tobeadded) == "Compare":
                break
            
            if i.find("span").string == None:
            
                tobeadded = ""
                for j in range(len(i.find("span").contents)):
                
                    tobeadded += i.find("span").contents[j].string

            tobeadded = tobeadded.replace(u'\xa0', u' ')

            iphoneList.append(tobeadded)

        self.avail_label["text"] = "Apple has " + str(len(iphoneList)) + " new models on their website." 

        for i in range(len(iphoneList)):
            self.phonelist.insert(tk.END, iphoneList[i])


    def on_samsung_click(self):

        self.phonelist.delete(0, tk.END)
        self.searchlist.delete(0, tk.END)

        self.samsbutton['state'] = tk.DISABLED
        self.applebutton['state'] = tk.NORMAL

        self.searchbutton['state'] = tk.NORMAL

        samsungList = []

        samsungURL = "https://www.samsung.com/ca/smartphones/"
        page = requests.get(samsungURL)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.find("div", class_="explore-lnb__link-container mb")

        for i in products.find_all("a"):
        
            tobeadded = i.contents[1].string
            samsungList.append(tobeadded)

        self.avail_label["text"] = "Samsung has " + str(len(samsungList)) + " new models on their website." 

        for i in range(len(samsungList)):
            self.phonelist.insert(tk.END, samsungList[i])

    def on_add_click(self):

        tobemoved = self.phonelist.curselection()
        
        for i in tobemoved:

            selectedphones = self.phonelist.get(i)
            insearch = self.searchlist.get(0, tk.END)
            if selectedphones not in insearch:
                self.searchlist.insert(0, selectedphones)

    def on_remove_click(self):

        tobemoved = self.searchlist.curselection()

        for i in reversed(tobemoved):

            self.searchlist.delete(i)

    def updateStatus(self):

        self.status["text"] = "Searching..." 
        self.progress['value'] = 0

    def on_search_click(self):

        self.results.delete(0, tk.END)

        if (self.searchlist.size() == 0):

            self.results.insert(tk.END, "No models were entered for search.")

            return

        if (self.bellcheck.get() == False and self.telcheck.get() == False):
            
            self.results.insert(tk.END, "No providers were selected for search.")

            return


        self.updateStatus()

        self.mainwindow.update_idletasks()

        if self.bellcheck.get() == True:

            idstring = "dl-list-"

            BellURL = "https://www.bell.ca/Mobility/Smartphones_and_mobile_internet_devices?filter="

            if str(self.applebutton['state']) == 'disabled':
                
                BellURL = BellURL + "Apple_Brand"

                idstring = idstring + "apple"

            if str(self.samsbutton['state']) == 'disabled':

                BellURL = BellURL + "Samsung_Brand"
                idstring = idstring + "samsung"

            Bpage = requests.get(BellURL)
    
            soup = BeautifulSoup(Bpage.content, "html.parser")
    
            bellproducts = soup.find("div", id=idstring)

            bell_list = []

            for i in bellproducts.find_all("div", class_= "dl-tile-content"):
            
                name = i.find("div", class_= "dl-tile-name").string

                price = i.find("span", class_= "qc").string.strip()

                #print(price)

                mprice = i.find("div", class_= "dl-tile-price-month").find("div", class_="dl-tile-price").string

                bell_list.append(product("Bell", name, price, mprice))

            for i in range(self.searchlist.size()):

                inresults = self.results.get(0, tk.END)

                for j in range(len(bell_list)):

                    if self.searchlist.get(i) in bell_list[j].name and str(bell_list[j]) not in inresults:
    
                        self.results.insert(tk.END, bell_list[j])

        self.progress['value'] = 50

        if self.telcheck.get() == True:

            chrome_options = Options()
            chrome_options.add_argument("--headless")

            DRIVER_PATH = 'chromedriver/chromedriver.exe'
            driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

            driver.get('https://www.telus.com/en/mobility/phones/brand')

            idstring = "brand-section-"

            if str(self.applebutton['state']) == 'disabled':
                
                xpath = '//*[@id="brand-section-apple"]/div[1]/div[3]/div/div/button'

                idstring = idstring + "apple"

            if str(self.samsbutton['state']) == 'disabled':

                xpath = '//*[@id="brand-section-samsung"]/div[1]/div[3]/div/div/button'

                idstring = idstring + "samsung"

            driver.find_element_by_xpath(xpath).click()
            Tpage = driver.page_source

            soup = BeautifulSoup(Tpage, "html.parser")

            driver.close()

            telproducts = soup.find("div", id=idstring)

            telus_list = []

            for i in telproducts.find_all("div", class_="styledComponents__DeviceDetailsWrapper-sc-1ujtfbp-3 cyboSx"):

                name = (i.find("a").string)

                price = i.find("span", class_="styledComponents__StyledPriceDigits-alblfz-5 gtRPyG").string
                
                price = price[price.index("$"):]

                mpricearr = i.find("span", class_="sc-iAyFgw amount hKCZrQ")

                mprice = "$" + mpricearr.contents[0] + mpricearr.find("span").contents[0] + "/mo."

                telus_list.append(product("Telus", name, price, mprice))

            for i in range(self.searchlist.size()):

                inresults = self.results.get(0, tk.END)

                for j in range(len(telus_list)):

                    if self.searchlist.get(i) in telus_list[j].name and str(telus_list[j]) not in inresults:
    
                        self.results.insert(tk.END, telus_list[j])

        self.progress['value'] = 100
        self.status["text"] = "Finished!" 

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':

    import tkinter as tk
    root = tk.Tk()
    root.geometry("600x700")
    root.resizable(False,False)
    app = TestingApp()
    app.run()

