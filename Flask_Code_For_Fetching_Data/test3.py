import requests
url = 'http://courses.iiit.ac.in/EdgeNet/archives.php'
headers = {'Cookie': '_ga=GA1.3.1976699568.1485781562; PHPSESSID=ST-11556-CyiU5gLrWqP7Wku4jkKE-loginiiitacin'}
 
r = requests.get(url,headers=headers)
r = r.content

from bs4 import BeautifulSoup
parsed_html = BeautifulSoup(r)

r = parsed_html.findAll('table')[2] 

for i in r.findAll('a', href =True):
	t = i['href']
	url = 'http://courses.iiit.ac.in/EdgeNet/'+t
	headers = {'Cookie': '_ga=GA1.3.1976699568.1485781562; PHPSESSID=ST-11556-CyiU5gLrWqP7Wku4jkKE-loginiiitacin'}
	y = requests.get(url,headers=headers)
	y = y.content
	parsed_html1 = BeautifulSoup(y)
	y = parsed_html1.findAll('table')[1].findAll('table')[2]
	q = y.findAll('tr')[0].findAll('td')[0]
	w = q.findAll('a')[0].findAll('center')[0].text
	print(w)
	

