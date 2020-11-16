const ADJUSTED_WIDTH = window.innerWidth * 0.97
const ADJUSTED_HEIGHT = window.innerHeight * 0.93 * 0.6
const PUZZLE_TABLE = document.getElementsByTagName('table')[0];
const TABLE_BODY = document.getElementsByTagName('tbody')[0];
const WORDS_BOX = document.getElementsByClassName('words-container')[0];
const EMPTY_BACK = 'gray';
const FULL_BACK = 'black';

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

function clearWords() {
  for (let word of WORDS_BOX.childNodes) {
    if (word.tagName === 'P') {
      word.style.color = 'black';
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

function highlightWord(element=false) {
  let giveError = false;

  if (! element) {
    element = event.target;
    giveError = true;
    clearGrid();
    clearWords();
  }

  const foundArr = JSON.parse(element.id);
  const wordLength = element.innerHTML.replace(/\s/g, '').length;

  if (! foundArr.length && giveError) {
    alert(`We couldn\'t find ${element.innerHTML} in this puzzle. This is most` +
          ' likely due to it being a subset of another word in the grid.')
  } else {
    for (let i = 0; i < foundArr.length; i++) {
      const startingNode = findStartNode(foundArr[i]);
      let backColor = genRandomRGB();

      if (i === 0) {
        element.style.color = backColor;
      }

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

function highlightAll() {
  clearGrid();

  for (let node of WORDS_BOX.childNodes) {
    if (node.tagName === 'P') {
      highlightWord(node);
    }
  }

  clearWords();
}

function changeBackground() {
  const prevColor = event.target.style.color;

  if (event.target.style.backgroundColor !== FULL_BACK) {
    event.target.style.backgroundColor = FULL_BACK;
    if (prevColor !== FULL_BACK && prevColor) {
      event.target.style.color = prevColor;
    } else {
      event.target.style.color = EMPTY_BACK;
    }
  } else {
    event.target.style.backgroundColor = EMPTY_BACK;
    if (prevColor !== EMPTY_BACK) {
      event.target.style.color = prevColor;
    } else {
      event.target.style.color = FULL_BACK;
    }
  }
}

if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
  // slightly different styling if on mobile
  PUZZLE_TABLE.style.width = ADJUSTED_WIDTH + 'px';
  PUZZLE_TABLE.style.height = ADJUSTED_WIDTH + 'px';

  for (let node of WORDS_BOX.getElementsByTagName('p')) {
    node.style.fontSize = 'large';
  }
} else {
  PUZZLE_TABLE.style.width = ADJUSTED_HEIGHT + 'px';
  PUZZLE_TABLE.style.height = ADJUSTED_HEIGHT + 'px';
}
