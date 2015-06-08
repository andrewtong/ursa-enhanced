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


class CharacterInfo:
    def __init__(self,substring):
        self.substring = substring
        self.lettervaluemap = CharacterInfo.scoreletters(self)
        self.substringmap = CharacterInfo.mapsubstring(self)
        
    def scoreletters(self):
        i = 1
        self.lettervaluemap = {}
        for char in self.substring:
            if char not in self.lettervaluemap:
                #The values associated with the letters must be unique to prevent dictionary key conflicts.
                self.lettervaluemap[char] = (i + len(self.substring))*(i + len(self.substring)) - i
                i += 1
        
        return self.lettervaluemap
                
    def getletterscore(self, letter):
        if letter not in self.lettervaluemap:
            return 0
        else:
            return self.lettervaluemap[letter]
                
    def mapsubstring(self):
        self.substringmap = {}        
        for j in range(0, len(self.substring)):
            try:
                sumvalue = CharacterInfo.getletterscore(self, self.substring[j]) + CharacterInfo.getletterscore(self, self.substring[j+1])
                diffvalue = CharacterInfo.getletterscore(self, self.substring[j]) - CharacterInfo.getletterscore(self, self.substring[j+1])
#                 if self.substringmap[(sumvalue, diffvalue)] in substringmap:
#                     self.substringmap[(sumvalue, diffvalue)].append(j)
#                 else:
#                     self.substringmap[(sumvalue, diffvalue)] = j
            except IndexError:
                return self.substringmap
#                 sumvalue = CharacterInfo.getletterscore(self, self.substring[j])
#                 diffvalue = CharacterInfo.getletterscore(self, self.substring[j])
            if (sumvalue, diffvalue) in self.substringmap:
                self.substringmap[(sumvalue, diffvalue)].append(j + 1)
            else:
                self.substringmap[(sumvalue, diffvalue)] = [j + 1]            
                
def score(main, substring):
    result = compare(main, substring)
    
    if result < 0 or result > 2*len(substring):
        return 0
    else:
        #return (1 - (result/(2*len(substring)))**2)/100
        percentcorrect = max(5.0, 100*(1 -result/(1.5*len(substring))))
        return int(100 - 76.87 * log10(100/percentcorrect))

def mapsubstring(substring):
    #Now the substring needs to be interpreted as a score, using the above scoring convention in uniquelettervalues.
    substringmap = {}
    for j in range(0,len(substring)):
        try:
            sumvalue = substring[j] + substring[j + 1]
            diffvalue = abs(substring[j] - substring[j + 1])
            substringvalue = (sumvalue, diffvalue)
            substringmap[j] = substringvalue
        except IndexError:
            substringvalue = (substring[j], substring[j])
            substringmap[j] = substringvalue
    return substringmap

def compare(string,substring):
    string = filterstringpattern(string)
    
    ci = CharacterInfo(substring)
    currentindex = 1
    objectivescore = 0
    skipped = 0
    
    #prevcharinfo (previous character letterscore, second previous character letterscore, previous index)
    #at the new index, it calculates the new sum and difference
    #previous index is used to compare against current index, which subsequently produces a score
    prevcharinfo = (-1, -1, 0)

    for char in string:

        
        #so if we are scanning the first letter in the main string, only the previous letterscore is found, and the 
        #algorithm moves to the next character
        if prevcharinfo[0] is -1:
            currentcharvalue = ci.getletterscore(char)
            prevcharinfo = (currentcharvalue, -1, 0)
            continue
        
        #if the current character is not the first letter, than a sum and diff value are calculated to check for accuracy
        #prev char info is updated depending on whether there is a match
        else:
            currentcharvalue = ci.getletterscore(char)
            sumvalue = prevcharinfo[0] + currentcharvalue
            diffvalue = prevcharinfo[0] - currentcharvalue
           
        #check for correct position or if the position of within the substring        
        if (sumvalue, diffvalue) in ci.substringmap:
            
            if len(ci.substringmap[(sumvalue, diffvalue)]) > 1:
                currentindex = ci.substringmap[(sumvalue, diffvalue)][0][0]
                ci.substringmap[(sumvalue, diffvalue)].pop(0)
            else:   
                currentindex = ci.substringmap[(sumvalue, diffvalue)][0]   
            
            #correct match exists, proceed to next index              
            if char is substring[currentindex]:

                objectivescore += 0
                prevcharinfo = (currentcharvalue, prevcharinfo[0], currentindex)
            #search has not started, this index will be deemed as the first index, iff current index is less than 1/2 of the
            #length of the substring
            elif prevcharinfo[2] is 0 and currentindex <= 0.5*len(substring):

                objectivescore += 1.5*(currentindex)
                prevcharinfo = (currentcharvalue, 0, currentindex)
            #substring search has started, but the index is out of place
            #if calculated index is less than current index, then...
            #if calculated index is greater than current index, then...
            else:
                if currentindex > prevcharinfo[2]:
                    objectivescore += (currentindex - prevcharinfo[2] - 1)*1
                    prevcharinfo = (currentcharvalue, prevcharinfo[0], currentindex)
                else:
                    objectivescore += 2
                    prevcharinfo = (prevcharinfo[0], prevcharinfo[1], prevcharinfo[2])
            
        #check for swapped position
        elif (sumvalue, -diffvalue) in ci.substringmap: # and char is substring[currentindex] and prevcharinfo[0] is not -1:

            if len(ci.substringmap[(sumvalue, -diffvalue)]) > 1:
                currentindex = ci.substringmap[(sumvalue, -diffvalue)][0][0]
                ci.substringmap[(sumvalue, -diffvalue)].pop(0)
            else:
                currentindex = ci.substringmap[(sumvalue, -diffvalue)][0]

            sv = prevcharinfo[1] + currentcharvalue
            dv = prevcharinfo[1] - currentcharvalue

            if (sv, dv) in ci.substringmap:
                objectivescore += 0.5*(currentindex - ci.substringmap[(sv, dv)][0])
            else:
                objectivescore += 1.5*(currentindex - prevcharinfo[2])
                
            #check if current index is 1 greater than previous index
            prevcharinfo = (ci.getletterscore(substring[currentindex]), ci.getletterscore(substring[currentindex - 1]), currentindex)
            
        #performs a one off check (typically where there is a misc. letter in between two correctly positioned letters)
        elif (prevcharinfo[1] + currentcharvalue, prevcharinfo[1] - currentcharvalue) in ci.substringmap:
            if len(ci.substringmap[(prevcharinfo[1] + currentcharvalue, prevcharinfo[1] - currentcharvalue)]) > 1:
                currentindex = ci.substringmap[(prevcharinfo[1] + currentcharvalue, prevcharinfo[1] - currentcharvalue)][0][0]
                ci.substringmap[(prevcharinfo[1] + currentcharvalue, prevcharinfo[1] - currentcharvalue)].pop(0)
            else:
                currentindex = ci.substringmap[(prevcharinfo[1] + currentcharvalue, prevcharinfo[1] - currentcharvalue)][0]
            objectivescore += 1
            prevcharinfo = (currentcharvalue, prevcharinfo[1], currentindex)
                  
        #case where current character is correct, but previous character is incorrect
        elif char is substring[currentindex + 1]:
            #first check if in combination with prev char creates a actual fit
                #this is checked by the first check, since it calculates current character and the one from prevchar value
            #if not, then there could be a missing letter in between, in which you assume to be true
            
            if prevcharinfo[0] > 0 and currentcharvalue > prevcharinfo[0]:
                #valid character in word but is incorrect (e.x. a letter skip)
                objectivescore += 0.5
            
            else: 
                #random character
                objectivescore += 1.5
            prevcharinfo = (currentcharvalue, prevcharinfo[0], prevcharinfo[2] + 1)
        
        #case where current character is incorrect, but search has began
        elif char is not substring[currentindex + 1] and prevcharinfo[0] > 0:
            #prevcharinfo should not change, since this is essentially a blank filler character
            #prevcharinfo = (currentcharvalue) 
            if currentcharvalue > 0:
                objectivescore += 0.8 + skipped*0.5
                #prevcharinfo = (currentcharvalue, prevcharinfo[0], prevcharinfo[2])
            else:
                objectivescore += 1.8 + skipped*0.3
            
            skipped += 2

            if skipped + currentindex + 1 >= len(substring):
                return objectivescore    
        else: 
            currentindex = 0
            prevcharinfo = (currentcharvalue, prevcharinfo[0], currentindex)

    
        if currentindex is len(substring) - 1:
            #the check for the last two lettersis performed, if the last letter doesn't exist, it would count as a one off anyways
            return objectivescore
        
        if objectivescore >= 1.5*len(substring):
            
            prevcharinfo = (currentcharvalue, 0, 0)
            objectivescore = 0
        
    #if no match is found
    return -1

       
#This function filters out irrelevant characters from the string pattern
def filterstringpattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words
