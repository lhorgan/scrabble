class Scrabble:
    def __init__(self):
        self.value_board = self.get_value_board()
        self.dct = self.build_dct_from_file("dict.txt")
        self.board = []
        self.tiles = ["ABCDEFG"]

        self.tile_values = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1,
                            "f": 4, "g": 2, "h": 4, "i": 1, "j": 8,
                            "k": 5, "l": 1, "m": 3, "n": 1, "o": 1,
                            "p": 3, "q": 10, "r": 1, "s": 1, "t": 1,
                            "u": 1, "v": 1, "w": 4, "x": 8, "y": 4,
                            "z": 10}

        for i in range(15):
            self.board.append([])
            for j in range(15):
                self.board[i].append("*")

    def build_dct_from_file(self, filename):
        print("reading dctionary...")
        with open(filename) as f:
            words = f.readlines()
        
        words = [word.strip().lower() for word in words]
        suffix_tree = self.build_suffix_tree(words)

        return suffix_tree

    def is_word(self, s, dct=None):
        dct = self.dct if dct is None else dct

        node = self.get_node(s, dct)
        if node:
            return node[1]
        return False

    def get_node(self, s, dct):
        dct = self.dct if dct is None else dct

        st = dct
        super_tree = None
        for c in s:
            if c in st:
                super_tree = st[c]
                st = st[c][0]
            else:
                return None
        return super_tree

    def get_all_words(self, letters, template, dct=None):
        dct = self.dct if dct is None else dct

        stack = []

        if template[0] == "*":
            for i in range(len(letters)):
                node = self.get_node(letters[i], dct)
                rest = letters[:i] + letters[i+1:]
                stack.append([letters[i], rest, node])
        else:
            node = self.get_node(template[0], dct)
            rest = letters
            stack.append([template[0], rest, node])
        
        words = set()
        while len(stack) > 0:
            seq, rest, node = stack.pop()
            if node[1]:
                words.add(seq)

            if len(seq) < len(template):
                if template[len(seq)] == "*":
                    for i in range(len(rest)):
                        new_first = rest[i]
                        new_rest = rest[:i] + rest[i+1:]
                        new_node = self.get_node(new_first, node[0])
                        if new_node:
                            stack.append([seq + new_first, new_rest, new_node])
                else:
                    new_first = template[len(seq)]
                    new_rest = rest
                    new_node = self.get_node(new_first, node[0])
                    if new_node:
                        stack.append([seq + new_first, new_rest, new_node])
        
        return words

    def build_suffix_tree(self, word_list):
        suffix_tree = {}
        for word in word_list:
            sub_tree = suffix_tree
            for i in range(len(word)):
                c = word[i]
                super_tree = sub_tree
                if c in sub_tree:
                    sub_tree = sub_tree[c][0]
                else:
                    sub_tree[c] = [{}, False]
                    sub_tree = sub_tree[c][0]
                if i == len(word) - 1:
                    super_tree[c][1] = True
        return suffix_tree
    
    def get_legal_words(self, i, j):
        template_str = "".join(self.board[i][j:15])
        print(template_str)
        words = self.get_all_words(self.tiles, template_str)
        print(words)

        print("\n\n")

        legal_words = {}

        for word in words:
            if j+len(word) < 15 and self.board[i][j+len(word)] == "*": # don't go RIGHT NEXT to an existing word
                score = self.score_word(word)#self.place_word(word, i, j)
                if score > 0:
                    legal_words[word] = score
                #self.place_word(template_str, i, j)
        
        return legal_words

    def pick_best_move(self):
        best_i = 0
        best_j = 0
        best_word = ""
        best_word_score = -1

        for i in range(15):
            for j in range(15):
                legal_words = self.get_legal_words(i, j)
                for w in legal_words:
                    #print(w + ", " + str(legal_words[w]))
                    if legal_words[w] > best_word_score:
                        best_word_score = legal_words[w]
                        best_word_i = i
                        best_word_j = j
                        best_word = w
        
        print("%s %i (%i, %i)" % (best_word,best_word_score,  best_word_i, best_word_j))
        return best_word
                

    def place_word(self, word, row, col):
        word_ind = 0
        score = 0

        # for i in range(col, 15):
        #     if word_ind >= len(word):
        #         break

        #     if self.board[row][i] == "*":
        #         up_str = ""
        #         down_str = ""
        #         for j in range(i-1, -1, -1):
        #             if self.board[j][i] == "*":
        #                 break
        #             up_str += self.board[j][i]
        #         up_str = up_str[::-1] 
        #         for j in range(i+1, 15):
        #             if self.board[j][i] == "*":
        #                 break
        #             down_str += self.board[j][i]
        #         new_word = up_str + word[word_ind] + down_str
        #         if len(new_word) > 1 and self.is_word(new_word):
        #             score += self.score_word(new_word)
        
        #     word_ind += 1

        return self.score_word(word)

    def rotate_board(self):
        new_board = []
        for i in range(15):
            new_board.append([])
            for j in range(15):
                new_board[i].append("*")

        for i in range(15):
            for j in range(15):
                new_board[i][j] = self.board[j][i]
    
    def score_word(self, word):
        score = 0
        for c in word:
            score += self.tile_values[c]
        return score

    def get_value_board(self):
        ST = 1
        DL = 2
        DW = 3
        TL = 4
        TW = 5
        board = [[TW, ST, ST, DL, ST, ST, ST, TW, ST, ST, ST, DL, ST, ST, TW],
                 [ST, DW, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, DW, ST],
                 [ST, ST, DW, ST, ST, ST, DL, ST, DL, ST, ST, ST, DW, ST, ST],
                 [DL, ST, ST, DW, ST, ST, ST, DL, ST, ST, ST, DW, ST, ST, DL],
                 [ST, ST, ST, ST, DW, ST, ST, ST, ST, ST, DW, ST, ST, ST, ST],
                 [ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST],
                 [ST, ST, DL, ST, ST, ST, DL, ST, DL, ST, ST, ST, DL, ST, ST],
                 [TW, ST, ST, DL, ST, ST, ST, DW, ST, ST, ST, DL, ST, ST, TW],
                 [ST, ST, DL, ST, ST, ST, DL, ST, DL, ST, ST, ST, DL, ST, ST],
                 [ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST],
                 [ST, ST, ST, ST, DW, ST, ST, ST, ST, ST, DW, ST, ST, ST, ST],
                 [DL, ST, ST, DW, ST, ST, ST, DL, ST, ST, ST, DW, ST, ST, DL],
                 [ST, ST, DW, ST, ST, ST, DL, ST, DL, ST, ST, ST, DW, ST, ST],
                 [ST, DW, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, DW, ST],
                 [TW, ST, ST, DL, ST, ST, ST, TW, ST, ST, ST, DL, ST, ST, TW]]

        return board