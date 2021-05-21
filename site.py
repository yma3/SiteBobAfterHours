from flask import Flask, render_template
from urllib.parse import unquote
import json
import sim
import params

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route("/")
def hello():
    # return "Hello World!"
    return render_template('inputfieldtest.html')

@app.route("/sim/<string:inputStr>", methods=['GET'])
def printTest(inputStr):
    # print(inputStr)
    # print(type(inputStr))
    # print(inputStr)
    decodedStr = unquote(inputStr)
    # print(type(decodedStr))
    # print(decodedStr)
    #
    strToDict = json.loads(inputStr)
    # print(type(strToDict))
    # print(strToDict)

    with open(params.SITE_INPUT_FILE, 'w') as outfile:
        json.dump(strToDict, outfile)
        # print("Dumped")

    # sim.sim()
    with open(params.SITE_INPUT_FILE) as json_file: # minionsList is the list of minions
        allBoards_data = json.load(json_file)

    strdata = sim.extractBoards(allBoards_data)
    # print(strdata)
    args = extractSimData(strdata)

    return render_template('sim_output.html', **args)
    # return render_template('sim_output.html', title='WoW!', simout=strdata, WLRate=wldata, labels=label, win_values=winbrk, max=max(dmgbrk)*1.1)

@app.route("/whatbuildshouldiplay", methods=['GET'])
def getRandomBuild():
    build = "Random Build Here"
    return build

@app.route("/testkrippsim", methods=['GET'])
def testKrippSim():
    with open(params.TEST_DATA_INPUT_FILE) as json_file: # minionsList is the list of minions
        allBoards_data = json.load(json_file)
    strdata = sim.extractBoards(allBoards_data)
    # print(strdata)
    args = extractSimData(strdata)
    return render_template('sim_output.html', **args)

def filterDmgBrk(dmgbrk):
    start, end = 0, 0
    for idx, val in enumerate(dmgbrk):
        if not val:
            start = idx
    for idx, val in reversed(list(enumerate(dmgbrk))):
        if not val:
            end = idx

    start_dist = 48-start
    end_dist = end-48
    higher_dist = min(int(max([start_dist, end_dist, 10])*1.2), 48)
    return higher_dist

def splitDmgBrk(dmgbrk):
    wins = [0]*len(dmgbrk)
    losses = [0]*len(dmgbrk)
    ties = [0]*len(dmgbrk)
    ties[48] = dmgbrk[48]
    for idx, val in enumerate(dmgbrk):
        if val > 0:
            if idx < 48:
                losses[idx] = dmgbrk[idx]
            elif idx > 48:
                wins[idx] = dmgbrk[idx]

    # print(max(wins), max(losses), max(ties))
    return wins, losses, ties

def extractSimData(strdata):
    strdata = strdata.split('$')[1:]
    eps = int(strdata[0])


    # WL data contains [Wins, Losses, Ties, W|F, L|F, T|F]
    wldata = []
    for wl in strdata[1].split(",")[0:3]:
        x = str(int(wl.split(":")[1])/eps*100)[0:5]
        x = x.split(".")
        x = ".".join([x[0][:3], x[1][:2]])
        wldata.append(x)

    eps_givenFirst = 0
    for wl in strdata[1].split(",")[3:6]:
        eps_givenFirst += int(wl.split(":")[1])

    # print(eps_givenFirst)
    for wl in strdata[1].split(",")[3:6]:
        x = str(int(wl.split(":")[1])/eps_givenFirst*100)[0:5]
        x = x.split(".")
        x = ".".join([x[0][:3], x[1][:2]])
        wldata.append(x)



    # print(strdata)
    # print(wldata)
    label = [item for item in range(-48, 48+1)]
    dmgbrk = [int(i) for i in strdata[2].split(',')]
    winbrk, lossbrk, tiebrk = splitDmgBrk(dmgbrk)
    filterIdx_dist = filterDmgBrk(dmgbrk)
    # print(filterIdx_dist)
    label = label[48-filterIdx_dist:48+filterIdx_dist]
    winbrk = winbrk[48-filterIdx_dist:48+filterIdx_dist]
    lossbrk = lossbrk[48-filterIdx_dist:48+filterIdx_dist]
    tiebrk = tiebrk[48-filterIdx_dist:48+filterIdx_dist]

    WLtotals = ", ".join(strdata[1].split(",")[0:3])
    #
    # print(winbrk, lossbrk, tiebrk)
    #
    # print(label)
    # print(dmgbrk)



    # Do shit here
    # response = inputStr
    # response.headers.add('Access-Control-Allow-Origin: *')
    args = {'title':'Simulation Results (' + str(eps) + ' iterations)','simout':strdata,'WLTotals':WLtotals,'labels':label,
            'win_values':winbrk, 'loss_values':lossbrk, 'tie_values':tiebrk, 'max':max(dmgbrk)*1.1, 'WLProbs':wldata
            }
    return args



if __name__ == "__main__":
    app.run()
