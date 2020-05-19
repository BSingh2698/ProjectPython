import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        try:
            i, j = cell
        except:
            print(cell)
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        
        return set()
        
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return
        self.cells = self.cells - set({cell})
        self.count = self.count-1
        
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells:
            return
        self.cells = self.cells - set({cell})
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        cells = set()
        i,j = cell
        
        start_row = max(0,i-1)
        end_row = min(self.height-1,i+1)
        
        start_col = max(0,j-1)
        end_col = min(self.width-1,j+1)
        
        for row in range(start_row,end_row+1):
            for col in range(start_col,end_col+1):
                c = row,col
                if not c == cell:
                    if c not in self.moves_made and c not in self.safes:
                        cells.add(c)
                        
        if len(cells) == 0:
            return
        
        
        sentence = Sentence(cells,count)
        self.knowledge.append(sentence)
        
        sentences = []
        for sents in self.knowledge:
            cells1 = sentence.cells
            cells2 = sents.cells
            
            if cells1.issubset(cells2) and not(cells1 == cells2):
                cells0 = cells2-cells1
                count0 = max(0,sents.count - sentence.count)
                sents0 = Sentence(cells0,count0)
                sentences.append(sents0)
            
            elif cells2.issubset(cells1) and not(cells1 == cells2):
                cells0 = cells1-cells2
                count0 = max(0,sentence.count - sents.count)
                sents0 = Sentence(cells0,count0)
                sentences.append(sents0)
            else:
                sentences.append(sents)
        
        self.knowledge = sentences

        l = len(self.knowledge)
        
        for i in range(l):
            
            sents = self.knowledge[i]
            safe_cells = sents.known_safes()
            mine_cells = sents.known_mines()
            
            for c in safe_cells:
                self.mark_safe(c)
            for c in mine_cells:
                self.mark_mine(c) 
                
        return
                
        
            
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #print(self.safes-(self.safes&self.moves_made))
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
            
        return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                cell = i,j
                possible_moves.add(cell)
                
        possible_moves = possible_moves - (self.mines|self.moves_made)
        if len(possible_moves) == 0:
            return None
        return random.sample(possible_moves,1)[0]
                
        #raise NotImplementedError
