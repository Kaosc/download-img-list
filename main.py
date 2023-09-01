import os
import json
import requests
import urllib.request

class Downloader:
   def __init__(self):
      self.urlList = []
      self.downloadPath = "./downloads"
      self.dataFilePath = "./data/list.json"

   def createImagePath(self):
      if not os.path.exists(self.downloadPath):
         os.makedirs(self.downloadPath)

   def getTotalFileSum(self):
      total = 0

      for root, dirs, files in os.walk(self.downloadPath):
         total += len(files)

      if total == 0:
         return 1
      else:
         return total + 1

   def extractData(self):
      file = open(self.dataFilePath)
      data = json.load(file)

      for i in data:
         self.urlList.append(i["url"])

      file.close()

   def download(self, src):
      fileNum = self.getTotalFileSum()
      extension = src.split(".")[-1]

      os.system("cls")
      print(f"Downloading {fileNum}/{len(self.urlList)}")

      urllib.request.urlretrieve(src, f"{self.downloadPath}/{fileNum}.{extension}")

   def execute(self):
      self.extractData()
      self.createImagePath()

      for url in self.urlList:
         self.download(url)

downloader = Downloader()

downloader.execute()