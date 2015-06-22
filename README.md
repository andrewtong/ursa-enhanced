# ursa-enhanced

**It is highly recommend to understand how URSA works before looking at this!**

The code and theory behind URSA can be found at : https://github.com/andrewtong/ursa

The theory behind URSA-enhanced is detailed in the theory file..

#Introduction#

URSA-enhanced is a fuzzy string matching algorithms that operates in **linear time-complexity** created using the
fundamentals of what I've learned while designing URSA.  Based off my understanding of how string matching operates,
there is an inherent tradeoff between knowing the location of the to-be matched substring, and the time complexity associated
with the algorithm.  In short, it is very costly in terms of time to determine the precise location of the substring.

Fuzzy string matches can be perceived as a two step process.  The first is determining the location of the substring within the main string.  Afterwards, it is then possible to compare the substring to the desired string to compute accuracy.  
URSA-enhanced takes a unique approach to this by performing both processes at once.  The concept behind this is that the
algorithm consistently attempts to estimate what the current index is, and calculates an aggregate score based off the
difference between the previous and current index.

#How does the algorithm of URSA-enhanced work?#

The theory behind the algorithm is still very tentative, but can be explained in a simple way.  There are two main issues
that need to be solved.  First off, the algorithm seeks where the substring may possibly exist in the main string.  Because
the algorithm will only scan the main string once, it is imperative to locate the substring as precisely as possible, and
additionally account for errors that may possibly exist within the main string.  Secondly, the algorithm must check how 
close of a match, if any, exists between the two strings.

The solution to performing this is to 'solve' the main string in terms of the substring.  Similar to how logarithms are 
applied to exponential equations in order to solve for the exponential value, if a value can be attributed to substring,
the algorithm can search for this particular value **if** the value can also trigger a response to the algorithm to indicate
the starting location of the word.  With the right hashing equation though, if the algorithm is capable of creating a unique 
code for the substring as well as performing accurately indicating where it believes the substring starts within the main
string, then it resolves both of the critical problems allowing the fuzzy string problem to be quickly solved.

This is done by analyzing similarities between pairs of letters between the substring and the main string.  A hashing 
equation unique to the letters of the substring allows for any pairs of letters to be hashed into a pair of numbers.  As the
algorithm consistently scans through each pair of numbers, it attempts to guess whether or not the current pair of letters
exists within the substring.  Using a combination of hashmaps and lazy evaluations, the algorithm attempts to categorize 
pairs of letters by the type of error, if any.  

#Performance#

Performance comparisons on URSA-enhanced done on the same computer as URSA show remarkable results in terms of accuracy
and speed.  On a per average basis, URSA-enhanced performs significantly faster while maintaining high accuracy rates.

```
print(score('URSA-enhanced is capable of performing fuzzy string matches at remarkable speeds.', 'fuzzy'))
100
```

```
print(score('Similar to URSA, basic errors can easily be recgnized.', 'recognized'))
95
```

```
print(score('Errors of higher comlpexty are now solved faster with the same precise accuracy.', 'complexity'))
48
```

```
print(score('URSA-enhanced can also accurately determine whether a word is not present.', 'python'))
0
```

Using IPython, I took two queries from the examples within the readme in URSA and recorded their respective runtimes.  Based
off a series of comparisons between URSA and URSA-enhanced, on average URSA-enhanced will outperform URSA in terms of 
runtime by apporximately 200% (i.e. operates twice as fast).

```
%timeit score('The quick brown fox jmuped over the lazy dog.','jumped')
10000 loops, best of 3: 193 μs per loop
```

```
%timeit score('Sally sells seashells down by the seaschore.','seashore')
1000 loops, best of 3: 339 μs per loop
```

The first example demonstrated an approximate 30% decrease in runtime (193 μs compared to 307 μs), while the second example
had an approximate 50% decrease in runtime (339 μs compared to 758 μs).  On a per average basis, there is a 
substantial decrease in runtime due to the elimination of many redundant processes involved in URSA and the efficiency 
associated with the algorithm of URSA-enhanced.  A special case worth mentioning is that significant (on the scale of >80%) 
decreases in runtime can be achieved when the substring is located within the first few indexes of the main string as 
demonstrated in the following example.

```
%timeit score('Sally sells seashells down by the seashore.','Sally')
10000 loops, best of 3: 90.1 μs per loop
```

Because the algorithm operates in linear-time complexity, runtime is expected to be primarily determined by where the 
substring is located (if it is at all) within the main string. 

#Why is this not a continuation of URSA?#

The reason this project has its own repository is because it plans to take a completely different direction, primarily 
focusing on how to optimize the runtime of the algorithm, as opposed to optimizing the accuracy of the result.  As explained 
above, the two factors inherently conflict with each other, so there is no real means to optimizing both.  That being said,
URSA-enhanced has significantly more potential due to how the uncertainty associated with the scoring can be exploited
in favor of using more estimation techniques.
      


