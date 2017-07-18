import urllib
import lxml.html
import urllib2
import re
import os
import json
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

products = list()

url = 'http://www.juniper.net/us/en/products-services/a-z/'
text = urllib2.urlopen(url).read();
soup = BeautifulSoup(text);

data = soup.findAll('li',attrs={'class':'productaz-item'})
for div in data:
    links = div.findAll('a')
    for a in links:
	products.append("http://www.juniper.net" + a['href'])

product_dict = {}
pdfList = list()
with open("/var/www/pythonApi/products.txt", 'w') as f:
    for product in products:
	f.write(product)
	f.write("\n")

	m = re.search('\w*.*products-services\/(\w*.*?)\/$',product)
	hier = m.group(1)
	hier_list = hier.split("/")

	if len(hier_list) == 3:
	    if not hier_list[0] in product_dict:
	        product_dict[hier_list[0]] = {}
	    if not hier_list[1] in product_dict[hier_list[0]]:
	        product_dict[hier_list[0]][hier_list[1]] = {}
	    if not hier_list[2] in product_dict[hier_list[0]][hier_list[1]]:
	        website = urllib2.urlopen(product)
                html = website.read()
                links = re.findall('"(http://.*?)"', html)
		linkList = list()
                for link in links:
                    if "datasheets" in link:
			lnk = link.split("ref=",1)[1]
			if lnk not in pdfList:
			    pdfList.append(lnk)
			m1 = re.search('\w*.*\/(\w*.*?)$',lnk)
			linkList.append(m1.group(1))
		product_dict[hier_list[0]][hier_list[1]][hier_list[2]] = linkList 
	elif len(hier_list) == 2:
	    if not hier_list[0] in product_dict:
	        product_dict[hier_list[0]] = {}
	    if not hier_list[1] in product_dict[hier_list[0]]:
                website = urllib2.urlopen(product)
                html = website.read()
                links = re.findall('"(http://.*?)"', html)
                linkList = list()
                for link in links:
                    if "datasheets" in link:
                        lnk = link.split("ref=",1)[1]
                        if lnk not in pdfList:
                            pdfList.append(lnk)
                        m1 = re.search('\w*.*\/(\w*.*?)$',lnk)
                        linkList.append(m1.group(1))
		product_dict[hier_list[0]][hier_list[1]] = {}
                product_dict[hier_list[0]][hier_list[1]]["default"] = linkList
	elif len(hier_list) == 1:
	    if not hier_list[0] in product_dict:
	        product_dict[hier_list[0]] = {}

directory = "/var/www/pythonApi/pdf_files"
if not os.path.exists(directory):
    os.makedirs(directory)

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    m1 = re.search('\w*.*\/(\w*.*?)$',download_url)
    fileName = m1.group(1)
    pathFile = directory + "/" + fileName
    file = open(pathFile, 'w')
    file.write(response.read())
    file.close()

def convert_pdf_to_txt(filepath):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(filepath, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

for pdf in pdfList:
    download_file(pdf)

dst_dir = "/var/www/pythonApi/products_database/"
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

src_dir = "/var/www/pythonApi/pdf_files"
path_files = os.listdir(src_dir)
for path_fil in path_files:
    filepath = os.path.join(src_dir, path_fil)
    text3 = convert_pdf_to_txt(filepath)
    m1 = re.search('(\w*.*?).pdf$',path_fil)
    fil = m1.group(1)
    fileName = "/var/www/pythonApi/products_database/" + fil + ".txt"
    with open(fileName, 'w') as f:
        f.write(text3)

with open('/var/www/pythonApi/products_database/hierarchy.json', 'w') as f: f.write(json.dumps(product_dict))
with open('/var/www/hierarchy.json', 'w') as f: f.write(json.dumps(product_dict))
