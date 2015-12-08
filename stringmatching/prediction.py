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
        self.letter_value_map = CharacterInfo.score_letters(self)
        self.substring_map = CharacterInfo.map_substring(self)
        
    def score_letters(self):
        i = 1
        self.letter_value_map = {}
        for char in self.substring:
            if char not in self.letter_value_map:
                #The values associated with the letters must be unique to prevent dictionary key conflicts.
                self.letter_value_map[char] = (i + len(self.substring))*(i + len(self.substring)) - i
                i += 1
        
        return self.letter_value_map
                
    def get_letter_score(self, letter):
        if letter not in self.letter_value_map:
            return 0
        else:
            return self.letter_value_map[letter]
                
    def map_substring(self):
        self.substring_map = {}        
        for j in range(0, len(self.substring)):
            try:
                sum_value = CharacterInfo.get_letter_score(self, self.substring[j]) + CharacterInfo.get_letter_score(self, self.substring[j+1])
                diff_value = CharacterInfo.get_letter_score(self, self.substring[j]) - CharacterInfo.get_letter_score(self, self.substring[j+1])
            except IndexError:
                return self.substring_map
            if (sum_value, diff_value) in self.substring_map:
                self.substring_map[(sum_value, diff_value)].append(j + 1)
            else:
                self.substring_map[(sum_value, diff_value)] = [j + 1]            
                
def score(main, substring):
    result = compare(main, substring)
    
    if result < 0 or result > 2*len(substring):
        return 0
    else:
        percent_correct = max(5.0, 100*(1 - result/(1.5*len(substring))))
        return int(100 - 76.87 * log10(100/percent_correct))

def map_substring(substring):
    #Now the substring needs to be interpreted as a score, using the above scoring convention in uniquelettervalues.
    substring_map = {}
    for j in range(0,len(substring)):
        try:
            sum_value = substring[j] + substring[j + 1]
            diff_value = abs(substring[j] - substring[j + 1])
            substring_value = (sum_value, diff_value)
            substring_map[j] = substring_value
        except IndexError:
            substring_value = (substring[j], substring[j])
            substring_map[j] = substring_value
    return substring_map

def compare(string,substring):
    string = filter_string_pattern(string)
    
    ci = CharacterInfo(substring)
    base_copy = ci.substring_map
    current_index = 1
    objective_score = 0
    skipped = 0
    
    #prevcharinfo (previous character letter score, second previous character letter score, previous index)
    #at the new index, it calculates the new sum and difference
    #previous index is used to compare against current index, which subsequently produces a score
    prev_char_info = (-1, -1, 0)

    for char in string:
        
        #so if we are scanning the first letter in the main string, only the previous letterscore is found, and the 
        #algorithm moves to the next character
        if prev_char_info[0] is -1:
            current_char_value = ci.get_letter_score(char)
            prev_char_info = (current_char_value, -1, 0)
            continue
        
        #if the current character is not the first letter, than a sum and diff value are calculated to check for accuracy
        #prev char info is updated depending on whether there is a match
        else:
            current_char_value = ci.get_letter_score(char)
            sum_value = prev_char_info[0] + current_char_value
            diff_value = prev_char_info[0] - current_char_value
        
        if (prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value) in ci.substring_map: 
            if ci.substring_map[(prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value)][0]*prev_char_info[2] is 1:
                objective_score = 0 #temp fix until i figure out this swap issue
                sum_value = prev_char_info[1] + current_char_value
                diff_value = prev_char_info[1] - current_char_value                
                prev_char_info = (prev_char_info[1], 0, 0)
                ci.substring_map = base_copy
                
        #check for correct position or if the position of within the substring        
        if (sum_value, diff_value) in ci.substring_map:
            result = check_valid_pattern_position(ci, char, sum_value, diff_value, prev_char_info, objective_score, substring, current_char_value, skipped)
            current_index = result[0]
            ci = result[1]
            objective_score = result[2]
            prev_char_info = result[3]
            
        #check for swapped position
        elif (sum_value, -diff_value) in ci.substring_map: # and char is substring[currentindex] and prevcharinfo[0] is not -1:
            result = check_swapped_position_pattern(ci, sum_value, diff_value, prev_char_info, objective_score, substring, current_char_value)
            current_index = result[0]
            ci = result[1]
            objective_score = result[2]
            prev_char_info = result[3] 
             
        #performs a one off check (typically where there is a misc. letter in between two correctly positioned letters)
        elif (prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value) in ci.substring_map:
            result = check_one_off_pattern(ci, prev_char_info, objective_score, current_char_value)
            current_index = result[0]
            ci = result[1]
            objective_score = result[2]
            prev_char_info = result[3] 
        
        #case where current character is incorrect, but search has began
        elif char is not substring[current_index + 1] and prev_char_info[0] > 0:
            objective_score, prev_char_info = check_invalid_char_pattern(current_char_value, objective_score, skipped, prev_char_info)
            skipped += 2

            if skipped + current_index + 1 >= len(substring) and current_index >= 0.5*len(substring):
                return objective_score    
        else: 
            current_index = 0
            objective_score = 0
            prev_char_info = (current_char_value, 0, current_index)
            ci.substring_map = base_copy

    
        if current_index is len(substring) - 1:
            #the check for the last two letters is performed, if the last letter doesn't exist, it would count as a one off anyways
            return objective_score
        
        if objective_score >= 1.5*len(substring):  
            prev_char_info = (current_char_value, 0, 0)
            objective_score = 0
            ci.substring_map = base_copy
            skipped = 0
        
    #if no match is found
    return -1

def check_valid_pattern_position(ci, char, sum_value, diff_value, prev_char_info, objective_score, substring, current_char_value, skipped):
    if len(ci.substring_map[(sum_value, diff_value)]) > 1:
        current_index = ci.substring_map[(sum_value, diff_value)][0][0]
        ci.substring_map[(sum_value, diff_value)].pop(0)
    else:   
        current_index = ci.substring_map[(sum_value, diff_value)][0]

    #index jump   
    if current_index - prev_char_info[2] > 1 and current_index - prev_char_info[2] <= int(len(substring)/2):
        objective_score += (current_index - prev_char_info[2] - skipped/2)*1.2
        prev_char_info = (current_char_value, prev_char_info[0], current_index)    
    #correct match exists, proceed to next index  
    elif char is substring[current_index]:
        if current_index is prev_char_info[2]:
            objective_score += 1.1
        else:
            objective_score += 0
        prev_char_info = (current_char_value, prev_char_info[0], current_index)
    #search has not started, this index will be deemed as the first index, iff current index is less than 1/2 of the
    #length of the substring
    elif prev_char_info[2] is 0 and current_index <= 0.5*len(substring):

        objective_score += 1.5*(current_index)
        prev_char_info = (current_char_value, 0, current_index)
    #substring search has started, but the index is out of place
    else:
        objective_score += 2
        prev_char_info = (prev_char_info[0], prev_char_info[1], prev_char_info[2])
        
    return (current_index, ci, objective_score, prev_char_info)

def check_swapped_position_pattern(ci, sum_value, diff_value, prev_char_info, objective_score, substring, current_char_value):
    if len(ci.substring_map[(sum_value, -diff_value)]) > 1:
        current_index = ci.substring_map[(sum_value, -diff_value)][0][0]
        ci.substring_map[(sum_value, -diff_value)].pop(0)
    else:
        current_index = ci.substring_map[(sum_value, -diff_value)][0]

    sv = prev_char_info[1] + current_char_value
    dv = prev_char_info[1] - current_char_value

    if (sv, dv) in ci.substring_map:
        objective_score += 0.5*(current_index - ci.substring_map[(sv, dv)][0])
    else:
        objective_score += 1.5*(current_index - prev_char_info[2])
        
    #check if current index is 1 greater than previous index
    prev_char_info = (ci.get_letter_score(substring[current_index]), ci.get_letter_score(substring[current_index - 1]), current_index)
    return (current_index, ci, objective_score, prev_char_info)

def check_one_off_pattern(ci, prev_char_info, objective_score, current_char_value):
    if len(ci.substring_map[(prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value)]) > 1:
        current_index = ci.substring_map[(prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value)][0][0]
        ci.substring_map[(prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value)].pop(0)
    else:
        current_index = ci.substring_map[(prev_char_info[1] + current_char_value, prev_char_info[1] - current_char_value)][0]
    objective_score += 1
    prev_char_info = (current_char_value, prev_char_info[1], current_index)
    
    return (current_index, ci, objective_score, prev_char_info)

def check_invalid_char_pattern(current_char_value, objective_score, skipped, prev_char_info):
    if current_char_value > 0:
        objective_score += 0.8 + skipped*0.5
        prev_char_info = (current_char_value, prev_char_info[0], prev_char_info[2] + 1)
    else:
        objective_score += 1.8 + skipped*0.3
        
    return (objective_score, prev_char_info)

#This function filters out irrelevant characters from the string pattern
def filter_string_pattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words

#print(score('URSA-enhanced is capable of performing fuzzy string matches at remarkable speeds.', 'fuzzy'))
#print(score('Similar to URSA, basic errors can easily be recgnized.', 'recognized'))
#print(score('Errors of higher comlpexty are now solved faster with the same precise accuracy.', 'complexity'))
#print(score('URSA-enhanced can also accurately determine whether a word is not present.', 'python'))
#print(score('Sesahells are slod down by the seacshore by Slally.','seashore'))
