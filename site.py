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
    with open('minionsList.json') as json_file: # minionsList is the list of minions
        allBoards_data = json.load(json_file)

    strdata = sim.extractBoards(allBoards_data)
    # print(strdata)
    strdata = strdata.split('$')[1:]
    print(strdata)
    label = [item for item in range(-48, 48+1)]
    dmgbrk = [int(i) for i in strdata[2].split(',')]
    print(label)
    print(dmgbrk)



    # Do shit here
    # response = inputStr
    # response.headers.add('Access-Control-Allow-Origin: *')
    return render_template('sim_output.html', title='WoW!', simout=strdata, WLRate=strdata[1], labels=label, values=dmgbrk, max=10000)

@app.route("/whatbuildshouldiplay", methods=['GET'])
def getRandomBuild():
    build = "Random Build Here"
    return build

if __name__ == "__main__":
    app.run()
