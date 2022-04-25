from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

#set browser options
options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')

#initialize browser
id = input("Enter profile link: ")
browser = webdriver.Chrome("chromedriver", options=options)

views = 0
favourites = 0
scores = 0
page = 1
while True:
    #open to sheet music page
    link = "{}/sheetmusic?page={}#main-content".format(id, page)
    browser.get(link)
    sleep(2) #load buffer
    html = str(browser.page_source)

    #check if page has no sheet music (page after last page)
    try:
        test = html[html.index("_1Tg_p MFWvy"):html.rfind("</nav>")].split('favorite')
    except:
        break
    else:
        html = html[html.index("_1Tg_p MFWvy"):html.rfind("</nav>")].split('favorite')
    for i in html: #get data from each score
        if i.rfind("part") == -1 or i.rfind(" • ") == -1:
            continue
        data = i[i.rfind("part"):]
        data = data.split(sep=" • ")
        try:
            test = int(data[-2].replace(",", "").replace(" views", ""))
        except:
            continue
        else:
            v = int(data[-2].replace(",", "").replace(" views", ""))
        views += v
        scores += 1
        favourites += int(data[-1].replace(" ", "").replace(",", ""))
    page += 1

print("User:\t\t\t\t\t\t{}".format(id))
print("Scores counted:\t\t\t\t\t{}".format(scores))
print("Views:\t\t\t\t\t\t\t".format(views))
print("Average views per score:\t\t{:,}".format(round(views/scores, 1)))
print("Favourites:\t\t\t\t\t{:,}".format(favourites))
print("Average favourites per score:\t{:,}".format(round(favourites/scores, 1)))
print("View-to-favourites ratio:\t\t", round(views/favourites, 1))
