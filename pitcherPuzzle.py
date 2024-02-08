#CSCI 6511
# Project 1: informed search with pitchers
#T. J. Foster 
# Must have cat input1..4.txt in same directory 
goalNumber = 0 #amount to be filled in the infinite pitcher


#create list to store pitcher options
pitcherOptions = dict() #tracks the quantities of different pitchers, sorted

def readPitcherFile (fileName):

    #print("in read pitcher file")
    #print("file name: ", fileName)
    pitcherFile = open(fileName, "r")
    pitcherOptionsString = pitcherFile.readline()
    # split up the pitcher options 
    global pitcherOptionsEnum # make them global so they are modified
    global pitcherOptions
    pitcherOptions = dict()# resets pitcher options each time 
    pitcherOptionsEnum = pitcherOptionsString.split(",") # interprets file line 
   
    #print(pitcherOptionsEnum)
    for number in pitcherOptionsEnum: #creates dictionary
        number = int(number)
        pitcherOptions[number] = 0 
    

    #print(pitcherOptions)

    goalNumber = pitcherFile.readline()

    print("goal number: ", goalNumber)

    computePath(goalNumber) #intial call 


def computePath(goalNumber): 
        sequenceString = "Sequence: " # record path 
        
        #print("compute Path, first value: ", goalNumber)
        minEstimate = 0 # values to pass into recursion for min path
        minKey = 0
        minTransferState = False
        first = True
        for value in reversed(pitcherOptions): 
           for value2 in reversed(pitcherOptions):#  I am not going by different actions, I have the option for regular or transfer
           # given a move, do the recursive function based on the remainder after that move has been done. 
        
                if value == value2: # calls the heuristic for using a pitcher without a transfer 
                    actionEstimate = heuristicFunction(goalNumber, value, False, 0) # does this account for the next action or the previous one
                elif value > value2: #accounts for an option that is a transfer
                    actionEstimate = heuristicFunction(goalNumber, value, True, value2) # does this account for the next action or the previous one

                if actionEstimate < minEstimate or first == True: # watch this OR statement
                    first = False #makes sure first estimate is not being compared to 0 for min value
                    minEstimate = actionEstimate
                    minKey = value
                    if value == value2:
                        minTransferKey = 0
                    else: 
                        minTransferKey = value2 # if the min is a transfer state, 
                
        totalSteps = computePathRecursive(minKey, minTransferKey, goalNumber, 0, sequenceString) #finding steps recursively

        print(totalSteps)


def computePathRecursive(key, transferKey, remaining, numSteps, sequenceString ): 

    #print("in computePath recursive")
    #print(" compute pathremaining", remaining)
    remaining = int(remaining)
    # do the move chosen by the previous node's heuristic function 
    oldRemaining = remaining # use this to see what the increment was for the purpose of the path string

    if transferKey == 0: # no transfer done, fill and pour
        if pitcherOptions[key] == 0: # not the case if a pitcher was the recipient of a transfer
            fillPitcher(key)
            numSteps +=1
        remaining -= pourPitcher(key)
        numSteps +=1
    else: 
        transferPitcher(key, transferKey)
        remaining -= pourPitcher(key)
        numSteps +=1
    # previous node's move done, steps recorded
    sequenceString = sequenceString + " "+ str(oldRemaining - remaining) # poured amount added to string

    # bases cases
    #print("remaining", remaining)
    if remaining == 0: 
        #answer found
        print(sequenceString)
        return numSteps
    elif remaining < int(min(pitcherOptions.keys())): # cannot fill the remaining with a single pitcher value
        print("no path")
        return -1
    elif remaining < 0:
        print("no path ")
        return -1
    # recursive case, choose next action
    else: 
        #iteratethrought pitcher options
        minEstimate = 0
        
        minKey = 0
        minTransferState = False
        first = True
        for value in reversed(pitcherOptions):
           for value2 in reversed(pitcherOptions):#  I am not going by different actions, I have the option for regular or transfer
           # given a move, do the recursive function based on the remainder after that move has been done. 
                #print("value checked: ", value)
                if value == value2: # calls the heuristic for using a pitcher without a transfer 
                    actionEstimate = heuristicFunction(remaining, value, False, 0) # does this account for the next action or the previous one
                elif value > value2: #accounts for an option that is a transfer, only allows a positive difference
                    actionEstimate = heuristicFunction(remaining, value, True, value2) # does this account for the next action or the previous one
                #print("action estimate before comparison", actionEstimate)
                if actionEstimate < minEstimate or first == True: # chooses action with smallest estimate > 0
                    first = False 
                    minEstimate = actionEstimate
                    minKey = value
                    if value == value2:
                        minTransferKey = 0
                    else: 
                        minTransferKey = value2 # if the min is a transfer state, 
             
        return computePathRecursive(minKey, minTransferKey, remaining, numSteps, sequenceString) #call recursive again 
                   


# pitcher water change actions   
def pourPitcher (key): # changes stored values and returns amount poured

    #print("in pourPitcher")
    #print("key: ", key)
    temp = pitcherOptions[key]
    #print("value poured out: ", temp)
    pitcherOptions[key] = 0
    return temp #return the amount poured to add to the running total for this recursion? 

def clearPitcher(key): #empty pitcher without filling goal
    #print("in clearPitcher")
    #print("key: ", key)
    pitcherOptions[key]=0

def fillPitcher(key): # fill pitcher that is empty 
    #print("in fillPitcher")
    #print("key: ", key)
    pitcherOptions[key] = int(key)


def transferPitcher (key1, key2): # first key is being poured into second key until second key is filled

    #print("in clearPitcher")
    #print("giver: ", key1, ". Reciever: ", key2)
    difference = pitcherOptions[key1] - pitcherOptions[key2]
    pitcherOptions[key2] = int(key2)
    pitcherOptions[key1] -= difference
    
def heuristicFunction (remaining, keyUsed, transferred, secondKey):
    
     
    #determine approximate cost given a starting point 
   # print("inside heuristic function")
    #print("heuristic remaining", remaining)
    if int(keyUsed) > int(remaining): # this node option is too big, cannot be the next step. Return arbitrarily large number
        # so it won't be picked
        #print("this node is too big")
        return 99999

    stepEstimate = 0
    #empties current full pitchers appropriately and then goes about fully filling
    # and emptying each type of pitcher based on category. 
    remaining = int(remaining)
    if transferred == True:
        remaining -= (keyUsed-secondKey)
    else: 
        remaining -= keyUsed
    #reamining estimate assumes the chosen move has already been made, both the fill and the pour, 
    # does measurements for remainder given that move
    #but number of steps will be counted in the recursive function that finds the path
    

    for currentKey in reversed(pitcherOptions): #iterate through pitcher options from biggest to smallest, find multiple of each 
    
        currentKey = int(currentKey)
        
        if currentKey < remaining: 
            if pitcherOptions[currentKey] == currentKey: #if this pitcher is already full, use a move to fill the goal 
                stepEstimate += 1
                #print(" full pour happened")
                remaining -= pitcherOptions[currentKey] #remainder being updated within heuristic, actual pitcher dictionary not being updated
                #print("remaining", remaining)
            elif pitcherOptions[currentKey] > 0: # if the pitcher is partially full, pour it into goal since it was there for a reason
                stepEstimate += 1 
                #print("partial pour happened")
                remaining -= pitcherOptions[currentKey] 
                #print("remaining: ", remaining)
            pitcherI = int(remaining / currentKey)
            #print("number of times key ", currentKey, " is used: ", pitcherI)
            remaining -= pitcherI * currentKey # reduce remaining by appropriate amount
            #print("end this pitcher end remaining ", remaining)
            stepEstimate += 2 * pitcherI
        else: 
            continue

    #print("inside pitcherTransferRemainder")nce
    # if multiples of whole pitchers no longer fit, estimate with possible differences of pitchers. 
    # using transfers 
    for K in pitcherOptions: #potentially larger one
            for L in pitcherOptions: #potentially smaller one 
                if K == L or K-L < 0:
                    break
                difference = K-L
                if difference == remaining or remaining %difference == 0:
                 
                    if pitcherOptions[K] != K: 
                            #fillPitcher(K)
                        stepEstimate += 1 #how to I count steps from here 
                    if pitcherOptions[L] != 0: # if the pitcher being poured into isn't empty 
                            #clearPitcher(L)
                        stepEstimate += 1
                        #transferPitcher(K, L)
                    stepEstimate +=2
                        #pourPitcher(K) # poured remaining portion of K to fill goalNumber
                # see if I can use a transfer between 2 to get the right number
    #print("heuristic step estimate ", stepEstimate)
    return stepEstimate




def main ():

    # unit testing code for different files
    readPitcherFile("cat input1.txt")
    readPitcherFile("cat input2.txt")
    readPitcherFile("cat input3.txt")
    readPitcherFile("cat input4.txt")
    #ensure global variables reset properly in between uses

main()