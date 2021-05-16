import hashlib
import json,os
import os.path
import random
import os.path
import sys

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint

cwd = os.getcwd()
print(cwd)
os.chdir(cwd)

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        pprint(message.__dict__)
        y = (message.__dict__)


        jsonobj = json.dumps(y)
        
        msgData = json.loads(jsonobj)
        content = msgData["message"]["content"]
        blkNo = json.loads(content)
        
        receivedTxID = blkNo["TxID"]
        
        filename = "block{}".format(receivedTxID)

        message_content = (json.loads(jsonobj))

        # #open a text file
        nsgfile = open(filename + ".txt","a")

        #write to the file 
        nsgfile.write(content)
        nsgfile.close()
        
    
        ###processing the received data####
        
        #convert the data into json format
        jsondata = json.loads(jsonobj)
        
        blockContent = jsondata["message"]["content"] #this is the raw json data in string format
        
        blockJson = json.loads(blockContent) #this is the raw json data in json format
        
        print()
        print("============= processing ==============")
        print()
        
        print("block content : {}".format(blockJson))
        nextTxID = blockJson["TxID"]
        nextnonce = blockJson["Nonce"]
        transaction = ""
        if (blockJson["Transaction"][0] == 'Bob'):
            transaction = blockJson["Transaction"][1]
            bobBlocks.append(transaction)
            blksused.append(transaction)
        
        print("TxID : {}\nNonce : {}\nTransaction : {}\n".format(nextTxID,nextnonce,transaction)) 
        print("bob used = {}".format(bobBlocks))
        
        #create data of the next block
        
        tictactoeNumber = random.randint(1, 9)    
        
        #verify that the alice chooses a vacant block
        diff = False
        while(diff == False):
            if tictactoeNumber not in blksused:
                diff = True
            else:
                tictactoeNumber = random.randint(1, 9)
        
        alicetransaction = ["Alice",tictactoeNumber]
        nextnonce = nextnonce + 1
        nonce = 0
        exit_ = True
        nextTxID = nextTxID + 1
        
        while( exit_ ):
            newhash = blockContent + str(nonce) #concat the previous block with nonce 
            
            #rehash the hashData
            hashData = hashlib.sha256(newhash.encode()).hexdigest()
            if (int(hashData[0:2],16) == 0):
                exit_ = False
            nonce = nonce + 1
            print(hashData[0:2])
            print(hashData)
            
            tx = json.dumps({'TxID': nextTxID , 'Hash':hashData,'Nonce':nonce,'Transaction': alicetransaction},sort_keys=False, indent=4, separators=(',', ': '))
            
    
        
        if (nextTxID == 3):
            aliceBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            # sendblock(nextTxID,tx)
            sendblock(tx)
        if (nextTxID == 5): 
            aliceBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            # sendblock(nextTxID,tx)
            sendblock(tx)
        if (nextTxID == 7):
            aliceBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            # sendblock(nextTxID,tx)
            sendblock(tx)
        if (nextTxID == 9):
            aliceBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            # sendblock(nextTxID,tx)
            sendblock(tx)
            pubnub.unsubscribe_all()
        if (nextTxID == 10):
            #pubnub.unsubscribe_all()
            sys.exit()
        
        

        
def startingblock():
    
    TxID= 0
    nonce = 0
    TxID = TxID + 1
    
    
    f = open("block"+str(TxID-1)+".json","r")
    data = f.read()
    f.close()
    
    #writing block0.txt
    file = open("block"+str(TxID-1)+".txt","w+")
    file.write(data)
    file.close()
    
    
    hashData = hashlib.sha256(data.encode()).hexdigest() # hash block0.json data
    tictactoeNumber = random.randint(1, 9)
    aliceBlocks.append(tictactoeNumber)
    blksused.append(tictactoeNumber)
    transaction = ["Alice",tictactoeNumber]
   
    exit_ = True
    while(exit_):
        newhash = hashData + str(nonce) #concat the previous block with nonce
        
        #rehash the hashData
        hashData = hashlib.sha256(newhash.encode()).hexdigest()
        
        if (int(hashData[0:2],16) == 0):
            exit_ = False
        print(hashData[0:2]) #prints out the first 2 hexadecimal indexs
        print(hashData)
        nonce = nonce + 1
       
        txdata = json.dumps({'TxID': TxID , 'Hash':hashData ,'Nonce':nonce,'Transaction': transaction},sort_keys=False, indent=4, separators=(',', ': '))
        
    
    fileName = "block" + str(TxID)
    file = open(fileName+".txt","w+")
    file.write(txdata)
    file.close()
    print("{}.txt created...".format(fileName))
    print("blocks used = {}".format(aliceBlocks))
    
    pubnub.publish()\
    .channel("Channel-qw613in8z")\
    .message({"sender": pnconfig.uuid, "content": txdata})\
    .pn_async(my_publish_callback)
        
  
        

def my_publish_callback(envelope, status):
    print(envelope, status)

    
# def sendblock(TxID,tx):
def sendblock(tx):
    # filename = "block" + str(TxID)
    # file = open(filename + ".txt","w+")
    # file.write(tx)
    # file.close()
    # print("{}.txt created !!".format(filename))
    
    #send the block to alice
    pubnub.publish().channel("Channel-qw613in8z").message({"sender": pnconfig.uuid, "content": tx})\
    .pn_async(my_publish_callback)



aliceBlocks = []
bobBlocks = []
blksused = []
TxID= 0
nonce = 0
TxID = TxID + 1


pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-ae5fdf88-7009-11eb-9994-e2667f94577d"
pnconfig.publish_key = "pub-c-26c42884-3c7c-4039-864d-7cbae5396fc7"

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())

startingblock()
  
    
pubnub.subscribe()\
.channels("Channel-qw613in8z")\
.with_presence()\
.execute()
 

