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
        # os.system("cls")

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

    def optimizeLocal(self):
        count = 0

        for root, dirs, files in os.walk(self.downloadPath):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    source = tinify.from_file(path)
                    source.to_file(path)
                    count += 1
                    print(f">>> [Optimized]: {count}/{len(files)}")
                except tinify.Error as e:
                    print(f">>> [Optimize Error]: {e}")

    def optimizeTinify(self):
        count = 0
        tinify.key = self.tinifyAPIKEY

        for root, dirs, files in os.walk(self.downloadPath):
            for file in files:
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
                    print(f"\n>>> [Optimize Error]: {e}")

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
            "[4] - Exit \n"
            ">>> ENTER NUMBER: "
        )
        if opt == "1":
            app.download()
        elif opt == "2":
            app.optimize()
        elif opt == "3":
            app.optimizeTinify()
        elif opt == "4":
            exit()
except:
    print(">>> Exiting...")
