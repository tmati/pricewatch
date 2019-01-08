from lxml import html
import requests
import csv
import datetime
import matplotlib.pyplot as plotting
plotting.style.use(['dark_background', 'presentation'])


#timestamp
def getDate():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y")
    print (timestamp)
    return timestamp


#get value of price html tag content
def getPrice(url, priceTag, nameTag):
    
    page = requests.get(url)
    tree = html.fromstring(page.content)

    price = tree.xpath(priceTag)
    name = tree.xpath(nameTag)

    print (name[0] + " " + price[0] + " €")

    return int(price[0])


#save price values and timestamp to CSV file
def saveIntoCSV(price, altPrice, filename):
    #newline param to not allow blank lines
    with open(str(filename)+'.csv', mode='a', newline='') as priceData:
        priceWriter = csv.writer(priceData, delimiter=',' , quotechar='"')
        priceWriter.writerow([getDate(), price, altPrice])
        print ("Yhteishinta tallennettu CSV-tiedostoon.")
        return;


#reading CSV prices
def readCSV(filename):
    print ("Luetaan hintahistoria CSV-tiedostosta.")
    with open(str(filename)+'.csv', mode='r') as priceData:
        csvReader = csv.reader(priceData, delimiter= ',')
        rows = 0
        for row in csvReader:
            print(row[0] + "| Kokonaishinta : " + row[1] + "€, hinta ilman näytönohjainta: " + row[2] + "€");
            rows += 1
        print("Käyty läpi "+ str(rows) + " merkintää.")
        return
            


#get prices for the items you want. Use browser console to determine the HTML tag where the price is shown.
def getVkPrices(filename):
    #verkkokauppa.com prices
    
    #Processor
    procPrice = getPrice('https://www.verkkokauppa.com/fi/product/4215/knqnq/Intel-Core-i5-9600K-3-7-GHz-LGA1151-suoritin', '//span[@class="price-tag-price__euros"]/text()', '//h1[@class="heading-page product__name-title"]/text()');
    print (" ")
    
    #Motherboard
    moboPrice = getPrice('https://www.verkkokauppa.com/fi/product/63886/kqkqd/Asus-PRIME-Z390M-PLUS-Intel-Z390-LGA1151-mATX-emolevy', '//span[@class="price-tag-price__euros"]/text()' , '//h1[@class="heading-page product__name-title"]/text()');
    print (" ")
    
    #GPU
    gpuPrice = getPrice('https://www.verkkokauppa.com/fi/product/66968/jqjrm/MSI-GeForce-GTX-1070-Ti-ARMOR-8G-naytonohjain-PCI-e-vaylaan', '//span[@class="price-tag-price__euros"]/text()', '//h1[@class="heading-page product__name-title"]/text()');
    print (" ")
    
    #RAM
    ramPrice = getPrice('https://www.verkkokauppa.com/fi/product/30793/ktxnx/Kingston-HyperX-FURY-DDR4-3200-MHz-CL18-16-Gt-muistimodulipa', '//span[@class="price-tag-price__euros"]/text()', '//h1[@class="heading-page product__name-title"]/text()');
    print (" ")

    #Grand total
    total = (procPrice + moboPrice + gpuPrice + ramPrice)
    totalWoGPU = (procPrice + moboPrice + ramPrice)
    print("=========================================================================");
    print ("Yhteishinta verkkokauppa.comista tilattuna: "+ str(total) + " € + toimitus");
    print ("Ilman näytönohjainta: "+ str(totalWoGPU) + " € + toimitus")
    print("=========================================================================");
    saveIntoCSV(total, totalWoGPU, filename)
    return

def makePlot(filename):
    date = []
    totalprice = []
    nonGpuPrice = []

    with open(str(filename)+'.csv', mode='r') as priceData:
        csvReader = csv.reader(priceData, delimiter= ',')
        for row in csvReader:
            date.append(row[0]);
            totalprice.append(int(row[1]))
            nonGpuPrice.append(int(row[2]))

    plotting.plot(date,totalprice, label='Total price')
    plotting.plot(date,nonGpuPrice, label='Price without GPU')
    plotting.xlabel('PVM')
    plotting.ylabel('€')
    plotting.title('Verkkokauppa.com hintakehitys')
    plotting.ylim(400, 1500)
    plotting.legend()
    plotting.show()
    return
  
getVkPrices('pricedata')
readCSV('pricedata')
makePlot('pricedata')

#the price element VERKKOKAUPPA.COM
#'//span[@class="price-tag-price__euros"]/text()'
#product name tag VERKKOKAUPPA.COM
#'//h1[@class="heading-page product__name-title"]/text()'


