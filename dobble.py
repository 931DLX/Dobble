import sys
import numpy as np


"""
Solves the Dobble symbols distribution for given number of symbols on each card.
The code is proof of concept of my own algorithm.

Author: Dariusz Laskowski
Date: 2024-08-26
"""
class Dobble:

    """
    ListOfLists: contains generated cards in form of lists of symbols' IDs
    ListOfSets: the same, but in form of list of sets. 
    Keeping both of them is a surplus for educational purposes.
    ListOfLists preserves oryginal order of elements, while ListOfSets is required to test correctness of generated cards.
    WorkMatrix is the main structure, which is recreated in each cycle of diagonal reads.
    """
    def __init__(self, PlaneOrder: int):
        self.PlaneOrder = PlaneOrder
        self.SymbolsOnCard = PlaneOrder + 1
        self.DeckSize = PlaneOrder * PlaneOrder + PlaneOrder + 1
        self.WorkMatrix = np.arange(self.PlaneOrder+1, self.DeckSize).reshape((self.PlaneOrder, self.PlaneOrder))
        self.ListOfLists=[]
        self.ListOfSets=[]
        
    """
    Creates a new mattrix by diagonal reads of current mattrix
    """
    def diagonalRead(self, direction: int):
        TmpMatrix = np.empty((self.PlaneOrder, self.PlaneOrder), dtype='int')
    
        for kolumna in range(self.PlaneOrder):
            for wiersz in range(self.PlaneOrder):
                if direction == 0:
                    TmpMatrix[kolumna, wiersz] = self.WorkMatrix[wiersz, (wiersz+kolumna) % self.PlaneOrder]
                else:
                    TmpMatrix[kolumna, wiersz] = self.WorkMatrix[(wiersz+kolumna) % self.PlaneOrder, wiersz]
        self.WorkMatrix = TmpMatrix

    
    """
    Tests given set against the list of sets for previosly generated cards.
    The set contains id's of elements on card.
    """
    def append_with_test(self, fset):
        for element in self.ListOfSets:
            wynik = element.intersection(fset)
            if len(wynik) != 1:
                print('Error in cards comparision, incorrect number of common symbols')
                quit()
        self.ListOfSets.append(fset)


    """
    Reads rows from WorkMatrix and stroes them in form of list of:
    - lists, which is finally used to generate the result 
    - sets to test correctness of generated cards.
    """
    def storeLists(self, prefix: int):
        for i in range(self.PlaneOrder):
            fset = set()
            flist= list()

            fset.add(prefix)
            flist.append(prefix)

            for j in range(self.PlaneOrder):
                fset.add(self.WorkMatrix[i,j])
                flist.append(self.WorkMatrix[i,j])
            
            self.append_with_test(fset)
            self.ListOfLists.append(flist)
            
    """
    Fills lists with the first card
    """
    def storeFirstList(self):
        fset = set()
        flist= list()
        
        for i in range(self.SymbolsOnCard):
            fset.add(i)
            flist.append(i)

        self.ListOfLists.append(flist)
        self.ListOfSets.append(fset)
        
    """
    Main part of algorithm
    """
    def generate(self):
        self.storeFirstList()
        for i in range(self.SymbolsOnCard):
            self.storeLists(i)
            self.diagonalRead(i)        
        
    """
    Some extra check if number of elements in list is correct
    """
    def testAmount(self):
        ListSize = len(self.ListOfLists)
        if ListSize == self.DeckSize:
            print(f"Deck size correct and equel to: {ListSize}")
        else:
            print(f"Deck size incorrect! Should be: {self.DeckSize} while is {ListSize}")

    def printResult(self):
        print(self.ListOfLists)


    """
    Writes results to file in form of sets of ints
    """
    def writeResultToFile(self, filename: str):
        with open(filename, 'w', encoding='utf8') as outputFile:
            for element in self.ListOfLists:
                card = "\t".join(map(str, element))
                outputFile.write(f"{card}\n")


    """
    Reads symbols from file
    """
    def readSymbols(self, symblolsFileName: str):
        lines = []
        with open(symblolsFileName, 'r', encoding='utf8') as file:
            lines = [line.strip() for line in file]
        return lines
        
    
    """
    Writes results to file in form of strings read from symbolsFile
    Make sure that symbolsFile contains correct number of elements
    """
    def writeResultWithSymbols(self, outFileName: str, symbolsFile: str):
        symbols = self.readSymbols(symbolsFile)
        if len(symbols) < self.DeckSize:
            print(f"\nError creating output file")
            print(f"Incorrect number of symbols in {symbolsFile} file")
            print(f"Should be {self.DeckSize} and file contains {len(symbols)}")
            quit()
        with open(outFileName, 'w', encoding='utf8') as outputFile:
            for element in self.ListOfLists:
                card = "\t".join([symbols[i] for i in element])
                outputFile.write(f"{card}\n")
        print(f"Results written to {outFileName}")


print("This program generates deck of cards for Dobble")
try:
    sideSize = int(input('Enter the number of symbols on a card '))
except ValueError:
    print("Error: Given value shuld be an integer, equal prime numer + 1.")
    sys.exit(1)    
    
    
if sideSize > 1:
    order = sideSize - 1
else:
    order = 1

myDobble = Dobble(order)
myDobble.generate()
myDobble.testAmount()
myDobble.writeResultWithSymbols('results.txt', 'symbols.txt')
# myDobble.writeResultToFile('dobble_cards.txt')
    


