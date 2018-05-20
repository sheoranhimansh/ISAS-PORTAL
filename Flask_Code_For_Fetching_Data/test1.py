import requests
url = 'http://courses.iiit.ac.in/EdgeNet/archives.php'
headers = {'Cookie': '_ga=GA1.3.1976699568.1485781562; PHPSESSID=ST-11556-CyiU5gLrWqP7Wku4jkKE-loginiiitacin'}
 
r = requests.get(url,headers=headers)
r = r.content

from bs4 import BeautifulSoup
parsed_html = BeautifulSoup(r)

r = parsed_html.findAll('table')[2].findAll('tr')

for i in range(0,len(r)):
	for j in range(0,5):
		print(r[i].findAll('td')[j].findAll('font')[0].text)
	
