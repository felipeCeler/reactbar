

import osc

osc.init()        
osc.sendMsg("/tuio/msg", ["mark","40005"], '127.0.0.1',40004)