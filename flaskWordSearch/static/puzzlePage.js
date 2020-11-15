const MIN_DIM = Math.min.apply(null, [window.innerHeight, window.innerWidth]) * .97;
const PUZZLE_TABLE = document.getElementsByTagName('table')[0];
const TABLE_BODY = document.getElementsByTagName('tbody')[0];

// TODO: figure out how to make words list fit on the page next to the grid depending on
// if it's on mobile or not

function genRandomRGB() {
  let rgb = 'rgb(';
  for (let i = 0; i < 3; i++) {
    randNum = Math.floor(Math.random() * 256).toString();
    rgb += randNum + ', ';
  }

  return rgb.slice(0, -2) + ')';
}

function clearGrid() {
  for (let row of TABLE_BODY.childNodes) {
    for (let elem of row.childNodes) {
      if (elem.tagName === 'TD') {
        elem.style.backgroundColor = 'white';
      }
    }
  }
}

function findStartNode(foundInfo) {
  const foundPlace = foundInfo[1][0] + ' '+ foundInfo[1][1];

  for (let row of TABLE_BODY.childNodes) {
    for (let elem of row.childNodes) {
      if (elem.id === foundPlace) {
        return elem;
      }
    }
  }
}

function highlightOtherNodes(start, length, xStep, yStep, colorBack) {
  xStart = parseInt(start.split(' ')[0]);
  yStart = parseInt(start.split(' ')[1]);

  for (let i = 0; i < length; i++) {
    elem = document.getElementById(`${xStart + i * xStep} ${yStart + i * yStep}`);
    elem.style.backgroundColor = colorBack;
  }
}

function highlightWord() {
  clearGrid();

  const foundArr = JSON.parse(event.target.id);
  const wordLength = event.target.innerHTML.replace(/\s/g, '').length;

  if (! foundArr.length) {
    alert(`We couldn\'t find ${event.target.innerHTML} in this puzzle. This is most` +
          ' likely due to it being a subset of another word in the grid.')
  } else {
    for (let i = 0; i < foundArr.length; i++) {
      const startingNode = findStartNode(foundArr[i]);
      let backColor = genRandomRGB();

      switch (foundArr[i][0]) {
        case 'N':
          highlightOtherNodes(startingNode.id, wordLength, 0, -1, backColor);
          break;
        case 'E':
          highlightOtherNodes(startingNode.id, wordLength, 1, 0, backColor);
          break;
        case 'S':
          highlightOtherNodes(startingNode.id, wordLength, 0, 1, backColor);
          break;
        case 'W':
          highlightOtherNodes(startingNode.id, wordLength, -1, 0, backColor);
          break;
        case 'NE':
          highlightOtherNodes(startingNode.id, wordLength, 1, -1, backColor);
          break;
        case 'SE':
          highlightOtherNodes(startingNode.id, wordLength, 1, 1, backColor);
          break;
        case 'SW':
          highlightOtherNodes(startingNode.id, wordLength, -1, 1, backColor);
          break;
        case 'NW':
          highlightOtherNodes(startingNode.id, wordLength, -1, -1, backColor);
          break;
      }
    }
  }
}

PUZZLE_TABLE.style.width = MIN_DIM + 'px';
PUZZLE_TABLE.style.height = MIN_DIM + 'px';
