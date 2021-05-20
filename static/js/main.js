function removerows (tablebody) {
  var rows = tablebody.getElementsByTagName("tr");
  while (rows.length)
    rows[0].parentNode.removeChild(rows[0]);
}

function addrows (tablebody, n, ally) {
  var allytext = ally ? "Ally" : "Enemy"
  for (var i=0; i<n; i++) {
    var row = document.createElement("tr");
    var titlecell = document.createElement("td");
    titlecell.appendChild(document.createTextNode("Row " + (i+1)));
    row.appendChild(titlecell);

    var cell = document.createElement("td");
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("id", allytext+"row["+i+"]ATK");
    input.setAttribute("placeholder", "ATK");
    var input2 = document.createElement("input");
    input2.setAttribute("type", "text");
    input2.setAttribute("id", allytext+"row["+i+"]HP");
    input2.setAttribute("placeholder", "HP");
    makeMinionDropdown(row, i, ally)
    cell.appendChild(input);
    row.appendChild(cell);
    cell.appendChild(input2);
    tablebody.appendChild(row);
  }
}

function changeAllied() {
  var select = document.getElementById("numrowsAlly");
  var index = select.selectedIndex;
  var n = parseInt(select.value);
  var tablebody = document.getElementById("maintablebodyAlly");
  removerows(tablebody);
  addrows(tablebody, n, 1);
}

function changeEnemy() {
  var select = document.getElementById("numrowsEnemy");
  var index = select.selectedIndex;
  var n = parseInt(select.value);
  var tablebody = document.getElementById("maintablebodyEnemy");
  removerows(tablebody);
  addrows(tablebody, n, 0);
}

function printText() {
  var dict = {};
  var select = document.getElementById("numrowsAlly");
  var n = parseInt(select.value);
  for (var i=0; i<n; i++) {
    var text1 = document.getElementById("Allyrow["+i+"]HP");
    var text2 = document.getElementById("Allyrow["+i+"]ATK");
    var selection = document.getElementById("AllyselectionCell"+i);
    console.log(text1.value);
    console.log(text2.value);
    console.log(selection);
    dict["Allyrow"+i+"col1"] = text1.value;
    dict["Allyrow"+i+"col2"] = text2.value;
    dict["Allyselection"+i] = selection.value;
    // array.push(text1, text2);
  }
  console.log(dict);
  Get(encodeURIComponent(JSON.stringify(dict)));
}

function getTableValues(ally) {
  console.log("HELLO HERE");
  var allytext = ally ? "Ally":"Enemy";
  var dict = {};
  var select = document.getElementById("numrows"+allytext);
  var n = parseInt(select.value);
  for (var i=0; i<n; i++) {
    var minion = {};
    var text1 = document.getElementById(allytext+"row["+i+"]HP");
    var text2 = document.getElementById(allytext+"row["+i+"]ATK");
    var selection = document.getElementById(allytext+"selectionCell"+i);
    // console.log(text1.value);
    // console.log(text2.value);
    // console.log(selection);
    minion["Name"] = selection.value;
    minion["HP"] = text1.value;
    minion["ATK"] = text2.value;
    // array.push(text1, text2);
    dict["Minion"+i] = minion;
  }
  return dict
}

function getAllTables() {
  console.log("HELLO HERE");
  var dict = {};
  dict["AlliedBoard"] = getTableValues(1);
  dict["EnemyBoard"] = getTableValues(0);
  Get(encodeURIComponent(JSON.stringify(dict)));
}


function Get(stringInput){
  // var stringInput = "aleccheckthisout";
  // var stringInput_Arr = JSON.stringify(array)
  var Httpreq = new XMLHttpRequest();
  var baseSiteURL = 'http://localhost:5000/test/';
  var httpURL = baseSiteURL + stringInput;
  console.log(httpURL);
  Httpreq.open("GET",httpURL, true);
  Httpreq.send(null);
  console.log(Httpreq.responseText);
  location.href = httpURL;
  return Httpreq.responseText;
}

function test() {
  console.log("Testing!");
  console.log(Get());
}

function makeMinionDropdown(row, i, ally) {

  // var minionList = ["Tabby Cat", "Alley Cat"];

  var rank1s = ["Alley Cat", "Tabby Cat", "Scavenging Hyena","Fiendish Servant","Vulgar Homunculus","Wrath Weaver",
                  "Dragonspawn Lieutenant","Red Whelp","Refreshing Anomaly","Sellemental","Water Droplet","Micro Machine",
                  "Micro Mummy","Murloc Tidehunter","Murloc Scout","Murloc Tidecaller","Rockpool Hunter","Deck Swabbie","Scallywag",
                  "Acolyte of C'Thun"];
  var rank2s = ["Spawn of N'Zoth", "Boom Bot"]


  var minionList = [rank1s, rank2s];
  // <select id="numrows" name="numrows" onchange="change()">
  //   <option value="1">1</option>
  //   <option value="2">2</option>
  //   <option value="3">3</option>
  //   <option value="4">4</option>
  //   <option value="5">5</option>
  //   <option value="6">6</option>
  //   <option value="7">7</option>
  // </select>
  var allytext = ally ? "Ally" : "Enemy";
  var listOfNumbers = ["a","b","c"];
  var selectionCell = document.createElement("select");
  selectionCell.setAttribute("id", allytext+"selectionCell" + i);
  for (var rank=0; rank<minionList.length; rank++) {
    var minionRanks = minionList[rank];
    var optgroup = document.createElement("optgroup")
    optgroup.setAttribute("label", "Rank " + (rank+1))
    selectionCell.appendChild(optgroup)
    for (var i=0; i<minionRanks.length; i++) {
      var option = document.createElement("option");
      option.setAttribute("value", minionRanks[i]);
      option.textContent = minionRanks[i];
      selectionCell.appendChild(option);
    }
  }
  row.appendChild(selectionCell);

}
