from flask import Flask, render_template
from urllib.parse import unquote
import json
import sim

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route("/")
def hello():
    # return "Hello World!"
    return render_template('inputfieldtest.html')

@app.route("/test/<string:inputStr>", methods=['GET'])
def printTest(inputStr):
    # print(inputStr)
    # print(type(inputStr))
    # print(inputStr)
    decodedStr = unquote(inputStr)
    # print(type(decodedStr))
    # print(decodedStr)
    #
    strToDict = json.loads(inputStr)
    print(type(strToDict))
    print(strToDict)

    with open('minionsList.json', 'w') as outfile:
        json.dump(strToDict, outfile)
        print("Dumped")

    # sim.sim()
    # Do shit here
    # response = inputStr
    # response.headers.add('Access-Control-Allow-Origin: *')
    return decodedStr

@app.route("/whatbuildshouldiplay", methods=['GET'])
def getRandomBuild():
    build = "Random Build Here"
    return build

if __name__ == "__main__":
    app.run()
