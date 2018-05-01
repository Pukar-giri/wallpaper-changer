import urllib3 as url
import ctypes
import json
import os
from random import randint
from bs4 import BeautifulSoup
#=================================================================================================================================================================

def changeit(rname):
	url.disable_warnings()
#preparing the search string to search for the image in google image search
	name=rname+" HD wallpaper"
	name=name.replace(" ","+")#google search string has + instead of space
	search="https://www.google.com.np/search?q={}&source=lnms&tbm=isch&tbs=isz:ex,iszw:1920,iszh:1080".format(name)#adding the search key word to the url
	#making up a fake header so that the ai at google beleives us to be an legitimate user not a bot
	hdr={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	#initializing the request pool to start the request.
	http=url.PoolManager()
	#sending the request to the google server.
	#print("starting the request\n at the location:\n"+search)
	connection=http.request(method='GET',url=search,headers=hdr)#using the connection pool here ie http
	#proceeding only if the server has responded correctly and completely
	if connection.status==200:
	#parsing the html code using the beautiful soup library.
		soup=BeautifulSoup(connection.data,"html.parser")
	# if there is no directory of the search name create one
		if not os.path.exists(rname):
			print("creating folder")
			os.makedirs(rname)
			print("created")

		for x in range(100):
			print("working on "+str(x)+" th image")
	#search the response for a div element having the data-ri value as that random number and search for a div with class name rg_meta and parse all its children.
			for child in soup.find("div", {"data-ri":"{}".format(str(x))}).find("div", {"class":"rg_meta"}).children:
	#load that child element searched by beautiful soup as json object
				data_content = json.loads(child)
	#load ou component of data_content as link
				link = data_content["ou"]
	#split the link at every backslash caracter ....it returns a list of splitted words
				file=link.split("/")
	#take the last item in the list to be the filename for the image to be downloaded
				fname=file.pop()
	#now send the request to the server to try and obtain the image
				image=http.request(method="get",url=link)
	#if the server sends the image correctly.
				if image.status==200:
	#create a new file in the directory name same as search keyword and file name same as generated above and write the image contents to the file.
					with open(rname+"\\"+fname,'wb')as w:
						w.write(image.data)
						w.close()
						print(fname+"---------> written successfully")
	#as the wallpaper has been saved correctly try to make it the current wallpaperusing the ctypes library
					#print("changing the wallpaper")
					#SPI_SETDESKWALLPAPER = 20
					#ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0,os.getcwd()+"\\"+rname+"\\"+fname, 0)
	#if the wallpaper has been set correctly declare that we have done the work correctly.
					notdone=False
					print("wallpaper changed successfully")
				else:
					print("The file could not be downloaded")
	else:
		print("Goole couldnot be contacted..........sorry")
		
#===================================================================================================================================================================
		
		
if __name__=="__main__" :
	rname=input("enter the name to search:    ")
	changeit(rname)