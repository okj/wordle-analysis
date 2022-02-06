# Finding the best first guess for Wordle

I've been playing [Wordle](https://www.powerlanguage.co.uk/wordle/) for about a week now, and I can definitely see what all the hype is about. It's a really fun puzzle game which you can play alone or with your friends, where the goal is to guess a 5 letter word in as few guesses as possible. Something that also piqued my interest was that the code behind this game was notoriously uncomplicated ([which didn't stop New York Times from aquiring it](https://www.cnn.com/2022/01/31/media/wordle-new-york-times-free/index.html)). 

The entire game is made up of a single minified javascript file [main.js](https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js) and the answer to the daily puzzle is stored in localstorage. This can easily be revealed using:
> javascript:alert(JSON.parse(localStorage.gameState).solution)

Contained in the main js file is a giant array containing all the possible solutions. This lead to the creation of sites like [WordleSolver.com](https://www.wordlesolver.com/) by [@cgenco](https://github.com/christiangenco) which narrows down solutions based on previous guesses until you are eventually given the answer.

Both of these techniques can be used to beat Wordle, but that ruins the fun. What I am more interested in, is answering **"What is the best first guess?"**

---

The first step was grabbing that giant array. I downloaded the main.js file, ran it through [a javascript deobfuscator](https://deobfuscate.io/) for better viewing, and opened it in VS Code.

```
// Here's our  big array
var La = ["cigar", "rebut", "sissy", "humph", "awake", "blush", "focal", "evade", "naval", "serve"...
```
I had to increase my `maxTokenizationLineLength` in VS Code just to see the end of this array!

I copied the line, ran some Regex, created `words.csv` and started running some code.

### The Plan

The plan was simple. I wanted to run a simple O(n^2) algorithm that compared the placement of each letter for each word, to that same index of every word. For example, if my word is "cigar" my code should loop 5 times (c, i, g, a, r) and look for words with letters in the same place. If the letters are the same, add +1 to `score`

So "**c**iga**r**" would earn +2 from a word like "**c**ove**r**". This should result in the best word to guess for the highest chance of a green tile.

### A Discovery

...and then my code broke. I quickly realized this wasn't a *single* big array, it was actually two. 

```
"rower", "artsy", "rural", "shave"], Ta = ["aahed", "aalii", "aargh", "aarti", "abaca", "abaci"
```

The 2nd array also contained 5 letter words, but there was a very distinct difference between the two... I don't think many people would be guessing "[aahed](https://www.merriam-webster.com/thesaurus/aahed)" (*verb: Simple past tense and past participle of aah*)

I figured that this must be an array of *acceptable* words contained in a 2nd array to prevent them from being one of the daily solutions. A quick test confirmed my suspicions.

![](https://i.imgur.com/OUPsyzB.png)

This meant I would want to compare all acceptable words + solutions, against all solutions. I split the word lists, finished the code, and got my results.

### The Results

The algorithm took about 20 seconds to complete which I figured was acceptable given it would only need to be ran once.

## Top 10
||Word|Score|
|-|----|-----|
|1|saree|1575|
|2|sooey|1571|
|3|soree|1550|
|4|saine|1542|
|5|soare|1528|
|6|saice|1512|
|7|sease|1510|
|8|seare|1491|
|9|seine|1480|
|10|slane|1480|

The suprising amount of words starting with "s" indicates that this must be the most common first character. The issue with this table is that in Worlde, there is no reason to guess words with repeated characters. These would be wasted guesses, and adjusting for this should increase our odds of getting Yellow tiles.

## Top 10 (Adjusted)
|Word|Score|
|----|-----|
|saine|1542|
|soare|1528|
|saice|1512|
|slane|1480|
|slate|1437|
|soily|1437|
|soave|1422|
|samey|1413|
|sauce|1411|
|slice|1409|

And there you go. The best first guesses for Wordle prioritizing Green > Yellow tiles.