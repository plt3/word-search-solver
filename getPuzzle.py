import requests
from bs4 import BeautifulSoup


def findWords(grid, words):
    noSpaceWords = [word.replace(" ", "") for word in words]
    wordsDict = {noSpace: space for noSpace, space in zip(noSpaceWords, words)}

    noSpaceWords.sort(key=lambda x: len(x), reverse=True)

    occupiedSpaces = []
    foundWords = []
    foundTotal = 0

    for word in noSpaceWords:
        for rowInd, row in enumerate(grid):
            for colInd, letter in enumerate(row):
                if letter == word[0]:
                    directions = []

                    # check for forward, horizontal words
                    east = "".join(row[colInd : colInd + len(word)])
                    if east == word:
                        spotList = [
                            (c, rowInd) for c in range(colInd, colInd + len(word))
                        ]
                        directions.append(("E", spotList))

                    # check for backward, horizontal words
                    if colInd - len(word) >= -1:
                        if colInd - len(word) == -1:
                            west = "".join(row[colInd::-1])
                        else:
                            west = "".join(row[colInd : colInd - len(word) : -1])
                        if west == word:
                            spotList = [
                                (c, rowInd)
                                for c in range(colInd, colInd - len(word), -1)
                            ]
                            directions.append(("W", spotList))

                    # check for down, vertical words
                    try:
                        south = "".join(
                            [grid[i][colInd] for i in range(rowInd, rowInd + len(word))]
                        )
                        if south == word:
                            spotList = [
                                (colInd, r) for r in range(rowInd, rowInd + len(word))
                            ]
                            directions.append(("S", spotList))
                    except IndexError:
                        pass

                    # check for up, vertical words
                    if rowInd - len(word) >= -1:
                        north = "".join(
                            [
                                grid[i][colInd]
                                for i in range(rowInd, rowInd - len(word), -1)
                            ]
                        )
                        if north == word:
                            spotList = [
                                (colInd, r)
                                for r in range(rowInd, rowInd - len(word), -1)
                            ]
                            directions.append(("N", spotList))

                    # check for up, right diagonal words
                    if rowInd - len(word) >= -1 and len(row) - colInd - len(word) >= 0:
                        northEast = "".join(
                            [grid[rowInd - i][colInd + i] for i in range(len(word))]
                        )
                        if northEast == word:
                            spotList = [
                                (colInd + i, rowInd - i) for i in range(len(word))
                            ]
                            directions.append(("NE", spotList))

                    # check for down, right diagonal words
                    if (
                        len(grid) - rowInd - len(word) >= 0
                        and len(row) - colInd - len(word) >= 0
                    ):
                        southEast = "".join(
                            [grid[rowInd + i][colInd + i] for i in range(len(word))]
                        )
                        if southEast == word:
                            spotList = [
                                (colInd + i, rowInd + i) for i in range(len(word))
                            ]
                            directions.append(("SE", spotList))

                    # check for down, left diagonal words
                    if len(grid) - rowInd - len(word) >= 0 and colInd - len(word) >= -1:
                        southWest = "".join(
                            [grid[rowInd + i][colInd - i] for i in range(len(word))]
                        )
                        if southWest == word:
                            spotList = [
                                (colInd - i, rowInd + i) for i in range(len(word))
                            ]
                            directions.append(("SW", spotList))

                    # check for up, left diagonal words
                    if rowInd - len(word) >= -1 and colInd - len(word) >= -1:
                        northWest = "".join(
                            [grid[rowInd - i][colInd - i] for i in range(len(word))]
                        )
                        if northWest == word:
                            spotList = [
                                (colInd - i, rowInd - i) for i in range(len(word))
                            ]
                            directions.append(("NW", spotList))

                    # check each found direction for overlaps with longer words
                    for direction in directions:
                        overlap = False

                        for spaceList in occupiedSpaces:
                            subString = " ".join(
                                [f"{col},{row}" for col, row in direction[1]]
                            )
                            bigString = " ".join(
                                [f"{col},{row}" for col, row in spaceList]
                            )

                            if subString in bigString:
                                overlap = True
                                break

                        if not overlap:
                            print(
                                f"{direction[0]}: found {wordsDict[word]} at ({colInd}, {rowInd})"
                            )
                            foundTotal += 1
                            occupiedSpaces.append(direction[1])
                            foundWords.append(wordsDict[word])
                            break

    notFoundWords = []

    for word in words:
        if word not in foundWords:
            notFoundWords.append(word)

    if not len(notFoundWords):
        print(f"\nFound all {len(words)} words in game!")
    else:
        notFound = len(words) - len(notFoundWords)
        print(f"\nFound {notFound} of {len(words)} words. Didn't find:")
        print("\n".join(notFoundWords))


def getHtml():
    res = requests.get(
        # the two below (halloween, relationshipts) have multiple occurences
        "http://www.whenwewordsearch.com/word_search/autumn_and_halloween/92158/word_search.jsp"
        # "http://www.whenwewordsearch.com/word_search/relationships/390/word_search.jsp"
        # one below (50 states) is poorly designed so the program doesn't find Virginia
        # "http://www.whenwewordsearch.com/word_search/all_50_states/13/word_search.jsp"
    )
    res.raise_for_status()

    fullHtml = res.text
    # with open("page.html") as f:
    #     fullHtml = f.read()

    return fullHtml


def getGridAndList(htmlPage):
    soup = BeautifulSoup(htmlPage, "lxml")
    puzzleTable = soup.select_one("table.puzzlegrid")
    answerTable = soup.select_one("td.datalistcolumn > table")

    gameGrid = []
    wordsList = []

    for row in puzzleTable.findChildren("tr", recursive=False):
        rowList = []
        for data in row.findChildren("td", recursive=False):
            rowList.append(data.get_text())
        gameGrid.append(rowList)

    for row in answerTable.findChildren("tr", recursive=False):
        for data in row.findChildren("td", recursive=False):
            targetWord = data.get_text().strip()
            if targetWord:
                wordsList.append(targetWord)

    return (gameGrid, wordsList)


def main():
    pageContent = getHtml()
    fullGrid, wordsList = getGridAndList(pageContent)
    findWords(fullGrid, wordsList)


if __name__ == "__main__":
    main()
