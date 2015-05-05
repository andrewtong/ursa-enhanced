# ursa-enhanced
#Currently a work in progress#
This is a preliminary concept that will expand the capabilities of the current existing repository URSA. 

**It is highly recommend to understand how URSA works before looking at this!**

The code and theory behind URSA can be found at : https://github.com/andrewtong/ursa

#Introduction#

URSA-enhanced is a fuzzy string matching algorithms that operates in **linear time-complexity** created using the
fundamentals of what I've learned while designing URSA.  Based off my understanding of how string matching operates,
there is an inherent tradeoff between knowing the location of the to-be matched substring, and the time complexity associated
with the algorithm.  In short, it is very costly in terms of time to determine the precise location of the substring.

An example of my point is explained below; consider the following string and substring:
String: 'The quick brown fox jumped over the lazy dog.'
Substring: 'jumped'

The most obvious way to solve this is to recognize that the word 'jumped' exists between the indexes 20 and 25 inclusive.
I can then compare the word 'jumped' in the string, to the substring 'jumped'.  However, this is incredibly inefficient
because the time required to find the exact location of the substring within the string is incredibly costly in terms of 
performance, since there is no efficient means to pinpoint the location of the substring.  Many existing fuzzy string 
algorithms circumvent this issue by attempting to partition the string in an attempt to guess the location of the substring.
An example of this would be assuming that words are split by a whitespace.  However, the fallacy behind this is that 
searching for words that are clustered between letters (for example, 'foxjumpedover') would not be possible.

I may take this a step further and attempt to find the location of the start of the substring.  This is exactly how URSA
operates.  Instead of partitioning by whitespaces, I attempt to find where the substring may possibly start, and partition
by letters given in the substring.  This is substantially more effective since the partitioning can be optimally performed
in linear time.   The biggest advantage of URSA is that it could perform fuzzy string matching on an per average basis 
significantly faster than existing algorithms without achieving very precise results.  Further detail regarding URSA can be 
found at https://github.com/andrewtong/ursa

However, in the worst case scenarios, URSA can still be pretty inefficient, since it may have to partition the main string
several times, and may even find no result at all.  To remedy this, URSA-enhanced is designed to only parse the main string
once, and then proceed to determine whether the substring exists either as a fuzzy string match within the main string.  The
difficulty behind this is that in the only way for this algorithm to operate in linear time is to never precisedly know
where the substring starts or ends.  Because of this, the quality of the result is not as 'accurate' but the algorithm
operates significantly more quickly.

#How does the algorithm of URSA-enhanced work?#

The theory behind the algorithm is still very tentative, but can be explained in a broad fashion.  There are two main issues
that need to be solved.  First off, the algorithm seeks where the substring may possibly exist in the main string.  Because
the algorithm will only scan the main string once, it is imperative to locate the substring as precisely as possible, and
additionally account for errors that may possibly exist within the main string.  Secondly, the algorithm must check how 
close of a match, if any, exists between the two strings.  Taking these two factors into consideration, it is completely
possible to perform fuzzy string matches in linear time.

The sollution to performing this is to 'solve' the main string in terms of the substring.  Similar to how logarithms are 
applied to exponential equations in order to solve for the exponential value, if a value can be attributed to substring,
the algorithm can search for this particular value **if** the value can also trigger a response to the algorithm to indicate
the starting location of the word.  With the right hashing equation though, if the algorithm is capable of creating a unique 
code for the substring as well as performing accurately indicating where it believes the substring starts within the main
string, then it resolves both of the critical problems allowing the fuzzy string problem to be quickly solved.

#Why is this not a continuation of URSA?#

The reason this project has its own repository is because it plans to take a completely different direction, primarily 
focusing on how to optimize the runtime of the algorithm, as opposed to optimizing the accuracy of the result.  As explained 
above, the two factors inherently conflict with each other, so there is no real means to optimizing both.  That being said,
URSA-enhanced has significantly more potential due to how the uncertainty associated with the scoring can be exploited
in favor of using more estimation techniques.
      


