def build_dict_from_file(filename):
    dict = {}

    print("reading dictionary...")

    with open(filename) as f:
        words = f.readlines()
    
    for word in words:
        word = word.strip().lower()
        wordAlphabetical = "".join(sorted(word)).strip()
        
        if(wordAlphabetical not in dict):
            dict[wordAlphabetical] = set()
        dict[wordAlphabetical].add(word)

    print("successfully read dictionary")

    return dict

def is_word(word, dict):
    wordAlphabetical = "".join(sorted(word))
    if wordAlphabetical in dict:
        if word in dict[wordAlphabetical]:
            return True
    return False

def unscramble(s, dict):
    wordAlphabetical = "".join(sorted(s))
    words = set()
    if wordAlphabetical in dict:
        words = dict[wordAlphabetical]
    return words

def build_suffix_tree(word_list):
    suffix_tree = {}
    for word in word_list:
        sub_tree = suffix_tree
        for c in word:
            if c in sub_tree:
                sub_tree = sub_tree[c]
            else:
                sub_tree[c] = {}
                sub_tree = sub_tree[c]
                
    
    return suffix_tree

