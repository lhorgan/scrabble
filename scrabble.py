def build_dct_from_file(filename):
    print("reading dctionary...")
    with open(filename) as f:
        words = f.readlines()
    
    words = [word.strip().lower() for word in words]
    suffix_tree = build_suffix_tree(words)

    return suffix_tree

def is_word(s, dct):
    node = get_node(s, dct)
    if node:
        return node[1]
    return False

def get_node(s, dct):
    st = dct
    super_tree = None
    for c in s:
        if c in st:
            super_tree = st[c]
            st = st[c][0]
        else:
            return None
    return super_tree

def get_all_words(letters, dct):
    stack = []
    for i in range(len(letters)):
        node = get_node(letters[i], dct)
        rest = letters[:i] + letters[i+1:]
        stack.append([letters[i], rest, node])
    
    words = set()
    while len(stack) > 0:
        seq, rest, node = stack.pop()
        #print(seq + ", "  + rest)
        if node[1]:
            words.add(seq)
        for i in range(len(rest)):
            new_first = rest[i]
            new_rest = rest[:i] + rest[i+1:]
            #print("trying " + new_first)
            new_node = get_node(new_first, node[0])
            #print(new_node)
            if new_node:
                stack.append([seq + new_first, new_rest, new_node])
    
    return words

def get_all_words2(letters, template, dct):
    stack = []

    if template[0] == "*":
        for i in range(len(letters)):
            node = get_node(letters[i], dct)
            rest = letters[:i] + letters[i+1:]
            stack.append([letters[i], rest, node])
    else:
        node = get_node(template[0], dct)
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
                    new_node = get_node(new_first, node[0])
                    if new_node:
                        stack.append([seq + new_first, new_rest, new_node])
            else:
                new_first = template[len(seq)]
                new_rest = rest
                new_node = get_node(new_first, node[0])
                if new_node:
                    stack.append([seq + new_first, new_rest, new_node])
    
    return words

def build_suffix_tree(word_list):
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

board = []

