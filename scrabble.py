class Scrabble:
    def __init__(self):
        self.board = self.get_board()
        self.dct = self.build_dct_from_file("dict.txt")

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

    def get_board(self):
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
                 [TW, ST, ST, DL, ST, ST, ST, ST, ST, ST, ST, DL, ST, ST, TW],
                 [ST, ST, DL, ST, ST, ST, DL, ST, DL, ST, ST, ST, DL, ST, ST],
                 [ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, TL, ST],
                 [ST, ST, ST, ST, DW, ST, ST, ST, ST, ST, DW, ST, ST, ST, ST],
                 [DL, ST, ST, DW, ST, ST, ST, DL, ST, ST, ST, DW, ST, ST, DL],
                 [ST, ST, DW, ST, ST, ST, DL, ST, DL, ST, ST, ST, DW, ST, ST],
                 [ST, DW, ST, ST, ST, TL, ST, ST, ST, TL, ST, ST, ST, DW, ST],
                 [TW, ST, ST, DL, ST, ST, ST, TW, ST, ST, ST, DL, ST, ST, TW]]

        return board