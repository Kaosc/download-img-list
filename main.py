import os
import json
import urllib.request
import time
from PIL import Image
import dotenv
import tinify

dotenv.load_dotenv()

class App:
    def __init__(self):
        self.urlList = []
        self.downloadPath = "./downloads"
        self.dataFilePath = "./data/list.json"
        self.tinifyAPIKEY = os.getenv("TINIFY_API_KEY")
        self.timeout = 5

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
            self.urlList.append(i)

        file.close()

    def download(self, url):
        os.system("cls")

        fileNum = self.getTotalFileSum()
        extension = url.split(".")[-1]

        try:
            src = url
            urllib.request.urlretrieve(
                src, f"{self.downloadPath}/{fileNum}.{extension}"
            )
        except Exception as e:
            print(f"\n>>> [Download Error]: {e} | {url}")

        print(f"\n\n>>> [Downloaded] {fileNum}/{len(self.urlList)}\n")

        for wait in range(self.timeout):
            print(
                f">>> {self.timeout-wait} seconds left to download next image...",
                end="\r",
            )
            time.sleep(1)

    def logger(self, e):
        f = open('error-logs.txt', 'a')
        f.write(f"[{time.strftime("%Y-%m-%d %H:%M:%S")}]: {e}\n")
        f.close()

    def getFileSizes(self):
        totalSize = 0

        try: 
            for root, dirs, files in os.walk(self.downloadPath):
                for file in files:
                    path = os.path.join(root, file)
                    totalSize += os.path.getsize(path)
        except Exception as e:
            self.logger(e)
            print(f"\n>>> [Get File Size Error]: {e}")

        return totalSize

    def optimizeLocal(self):
        count = 0

        unoptimizedtotalSize = self.getFileSizes()                

        for root, dirs, files in os.walk(self.downloadPath):
            for file in files:
                os.system("cls")

                try:
                    path = os.path.join(root, file)
                    img = Image.open(path)
                    img.save(path, optimize=True, quality=50)
                    count += 1
                    print(f">>> [Optimized]: {count}/{len(files)}")
                    time.sleep(1)
                except tinify.Error as e:
                    self.logger(e)
                    print(f">>> [Optimize Error]: {e}")

        optimizedTotalSize = self.getFileSizes()

        self.printOptimizeResults(unoptimizedtotalSize, optimizedTotalSize)

    def optimizeTinify(self):
        count = 0

        if (self.tinifyAPIKEY == None) or (self.tinifyAPIKEY == ""):
            m = ">>> [Tinify Error]: API KEY not found"
            self.logger(m)
            throw(m)

        tinify.key = self.tinifyAPIKEY

        unoptimizedtotalSize = self.getFileSizes()                

        for root, dirs, files in os.walk(self.downloadPath):
            for file in files:
                os.system("cls")

                try:
                    path = os.path.join(root, file)
                    source = tinify.from_file(path)
                    source.to_file(path)
                    count += 1
                    print(f"\n\n>>> [Optimized]: {count}/{len(files)}\n")

                    for wait in range(self.timeout):
                        print(
                            f">>> {self.timeout-wait} seconds left to optimize next image...",
                            end="\r",
                        )
                        time.sleep(1)

                except tinify.Error as e:
                    self.logger(e)
                    print(f"\n>>> [Optimize Error]: {e}")

        optimizedTotalSize = self.getFileSizes()

        self.printOptimizeResults(unoptimizedtotalSize, optimizedTotalSize)
    
    def printOptimizeResults(self, unoptimizedSize, optimizedSize):
        print(f"\n\n>>> [Unoptimized Size]: {unoptimizedSize/1000000} MB")
        print(f">>> [Optimized Size]: {optimizedSize/1000000} MB")
        print(f">>> [Total Saved]: {(unoptimizedSize - optimizedSize)/1000000} MB")

    def execute(self):
        self.extractData()
        self.createImagePath()

        for url in self.urlList:
            self.download(url)

app = App()

try:
    while True:
        print("\n\n****************\n")
        opt = input(
            "[1] - Download \n"
            "[2] - Optimize (Local) \n"
            "[3] - Optimize (Tinify) \n"
            "[4] - Exit \n\n"
            ">>> ENTER NUMBER: "
        )
        if opt == "1":
            app.execute()
        elif opt == "2":
            app.optimizeLocal()
        elif opt == "3":
            app.optimizeTinify()
        elif opt == "4":
            exit()
except KeyboardInterrupt:
    print("\n>>> Exiting...\n")
except Exception as e:
    app.logger(e)
    print(f"\n>>> [Unexpected Error]: {e}\n")
