from re import sub
from math import log10

#Terminology:
#
#String Pattern: The input that is to be compared against to check whether the substring exists within.  
#For example, if I want to check if the word 'dog' is in 'The dog is tired.', the latter sentence is considered
#as the string pattern.
#
#Substring: The input that the user wants to know whether it exists within the string pattern.  In the above
#example, it would be the word 'dog'/


class ListInfo:
    def __init__(self,divided,index):
        self.divided = divided
        self.index = index

def score(main, substring):
    result = compare(main, substring)
    return result
#     if result > 2*len(substring) or result is 0:
#         return 0
#     else:
#         #return int(100 - 76.87 * log10(result*10/len(substring)))
#         return result
    

def compare(string, substring):
    #The input is initially filtered, than it is partitioned.  The number of partitions is dependent on
    #whether an answer is found and also the length of the substring.  If a match is found, it will stop
    #otherwise, it procedes with latter letter partitions until the algorithm knows there can be no
    #more possible matches.
    string = filterstringpattern(string)
    
    #This sequence will parse every character in the substring, than create a dictionary with values
    uniquelettervalues = {}
    i = 1
    for char in substring:
        if char not in uniquelettervalues.keys():
            uniquelettervalues[char] = i
            i += 1
    
    substringhashvalues = []
    
    #retrieves the score value associated with the letter
    def getlettervalue(l):
        if l not in uniquelettervalues.keys():
            return 0
        else:
            return uniquelettervalues[l]
    
    #Now the substring needs to be interpreted as a score, using the above scoring convention in uniquelettervalues.
    for j in range(0,len(substring)):
        
        #Priority in terms of unit, tens, and hundreds
        #Hundreds, units, tens
        try:
            if j is 0:
                #check previous digit, which you will assume is zero
                #it will indicate that search is off, so whenever the search is flipped on, then the hashvalue is automatically
                #set to 1
                substringhashvalues.append(1)
                
            else:
                if substringhashvalues[j-1] >= 10:
                    unitvalue = substringhashvalues[j-1]%10
                else:
                    unitvalue = substringhashvalues[j-1]
                substringhashvalues.append(unitvalue + 10*uniquelettervalues[substring[j+1]] + 100*uniquelettervalues[substring[j]])
                
        except IndexError:
            #in this case you assume that the following letter is a blank, since it would be the following letter in the string
            #'blank' letters are associated with a score of 0
            if substringhashvalues[j-1] >= 10:
                unitvalue = substringhashvalues[j-1]%10
            else:
                unitvalue = substringhashvalues[j-1]            
            substringhashvalues.append(unitvalue + 100*uniquelettervalues[substring[j]])
        
#         print(substringhashvalues)
    objectivescore = 0
    #Scoring will work on the following basis:
    
    #For the first character:
    #Hundreds: 0 if exists substring, 1 if not
    #Tens: 0 if exists in substring, 1 if not
    
    #For the last character:
    #Hundreds: 0 if matching, 1 if not
    #Tens: 0 if matching, 1 if not
    #Units: 0 if matching, 1 if not
    
    #For all other characters:
    #Hundreds: 0 if matching, 1 if not
    #Unit: 0 if matching, 1 if not
    stringhashvalues = []
    searching = False
    searchindex = 0
    for k in range(0, len(string)):
#         print(stringhashvalues)
#         print('Score: ' + str(objectivescore) + ' Letter: ' + str(string[k]))
        
        #You first check where to start, which is done by finding a matching letter to the substring
        if string[k] in uniquelettervalues.keys() or searching is True:
            if k is 0 or searchindex is 0:
                #First character case
                
                #Calculate stringhashvalue based off current and following letter
                currentletterhashvalue = 10*getlettervalue(string[k+1]) + 100*getlettervalue(string[k])
                #Compare it to the substring hashvalue using searchindex than compute a difference value
                if (currentletterhashvalue%100)/10 > 0:
                #If the difference value is acceptable, than turn searching to true
                    searching = True
                    searchindex += 1
                    if (currentletterhashvalue%100)/10 - getlettervalue(string[k+1]):
                        objectivescore += 1
                        
                    stringhashvalues.append(1)
            elif searchindex is len(substring)-1:
                #end case, calculate stringhashvalue based off end condition, compare to last
                
                if stringhashvalues[searchindex-1] >= 10:
                    unitvalue = stringhashvalues[searchindex-1]%10
                else:
                    unitvalue = stringhashvalues[searchindex-1]
                    
                currentletterhashvalue = unitvalue + 100*getlettervalue(string[k])
                difference = abs(currentletterhashvalue - substringhashvalues[searchindex])
                if difference%100 > 0:
                    objectivescore += 1
                if difference > 99:
                    objectivescore += 1
                
                stringhashvalues.append(currentletterhashvalue)
                    
                return objectivescore    
            else:
                additionalscore = 0
                
                if stringhashvalues[searchindex-1] >= 10:
                    unitvalue = stringhashvalues[searchindex-1]%10
                else:
                    unitvalue = stringhashvalues[searchindex-1]
                
                #This is the case where the letter is neither first nor the last one
                #Calculate stringhashvalue based off current, previous, and following letter
                currentletterhashvalue = unitvalue + 10*getlettervalue(string[k+1]) + 100*getlettervalue(string[k])
                
                #Compare it to the substring hashvalue using searchindex, compute difference value
                difference = abs(currentletterhashvalue - substringhashvalues[searchindex])
                
                #Need to check whether current index characters could possibly be a false index (i.e. filler characters)
                if difference > 0.25*currentletterhashvalue:
                    #In this case, we assume that there is a mismatch, and proceed to check the next character against the same
                    #index.
                    additionalscore += 2
                else:
                    #In this case, we assume that the indexes are a match, and can be compared to check for string accuracy
                    if difference%100 > 0:
                        additionalscore += 1
                    if int(difference%10) > 0:
                        additionalscore += 1
                    if difference > 99:
                        additionalscore += 2
                
                #Case where objective score is too high, turn searching off, reset search index to 1, reset objectivescore
                if objectivescore > 0.5*len(substring):
                    searchindex = 1
                    objectivescore = 0
                else:
                #Case where additionalscore is acceptable, move index to the next one, add additionalscore to objectivescore
                    objectivescore += additionalscore
                    searchindex += 1
                    stringhashvalues.append(currentletterhashvalue)
                
                
        
    return 0
       
#This function filters out irrelevant characters from the string pattern
def filterstringpattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words
