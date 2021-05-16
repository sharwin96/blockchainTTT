import hashlib
import json,os
import random
import os.path
import sys

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint

cwd = os.getcwd()
os.chdir(cwd)
print("BOB is ready ....")

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
        blk = json.loads(content)
        blkNo = blk["TxID"]
        
        filename = "block{}".format(blkNo)

        message_content = (json.loads(jsonobj))

        #open a text file
        nsgfile = open(filename + ".txt","a")

        #write to the file 
        # nsgfile.write(str(message_content))
        nsgfile.write(content)
        nsgfile.close()

        
        ###processing the received data####
        
        #convert the data into json format
        jsondata = json.loads(jsonobj)
        
        blockContent = jsondata["message"]["content"]
        
        blockJson = json.loads(blockContent)
        
        print()
        print("============= processing ==============")
        print()
        
        print("block content : {}".format(blockJson))
        TxID = blockJson["TxID"] 
        thisnonce = blockJson["Nonce"]
        transaction = ""
        if (blockJson["Transaction"][0] == 'Alice'):
            transaction = blockJson["Transaction"][1]
            aliceBlocks.append(transaction)
            blksused.append(transaction)
        
        print("TxID : {}\nNonce : {}\nTransaction : {}\n".format(TxID,thisnonce,transaction)) 
        print("alice used = {}".format(aliceBlocks))
         
        
        #create data of the next block
        data = jsonobj 
        hashData = hashlib.sha256(data.encode()).hexdigest()
        tictactoeNumber = random.randint(1, 9)
        
        #check whether bob choose a vacant block
        diff = False
        while(diff == False):
            if tictactoeNumber not in blksused:
                diff = True
            else:
                tictactoeNumber = random.randint(1, 9)
        
        bobtransaction = ["Bob",tictactoeNumber]
        nonce = 0
        exit_ = True
        TxID = TxID + 1
        
        
        while(exit_):
            newhash = blockContent + str(nonce) # concat the last block with the nonce
            
            #hash the hashData
            hashData = hashlib.sha256(newhash.encode()).hexdigest()
        
            if (int(hashData[0:2],16) == 0):
                exit_ = False
            nonce = nonce + 1
            print(hashData[0:2])
            print(hashData)
            tx = json.dumps({'TxID': TxID , 'Hash':hashData + str(nonce),'Nonce':nonce,'Transaction': bobtransaction},sort_keys=False, indent=4, separators=(',', ': '))
            

        
    
        if(TxID == 2):
            bobBlocks.append(tictactoeNumber) #update the blocks bob had chosen
            blksused.append(tictactoeNumber) #update the blocks both players had choosen
            #sendblock(TxID,tx)
            sendblock(tx)
        if(TxID == 4):
            bobBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            #sendblock(TxID,tx)
            sendblock(tx)

        if(TxID == 6):
            bobBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            #sendblock(TxID,tx)
            sendblock(tx)
  
        if(TxID == 8):
            bobBlocks.append(tictactoeNumber)
            blksused.append(tictactoeNumber)
            #sendblock(TxID,tx)
            sendblock(tx)

        if(TxID == 10):
            
            sys.exit()
        
        
    
def my_publish_callback(envelope, status):
    print(envelope, status)
    
# def sendblock(TxID,tx):
def sendblock(tx):
    # filename = "block" + str(TxID)
    # file = open(filename + ".txt","w+")
    # file.write(tx)
    # file.close()
    
    #send the block to alice
    pubnub.publish().channel("Channel-qw613in8z").message({"sender": pnconfig.uuid, "content": tx})\
    .pn_async(my_publish_callback)

    
    
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-ae5fdf88-7009-11eb-9994-e2667f94577d"
pnconfig.publish_key = "pub-c-26c42884-3c7c-4039-864d-7cbae5396fc7"

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())

aliceBlocks = []
bobBlocks = []
blksused = []

data = pubnub.subscribe()\
    .channels("Channel-qw613in8z")\
    .with_presence()\
    .execute()
