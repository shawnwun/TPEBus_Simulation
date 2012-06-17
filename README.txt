每個 iteration 一分鐘
* 選路線忽略轉車

Map: Graph
    給 bus 參考的，包含交通狀況，邊緣 edge, node 資訊
    
Node:
    Clients queue
    Bus queue
    路線表:  對任意一個點根據一個 bus configuration 的 cost

Client Manager:
    Need to configure
    處理 client 的誕生

Bus Manager:
    Data ---------------------------------
    所有公車路線:   a bunch of list of nodes
    每個公車路線的班距:	iteration


Bus Class:
    Data ---------------------------------
    BusID:	(route, number)
    路線圖:	node list read from data
    clients:	a list of Client obj 
    Life time:	start from 0, every iteration +1
    
    MetaData:	{'from': 
		 'to':
		 'at':
		 'dist':
		 'speed':}    

    --------------------------------------
    Behavior:	遇到起點直接消失，遇到終點返路線
		到每個 node, 呼叫每個 client 滾蛋下車
		根據該段路況調整速度, (20,30,40,50) km/hr
		忽略停車時間
		經過路線上的 node 必停

Client Class:
    位置:	(目前位置，終點)
    
    Behavior:	讀該 node 紀錄的路線表, 決定上哪班車
    Life time:	start from 0, every iteration +1
    預計多遠:	const, init 決定


/**** Over all  flow ****/
建好 map 資訊，路況，公車路線
先根據每個 node 對任一個 node 算 shortest path, 記錄為該 node 的路線表
Bus manager 先 setup

每個 iteration:
    全部現有公車 move(若遇站則呼叫下車), 判斷是否到站, 如果到起點消失(記錄cost)
    Bus manager 誕生公車 (start), 塞入 node
    Client Manager 誕生Client, 塞入 node
    對於每個 node:
	呼叫 client 消失 => 記錄 cost
	若不消失請選車
    

