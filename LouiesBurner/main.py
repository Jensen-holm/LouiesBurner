import requests
from bs4 import BeautifulSoup

# URL = '/'.join([VOLLEYBALL_ROOT_URL, "stats", "2024"])
URL: str = "https://gvsulakers.com/sports/womens-volleyball/stats/2024"

page: str = requests.get(URL)                               

html_soup: str = BeautifulSoup(page.text, "html.parser")    #parses the html 

results = html_soup.find_all('td')          #looks for table data element 

for data in results:        
    print(data.text)        #prints all table data 

