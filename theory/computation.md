v0.2

This file is dedicated towards more of the theoretical aspects of the project and the logic behind how the problem was 
solved. As explained in the readme, I attempt to solve fuzzy string matches similar to how an exponent is solved for in a 
exponential equation (as in, taking the logarithms of both sides).

For any substring, each letter is assigned an integer value associated with its position.  This serves as the fundamental 
scoring mechanism used for determing whether each letter is a fit.  For example, for the substring 'dog', I may choose to 
assign the letters with the followng integer values, while any other letters that are not 'd', 'o', or 'g' are scored as 0.

- 'd' : 1
- 'o' : 2
- 'g' : 3

This structure serves as the gist for determining string matches.  The assigning of the intergers utilizes a slightly more 
complex function to prevent dictionary key conflicts, but the basic idea still stands.  Using these numbers, each pair of 
letters will have two numbers associated with it.  For example, the letters 'do' are associated with the numbers 1 and 2.  
URSA-enhanced takes the sum and difference of the two numbers and places it in a tuple (3, -1).  The hashing function of 
URSA-enhanced ensures that the tuple (3, -1) will only correspond to the pair of letters 'do', and this respective key/value
pair is stored in a map.  So for each pair of letters in the substring, the corresponding index value is stored into a 
hashmap. Because hashmaps can perform lookups in constant time, this is consistently used to tell the algorithm whether the 
current tuple value is a correct match, partially correct match, or incorrect match depending on the values of the tuple 
itself.

* Case 1: Correct Match

  This is probably the easiest match, since if the current pair tuple value matches with an existing tuple value in the 
  dictionary, URSA-enhanced is immediately capable of knowing which index of the substring it is on.  However, its slightly 
  more complex.  The substring can be in numerous states, and by this I it can exist in a search/unsearched state, and
  IF it is in a searched state, then the index may be greater or less than the previous index that was found.

  So let's break this down into a few examples.  Let's say I have not started the search yet.  Assuming that the substring 
  is 'dog', if I see the tuple value (3, -1) associated with the letters 'do', this will be flagged as a match and the 
  algorithm will know to start searching for the word 'dog'.  However, let's say the I have a longer substring such as 
  'computer'.  If the algorithm reads the tuple value associated with 'te' of 'computer', then there are two results.
  IF the search has not started, then the algorithm would not start the search at the second to last index.  However, 
  if the search has been started, then it acknowledges the pair 'te' as a correct result.
  
  So let's assume that the search has started and the algorithm is currently on the index associated with the letter pair
  'te'.  The algorithm must now calculate how 'correct' this index is in terms of position.  Let's say the previous letter 
  pair was 'mt' (assuming that in the main string the word is incorrectly spelled as 'comter').  The letter pair 'te'    
  essentially jumps three indices, and receives a harsher score because rationally speaking if a word is missing 25% of 
  its letters, its likely a poor match.  On the contrary, if the previous letter pair was 'ut', then the algorithm would 
  detect that the current index is in the correct position.  
  
  This is a small breakdown behind the logic of URSA-enhanced for the correct case.  As demonstrated, because everything
  must be done 'lazily', it is critical that every case must be accounted for, and even the simpliest of cases has a 
  long thought process behind it.  Interestingly enough, the 'correct match' case is the foundation for the remainder of
  the cases, and a similar process is used once the algorithm determines a potential match exists.
  
* Case 2 : Partially Correct Match

  URSA-enhanced is also capable of analzying tuples for partially correct matches.  For example, lets assume that we are 
  given the word 'dog' along with the hashed values for each letter as shown above.  If the letters 'd' and 'o' were
  swapped, the resulting tuple would be (3, 1).  Notice how that the difference character only changes, but as expected
  the sum value remains the same.  This is by far the simplest case of the partially correct match category, and by 
  performing a very fast check it is possible to determine whether two characters that are correctly positioned are 
  swapped.

  However, there are a number of other cases which fall under the partially correct matched category but are more complex.
  Let's assume that the substring is 'dog', yet the word 'dog' is mispelled as 'doag' in the main string.  The algorithm
  will analyze tuple value expected the letter pair 'og', yet will find the letter pair 'oa'.  In this case, there are 
  a number of possible states that the substring may be in.  For this specific example, it will assume that either the 
  last letter 'g' will appear within the next few indexes, or the letter 'g' may not exist at all.  To compensate for this,
  URSA-enhanced attempts to guess how many indexes have been skipped.  The scoring is then reflected based off how many
  indexes are assumed to be skipped, with a greater number of skipped indexes corresponding to a higher incorrect score.  
  
  A key component of URSA-enhanced is that it stores the previous last correct letter.  Therefore, when it reaches the 
  letter pair 'ag', it will realize that the previous correct letter was 'o', and that in fact the letter pair 'og' does
  exist, except it is slightly mispositioned.  The algorithm will then access the hashmap to determine what index it is on,
  and continue on.
  
  However, what happens if the word 'dog' was simply mispelled as 'doa', and the 'g' is never seen in the following indexes.
  Recall that URSA-enhanced *assumes* how many indexes have been skipped.  Let's say that the letter pair following 'oa' was 
  'at'.  In this case, it will the skipped counter will be iterated by one, and the algorithm then assumes that two letters
  have been skipped.  However, recall that the last previous correct index was at the second index (or first, depending on
  how you look at it), which would be 'do'.  The algorithm recognizes that the word 'dog' has four letters, but it has 
  registered two correct letters.  Assuming that two letters have been skipped, it passes a threshold where it is pointless
  to search beyond the length of the substring.  This ensures that the matched words are scored correctly without the 
  algorithm searching for the last few letters.
  
  These two possibilities sum of the majority of the 'partially correct' match cases.  Similar to what is done in the   
  'correct match' case, the scoring is determined based off the distance between the previously computed and the current   
  computed index.
  
* Case 3 : Incorrect Match
  
  The 'incorrect' match case is a variant of the 'partially correct' match case whereas it utilizes the 'skipped' variable
  as previously mentioned.  As discussed in the 'partially matched' case, when the algorithm recognizes a letter that 
  is incorrect in terms of position, it aggregates the skipped variable by 1 to acknowledge the possibility of said variable
  not existing within the main string.  As a result, two cases may be derived from this scenario.

  The first possibility includes finding the correct letter, but incorrectly positioned at a future index.  This overlaps
  with the computations done in the 'partially correct' case, where the resulting score is an aggregate of the number of
  letters that had to be skipped times a variable multiplier and a measure of how many indexes, if any, were skipped.  
  
  The second possibility is when the desired letter is never found on a future index, and a subsequent upcoming future pair
  of letters is encountered as the algorithm iterates through the main string (consider 'compaaater' as an example for the 
  substring 'computer').  The letter pairs 'pu' / 'ut' is never found, while the next correct letter pair 'te' is the next to
  appear.  Similar to how the skipped variable was used in the other cases, a score based off the number of letters skipped 
  times a given multiplier will be added to the string's score.  However, in this case, it is important to recognize that the
  letter pair 'ut' never existed within the string.  Therefore, the algorithm recognizes (via the hashmap) that the letter 
  pair 'te' is two indexes ahead of the previous correct letter pair 'mp' and will add a second score, similar to the method
  used in the 'correct match' case to account for the missing index.
