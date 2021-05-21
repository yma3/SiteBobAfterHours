import json
import subprocess
import params



def extractBoards(board_dicts):

    with open(params.ALL_MINIONS_FILE) as json_file: # minions is the overall file of all minions
        listOfAllMinions = json.load(json_file)

    # print("Hello World!")

    alliedBoard = board_dicts["AlliedBoard"]
    enemyBoard = board_dicts["EnemyBoard"]
    #
    # print(alliedBoard)
    # print(enemyBoard)

    minion_vects = {}
    allied_minionvect = []
    enemy_minionvect = []

    print("Getting Player Board")
    for minion_pos, minion_data in alliedBoard.items():
        for minion_tag, allminion_data in listOfAllMinions.items():
            if (allminion_data["name"] == minion_data["Name"]) and (len(minion_tag) <= 4):
                print("Found:" + minion_tag + ", " + allminion_data["name"])
                curr_min = allminion_data.copy() # SET TAG DATA HERE
                curr_min["id"] = int(minion_tag)
                curr_min["hp"] = int(minion_data["HP"])
                curr_min["atk"] = int(minion_data["ATK"])
                curr_min["isTaunt"] = int(minion_data["isTaunt"])
                curr_min["isDivine"] = int(minion_data["isDivine"])
                curr_min["isPoison"] = int(minion_data["isPoison"])
                allied_minionvect.append(curr_min)

    print("Getting Enemy Board")
    for minion_pos, minion_data in enemyBoard.items():
        for minion_tag, allminion_data in listOfAllMinions.items():
            if (allminion_data["name"] == minion_data["Name"]) and (len(minion_tag) <= 4):
                print("Found:" + minion_tag + ", " + allminion_data["name"])
                curr_min = allminion_data.copy() # SET TAG DATA HERE
                curr_min["id"] = int(minion_tag)
                curr_min["hp"] = int(minion_data["HP"])
                curr_min["atk"] = int(minion_data["ATK"])
                curr_min["isTaunt"] = int(minion_data["isTaunt"])
                curr_min["isDivine"] = int(minion_data["isDivine"])
                curr_min["isPoison"] = int(minion_data["isPoison"])
                enemy_minionvect.append(curr_min)

    # print(allied_minionvect)
    #
    # print(enemy_minionvect)

    minion_vects["Allied"] = allied_minionvect
    minion_vects["Enemy"] = enemy_minionvect

    with open(params.CPP_INPUT_FILE, 'w') as outfile:
        json.dump(minion_vects, outfile)
        # print("Dumped")

    strdata = simSubprocess()
    return strdata


def simSubprocess():
    # print("Running subprocess...")
    p=subprocess.Popen([params.CPP_PROCESS_FILE, params.TOTAL_ITERATIONS, "0", params.CPP_INPUT_FILE, params.DATABASE_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    # print(stdout_data.decode('utf8'))
    print("Subprocess Done.")
    return stdout_data.decode('utf8')







if __name__ == "__main__":
    print("Running!")

    with open('minionsList.json') as json_file: # minionsList is the list of minions
        allBoards_data = json.load(json_file)


    extractBoards(allBoards_data)
    # simSubprocess()
