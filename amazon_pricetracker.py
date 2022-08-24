import requests
import matplotlib.dates as mdates
import time

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt


def page_content(url, HEADERS):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    return soup


def main(url, zeitperiode):
    # Scraping Code: https://www.geeksforgeeks.org/scraping-amazon-product-information-using-beautiful-soup/

    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})

    try:
        title = page_content(url, HEADERS).find("span",
                                                attrs={"id": 'productTitle'})
        title_value = title.string
        TITLE_STRING = title_value.strip().replace(',', '')
    except AttributeError:
        TITLE_STRING = "NA"

    listX = []
    listY = []

    plt.clf()

    while datetime.now() < ende:

        try:
            price = page_content(url, HEADERS).find(
                "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '.').replace('€', '')
        except AttributeError:
            price = "NA"

        listX.append(datetime.now().strftime("%d.%m.%y %H:%M:%S"))
        print("[Date] " + datetime.now().strftime("%d.%m.%y %H:%M:%S") + " | [Price] " + price)
        try:
            listY.append(float(price))
        except ValueError:
            pass

        time.sleep(zeitperiode * 60)

    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.title(TITLE_STRING, fontsize=10)

    plt.plot(listX, listY)  # Blaue Linie
    plt.plot(listX, listY, 'ro')  # Rote Punkte

    plt.gcf().autofmt_xdate()

    plt.savefig(TITLE_STRING.replace('/', '_'), bbox_inches='tight')


if __name__ == '__main__':

    print("""\
██████╗ ██████╗ ██╗ ██████╗███████╗████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║██║     █████╗     ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██╗██║██║     ██╔══╝     ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║██║╚██████╗███████╗   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                       
    """)

    tage = input("Wie lange soll der Preis verfolgt werden?[in Tage]: ")
    zeitperiode = input("In was für Zeitabständen soll der Preis gespeichert werden?[in Minuten]: ")

    ende = datetime.now() + timedelta(days=int(tage))

    print("\nDer Preis wird bis zum " + ende.strftime("%d.%m.%y %H:%M:%S") + " verfolgt")

    file = open("url.txt", "r")
    for links in file.readlines():
        main(links, int(zeitperiode))
