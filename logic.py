"""Handles the graph object and chooses paths"""
import json
import random

#read graph from config and store as dict
def load_graph(path):
    dict = None
    with open(path, "r") as f:
        dict = json.load(f)
    return dict

def get_random_next(graph, key):
    #print(graph[key])
    i = len(graph[key])
    if i == 1:
        return graph[key][0]

    return graph[key][random.randint(0, i-1)]

#generate valid walks when asked
def walk(graph):
    out = []
    keys = list(graph.keys())
    start = keys[0]
    if start == "graph":
        graph = graph["graph"]
        keys = list(graph.keys())
        start = keys[0]
    out.append(start)
    random_next = start
    while True:
        random_next = get_random_next(graph, random_next)
        if random_next == start:
            return out
        out.append(random_next)






#export files when asked
def export(sequence):
    pass

def main():
    d = load_graph("./demos/democonfig.json")
    print(walk(d["graph"]))

if __name__ == "__main__":
    main()