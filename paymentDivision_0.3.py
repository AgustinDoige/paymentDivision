"""
Paying Division:
An algorithm that asks for a list of people and what they bought at a get together, the price, 
and if someone didn't consume something in case they shouldn't pay for that, and calculates
who should pay who.

One property this algorithm has is that it minimizes* the amount of diferent payments the whole group
will end up doing. 
For example:
        Scenario A: 
            p1 pays $40 to p3
            p1 pays $40 to p4
            p2 pays $40 to p3
            p2 pays $40 to p4
        Scenario B:
            p1 pays $80 to p3
            p2 pays $80 to p4
    While both scenarios are equal in the sense that the debts of everyone are the same
    The algorithm would favor Scenario B that has a solution with less individual paymentss.
*:I think (:I)

Idea From: Calixto
Code From: Agustin Marcelo Dominguez (ADoige)
Sep 2019
"""

#CONSTANTS:
DIGIT_ROUNDING_OF_CURRENCY = 1 #This means that 250.412 will be rounded to 250.40. Original: 1

#AUX FUNCTIONS
def raw_cToC(raw_c):
    # Takes the raw console input and 
    # returns a tuple with the name and it's price. Very weak
    # PROBLEMS: The number has to be separated by a space and have no other symbols or period at the end
    purchase = raw_c.split()
    price = purchase.pop(len(purchase)-1)
    purchase = ' '.join(purchase)
    return (purchase,float(price))

def sortedDictionary(dictionary):
    # Returns a List with each person sorted by how much they spent, from largest sum to smallest
    # List Structrure: (moneyPayed,PersonName,PersonDictionary)
    ls = []
    for person in dictionary:
        ls.append([dictionary[person]['credit'],dictionary[person]])
    return sorted(ls,key=lambda x: x[0],reverse=True)

def insertInOrder(personDic,sortedList):
    """Used in calculateDebts(). Explanation there"""
    returnList = sortedList
    for i in range(len(sortedList)):
        if (personDic['credit'] >= returnList[i][0]):
            returnList.insert(i,(personDic['credit'],personDic))
            return returnList
    #It should not get here because by algorithm, personDic['credit'] should be positive
    #but the person with the most debt should be, at maximum, 0.
    raise NameError('owedPer Credit is less than the last entry of sortedls. Something wrong with algorithm')

####
#MAIN PIPE FUNCTIONS
def getParticipants():
    # Asks the user to enter participants. It saves in "participants". Case Insensitive.
    participants = []
    print("Enter the names of every participant, one below the other:")
    print("(Make 'end' the last entry)")
    while(True):
        inp = input(">> ").lower()
        if (inp=='end'):
            break
        else:
            participants.append(inp)
    print("\n")
    return participants

#>>>>
def getPurchases(participantes):
    """Returns a the first step of the purchase dictionary,
    with each person and what they bought with price.

    Structure Example:
    {
        'tomas': {'name': 'tomas', 'purchases': {'itema': 100.0, 'itemb': 200.0}}, 
        'damian': {'name': 'damian', 'purchases': {}}, 
        'laura': {'name': 'laura', 'purchases': {'itemc': 250.0}}
    }
    NOTE: name is saved for when each value of the dictionary is taken from the dictionary for sorting.
        so the original dictionary can be reconstructed"""

    print("Enter what each person bought and it's price as a plain number (without'$', decimals are allowed)")
    print("Enter 'end' if the person mentioned didn't buy anything or as the last entry of each person")
    purchases = {} #General dictionary that contains each personl dictionary of purchases
    boughtItems = {} #separate dictionary that will be needed for the next function, but is more effective to create now
    for p in participantes:  #p := person
        ppurchases = {'name':p,'purchases':{}} #Personl Dict of person p
        print(" {} bought: ".format(p.capitalize()),end='')
        print("('end' to terminate purchases of {})".format(p.capitalize()))
        while(True):
            raw_c = input(">> ").lower()
            if (raw_c == 'end'):
                break
            itemTuple = raw_cToC(raw_c) #Call to aux func
            boughtItems[itemTuple[0]] = itemTuple[1] #itemTuple[0] := itemName // #itemTuple[1] := itemPrice
            ppurchases['purchases'][itemTuple[0]] = itemTuple[1]
        purchases[p] = ppurchases
    return (purchases,boughtItems)

#>>>>
def getExceptions(compTupl):
    """Adds information to the main dictionary with the exceptions of what each person didn't consume"""
    compDic = compTupl[0] #Main Dict
    boughtItDic = compTupl[1]
    ans = input("Did everyone consume everything? (y/n): ").lower()
    if (ans == 'y'):
        return (compDic,compTupl[1]) #No exceptions are added
    for per in compDic:
        compDic[per]['exceptions'] = []
        ans = input("\tDid {} not consume something? (y/n): ".format(per.capitalize())).lower()
        if (ans == 'n'):
            continue
        print("'end' to terminate {} exceptions before".format(per.capitalize()))
        for it in boughtItDic:
            ans = input("\t\tDid {} avoided consuming {}? (y/n/end): ".format(per.capitalize(),it)).lower()
            if (ans=='end'):
                break
            elif (ans=='n'):
                continue
            else:
                compDic[per]['exceptions'].append(it)
    return (compDic,compTupl[1])

def calculateDebts(exceptionsTupl):
    """CENTRAL function:
    Takes the dictioanry with purchases and exceptions and computes how much money each person
    owes to the group. This is saved in 'debt'. It then calculates how much each person is owed by the group.
    This is saved in 'owed'.
    Then it fuses both vairables in the one called 'credit' where person that has a positive number
    is still being owed something by the group. negative credit means that the person sill owes money and 
    'credit' == 0 means person is square.

    Finally, 'payls' saves the instances of payment there should be so the group gets even.

    NOTE: The thing with 2 variables fusing into one comes from the first version of the program, but then
    I figured that it would be better for the changing of money to have a single variable, but I already
    had half of the function written...
    """
    centralDict = exceptionsTupl[0]
    itCompradosDic = exceptionsTupl[1]

    consumedDict = {} #Important Aux Dictionary that saves who consumed what item; used for the exceptions computation.
    for itC in itCompradosDic:
        consumedDict[itC] = []

    for person in centralDict:
        suma = sum(centralDict[person]['purchases'].values())
        centralDict[person]['owed'] = suma
        centralDict[person]['debt'] = 0
        for product in itCompradosDic:
            try: #This is used because when no exceptions are there, there will not be an 'exceptions' key
                if product in centralDict[person]['exceptions']:
                    pass
                else:
                    consumedDict[product].append(person)
            except KeyError:
                consumedDict[product].append(person) #No exceptions means everyone consumes everything
                #NOTE: This part could be changed so it doesn't try every time but instead if the first try fails then the dictionary consumedDict should be everyperson for every item. That would be slightly faster
    
    for itm in consumedDict:
        temp = itCompradosDic[itm]/len(consumedDict[itm]) #This is the value of each purchase divided by the amount of people that consumed that specific purchase
        for per in consumedDict[itm]: #Then it adds that division of that item to every person that consumed it
            centralDict[per]['debt'] += temp    
    del temp
    
    for per in centralDict: #THIS is the fusion of the 'owed' and 'debt' keys into 'credit'. 
        # It deletes the previous keys.
        temp1 = centralDict[per]['owed']
        temp2 = centralDict[per]['debt']
        del centralDict[per]['owed']
        del centralDict[per]['debt']
        centralDict[per]['credit'] = round(temp1-temp2,ndigits=DIGIT_ROUNDING_OF_CURRENCY)
        centralDict[per]['payls'] = {} #Creates the variable that will store the final payments that would be made
    del temp1
    del temp2

    sortedls = sortedDictionary(centralDict)
    finalDictionary = {}
    while(True):
        if (len(sortedls)<2):
            if (len(sortedls) == 1):
                finalDictionary[sortedls[0][1]['name']] = sortedls[0][1]
            break
        
        #Important. The previous list gets progresively smaller
        owedPer = sortedls.pop(0)
        debtor = sortedls.pop(-1)

        #Structure of owedPer and debtor = ( credit , personalDictionary )
        # So owedPer[0] is a num that says how much that person is owed (by algorithm's behavior, positive) 
        # And debtor[0] the same but what that person owes (to the group. Also by alg behavior, debtor[0]<=0)
        
        if (owedPer[0] == abs(debtor[0])): 
            #Specific case where what a person owes is exactly that the other is owed
            debtor[1]['payls'][owedPer[1]['name']] = abs(debtor[1]['credit']) #saves the 'virtual' Payment
            #Both people get 0 on their credit, so the variable is no longer needed:
            del owedPer[1]['credit']
            del debtor[1]['credit']
            #Both people get added to the final dict and none are re-inserted into the sortedLs:
            finalDictionary[owedPer[1]['name']] = owedPer[1]
            finalDictionary[debtor[1]['name']] = debtor[1]

        elif owedPer[0] < abs(debtor[0]):
            #Case where the debtor owes MORE than what 'owedPer' is actually owed
            #The debtor gets deducted the amount they virtually 'pay' to the other:
            debtor[1]['credit'] = abs(debtor[1]['credit'])-owedPer[1]['credit']
            debtor[1]['payls'][owedPer[1]['name']] = owedPer[1]['credit'] #The virtual payment gets added
            del owedPer[1]['credit'] #owedPer is completely payed off
            finalDictionary[owedPer[1]['name']] = owedPer[1] # Only owedPer was done, so only they get added to the finalDictionary
            sortedls.append((debtor[1]['credit'],debtor[1])) # debtor still owes something so they get back into the list.
        
        else:
            #Case where the debtor owes LESS than what 'owedPer' is actually owed
            #The owed Person gets deducted the amount they virtually get paid by the debtor:
            owedPer[1]['credit'] = owedPer[1]['credit']-abs(debtor[1]['credit'])
            debtor[1]['payls'][owedPer[1]['name']] = abs(debtor[1]['credit']) #The virtual payment gets added
            del debtor[1]['credit'] #debtor pays their debt completely
            finalDictionary[debtor[1]['name']] = debtor[1] #debtor is done, so they get added to the final dict
            sortedls = insertInOrder(owedPer[1],sortedls) #owedPer is not done, so they get re-entered into the sorted list.
            """NOTE:The use of insertInOrder instead of a basic sortedls.insert(0,...) is because
                    after a payment, there might be the case where another person is now the one
                    with the largest owed amount; and because of the desired property of the algorithm,
                    the decreasing order of the debts should remain."""

    return finalDictionary

#####################
#####################
def main():
    # It's a pipe with each function adding more information to the dictionary and passing it along
    # a la siguiente funcion:
    # getParticipants >| getPurchases >| getExceptions >| calculateDebts
    diccionarioFinal = calculateDebts(getExceptions(getPurchases(getParticipants())))
    for person1 in diccionarioFinal:
        if diccionarioFinal[person1]['payls'] != {}:
            for person2 in diccionarioFinal[person1]['payls']:
                print("--> {} should pay ${} to {}.".format(person1.capitalize(),diccionarioFinal[person1]['payls'][person2],person2.capitalize()))

main()