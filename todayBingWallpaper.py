'''
	todayBingWallpaper
	Bing json File Url: https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN
	Just for learn!
'''
import requests
import json
import time
import os
import argparse

info = '''todayBingWallpaper,default download path './data',save name simple: 2020-01-01.jpg.
Just for learn!
'''


class BingWallpaper:
	def __init__(self):
		self.url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
		self.timeFormat = time.strftime('%Y-%m-%d')
		self.version = '0.0.1'
			
	def parse(self,echo=False,writeDir=[]):
		'''
			@echo: echo parse result.
			@writeDir: save json file while list not empty.
		'''
		print('get json')
		r = requests.get(self.url)
		
		if r.status_code != 200:
			print(f'network error:{r.status_code}')
			return
		
		if len(writeDir):
			for dirPath in writeDir:
				saveJsonName = os.path.join(dirPath,timeFormat)
				
				with open(saveJsonName,'w',encoding='utf-8') as f:
					f.write(r.text)
				
		print('parse json')
		try:
			j = json.loads(r.text)
		except Exection as e:
			print(f'Error:{e.txt}')
		
		img = j['images'][0]

		imgPath = img["url"]
		imgurl = "http://cn.bing.com" + imgPath
		title = img['title']
		copyright = img['copyright']
		copyrightlink = img['copyrightlink']

		print('parse succesful')
				
		if echo:
			print('-'*51)
			print(f"""title: {title}
imgUrl: {imgurl}
copyright: {copyright}
copyrightlink: {copyrightlink}
		""")

		
		return imgurl
		
	def download(self,downloadDir=[],force=False):
		url = self.parse(echo=False,writeDir=[])
		saveName = self.timeFormat + '.jpg'
		
		img = requests.get(url)
		
		if len(downloadDir):
			for dirPath in downloadDir:
				downloadPath = os.path.join(dirPath,saveName)
				
				if os.path.exists(downloadPath):
					print(f'file {downloadPath} exist!')

				if force or not os.path.exists(downloadPath):
					print(f'write path: {downloadPath}')
				
					with open(downloadPath,'wb' ) as f:
						f.write(img.content)		

	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=info)
	parser.add_argument('-s', '--save', dest='save', nargs='+', help='save folders;if not exist,make it;default is ./data')
	parser.add_argument('-p', '--parse-without-download', action='store_true', dest='parse', default=False, help='just parse and echo Wallpaper url')
	parser.add_argument('-f', '--force', action='store_true', dest='force', default=False, help='download and write whether it exists')
	parser.add_argument('-v', '--version', action='store_true', dest='version', default=False, help='Version')

	args = parser.parse_args()

	bW = BingWallpaper()
	
	if args.version:
		print(bW.version)
		exit()
	   
	if args.parse:
		bW.parse(echo=True,writeDir=[])
		exit()
	
	downloadDir = []

	if args.save:
		downloadDir = args.save
	else:
		downloadDir.append('./data')
		if not os.path.exists('./data'):
			os.mkdir('./data')
			
	bW.download(downloadDir,force=args.force)
