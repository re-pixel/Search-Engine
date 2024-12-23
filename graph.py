class Graph():

    def __init__(self):
        self.outgoing = {}
        self.incoming = {}

    def add(self, node1, node2):
        if node1 in self.outgoing:
            self.outgoing[node1].append(node2)
        else:
            self.outgoing[node1] = [node2]
        
        if node2 in self.incoming:
            self.incoming[node2].append(node1)
        else:
            self.incoming[node2] = [node1]

    def get_references_to(self, node):
        return self.incoming[node] if node in self.incoming else None
    
    def get_number_of_references_to(self, node):
        return len(self.get_references_to(node)) if self.get_references_to(node) else 0

    def print_graph(self):
        print(self.outgoing)
        print(self.incoming)