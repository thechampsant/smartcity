import os                       
import json                                             
from flask import Flask, request                       
from flask_pymongo import PyMongo
from collections import defaultdict
import pymongo
import json


app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://heroku_14nz5659:fh9bbo96241au1jdcko1nuucqi@ds341837.mlab.com:41837/heroku_14nz5659"
#mongodb://localhost:27017/testing"
mongo = PyMongo(app)  


with open('result.json') as f:
    file_data = json.load(f)

myList = []


@app.route("/first")
def index():
    return "<h1>Hello Azure!</h1>"

@app.route('/fetch')
def myABC():
    x = mongo.db.sensorTest.find({"accelorometerx":{"$gt":70},"IRsensor":{"$gt":11}})
    print(x)
    for res in x:
        print(res)
        myList.append(res)
    return json.dumps(myList)

@app.route('/store')
def myXYZ():
    y = mongo.db.sensorTest.insert_many(file_data)
    print(y)
    return 'ok'

@app.route('/health')
def shorDist():
    temp = request.json
    print("Source: " + temp["source"])
    print("Destination: " + temp["destination"])
    
    class Graph():
        def __init__(self):
            self.edges = defaultdict(list)
            self.weights = {}
    
        def add_edge(self, from_node, to_node, weight):
            # Note: assumes edges are bi-directional
            self.edges[from_node].append(to_node)
            self.edges[to_node].append(from_node)
            self.weights[(from_node, to_node)] = weight
            self.weights[(to_node, from_node)] = weight
    graph = Graph()
    
    edges = [
    ('A', 'B', 52),
    ('B', 'C', 40),
    ('B', 'D', 20),
    ('D', 'E', 25),
    ('D', 'H', 26),
    ('E', 'F', 5),
    ('E', 'H', 18),
    ('F', 'G', 22),
    ('H', 'I', 21),
    ('H', 'J', 23),
    ('H', 'L', 24),
    ('I', 'J', 10),
    ('J', 'K', 11),
    ('K', 'M', 32),
    ('K', 'L', 27),
    ('K', 'W', 28),
    ('L', 'Y', 13),
    ('Y', 'W', 7),
    ('Y', 'Z', 2),
    ('M', 'N', 12),
    ('M', '0', 31),
    ('N', 'P', 17),
    ('O', 'P', 33),
    ('O', 'W', 16),
    ('O', 'R', 14),
    ('O', 'X', 34),
    ('Q', 'R', 23),
    ('R', 'S', 19),
    ('R', 'V', 9),
    ('R', 'U', 8),
    ('R', 'T', 7),
    ('S', 'T', 15),
    ('T', 'U', 4),
    ('U', 'V', 3)
    
    ]

    for edge in edges:
        graph.add_edge(*edge)
        
    def dijsktra(graph, initial, end):
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
       
            path = path[::-1]   
        
        return path

    x = dijsktra(graph, temp["source"], temp["destination"])
    print(x)
    return json.dumps(x)

if __name__ == "__main__":
    app.run()

