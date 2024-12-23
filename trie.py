class TrieNode():
    def __init__(self):
        self.freq = 0
        self.pages = {}
        self.children = {}
        self.end = False

    def __str__(self):
        return str(self.children)

class Trie():
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, page, position):
        if len(word) > 20:
            return
        word = word.lower()
        node = self.root
        for char in word:
            if not char.isalnum() and char != '-':
                continue
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.freq += 1
        if page not in node.pages:
            node.pages[page] = [position]
        else:
            node.pages[page].append(position)
        node.end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        if node.end:
            res = node.pages
            return res
        return False
    
    def find_similar_query(self, query):
        node = self.root
        index = 0
        for i in range(len(query)):
            if node != self.root and (query[i] not in node.children or node.freq < 10):
                index = i-1
                break
            node = node.children[query[i]]

        recommendations = self.autocomplete(query[:index])
        return recommendations[0][0]

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        suffixes = []
        amount_of_pages = []

        def find_suffixes(node, suffix):
            if not node.children:
                return
            for char in node.children:
                suffix += char
                if node.children[char].end:
                    amount_of_pages.append(len(node.children[char].pages))
                    suffixes.append(suffix)
                find_suffixes(node.children[char], suffix)
                suffix = suffix[:-1]

        find_suffixes(node, '')
        recommendations = [prefix+suffix for suffix in suffixes]
        result = [[recommendations[i], amount_of_pages[i]] for i in range(len(recommendations))]
        result.sort(key=lambda x:-x[1])
        return result            
      
    def print_trie(self, node=None, prefix=''):
        if node is None:
            node = self.root

        for char, child_node in node.children.items():
            if child_node.end:
                print(f"{prefix}{char}*")
            else:
                print(f"{prefix}{char}")
            self.print_trie(child_node, prefix + char)