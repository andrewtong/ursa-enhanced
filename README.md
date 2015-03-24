# ursa-enhanced
This is a preliminary concept that will expand the capabilities of the current existing repository URSA.  

The purpose of this is to take URSA into a new direction.  There are a number of difficulties associated with the 
scoring and partitioning methods used that prevent implementation of features that could possibly expedite runtime.  
That being said, it is highly suggested to first understand how URSA works before taking a look at this.  If this project
does happen to be a success, it will become the new URSA.  The reason this project has its own repository is because it 
plans to take a completely different direction and may prove to be more inefficient than URSA due to the complexity of 
the newly added algorithms.

Currently, goals for this project are the following

- Support already-searched word removal.

      Example: Given the substring 'word' and the string pattern 'We really like windy words.', I would want to remove
      'We re' and 'wind' because they are 4 letter word combinations that I know *do not* match the word 'word'.  The   
      difficulty behind this is that the scoring system needs to be more precise *and* you do not want to randomly remove 
      letters that may be part of the word, except in a different location.  Additionally, because the partitioning methods 
      creates paritions of minimum length 'j' where 'j' is the length of the substring, you do not want to accidently remove 
      too many letters!

- Scoring system needs to be slightly fixed to discern more accurately between 'wrong' and 'right' words.

      Explanation: Currently there are too many cases where a word comes out with a score of anywhere between 50-80.  This 
      is not good because it does not really give much information to the user whether the word is actually correct or 
      incorrect.  Instead, URSA just flags it as a potential match, which frankly does not mean much.  Ideally I want words
      to either be a definite 'yes or no' match with middle ground scores being used as less as possible.
      


