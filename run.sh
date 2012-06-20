#!/bin/bash


#python src/simulation.py TPMap_nodes.txt TPMap_edges.txt traffic/weekend_1800_01.txt route/Baseline.txt interval/Baseline.txt 10000 morning

#python src/simulation.py TPMap_nodes.txt TPMap_edges.txt traffic/weekend_1800_01.txt route/Chessboard.txt interval/Chessboard.txt 10000 morning

python src/simulation.py TPMap_nodes.txt TPMap_edges.txt traffic/weekend_1800_01.txt route/Allpair.txt interval/Allpair.txt 10000 morning

