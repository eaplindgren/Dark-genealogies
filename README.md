# Dark Genealogies
Project inspired by [this reddit post](https://www.reddit.com/r/DarK/comments/1jwgu3b/spoilers_s3_elisabeth_charlotte_and_hanno/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button), which noted that Charlotte is 2/3 Noah 1/3 Peter, and Elizabeth is 2/3 Peter 1/3 Noah. I thought this was interesting and surprising and realized that there was a more elegant way to do math on this using linear algebra/Markov chains rather than calculus.

This program calculates the ancestry of each person in the Dark family tree in terms of the percentage of their DNA they get from
each of the following people: Egon, Doris, Katharina, Jana, Alexander, Katharina, Hannah, Peter. Every other character in the tree is descended from them. Results are in the file ``genealogy.txt``.



I left out some of the ancestors of the aforementioned people because they have "conventional" ancestries (e.g., Peter's ancestry, his parents and grandparents didn't bear any children elsewhere in the tree) and also left out some characters whose ancestry is identical to others' (Magnus has the same ancestry as Martha and Mikkel, Mads has the same ancestry as Ulrich, Franziska has the same ancestry as Elizabeth.)

As an example, here's Jonas's ancestry.
```
Hannah: 53.45%
Katharina: 27.59%
Jana: 13.79%
Egon: 2.16%
Alexander: 1.72%
Bernd: 0.86%
Doris: 0.43%
```
In general, the results are more complex than you might imagine! For example, Jonas gets 50% Hannah DNA because she's his mom, but an extra 1.56% because she's also his great-great-great-great-grandmother: (Hannah->Silja->Agnes->Tronte->Ulrich->Mikkel->Jonas), and another 1.8% because Jonas is his own great-great-great-grandfather (Jonas->Unknown->Tronte->Ulrich->Mikkel->Jonas), recursively introducing more Hannah DNA into his ancestry.




## Variant Genealogies
I created some other genealogies as well, contained in the other text files. Here's a description of each of them. There's also a description at the top of each file.
#### ``tronte.txt``
If Tronte had been Regina's biological father. The result is that Regina, Bartosz, Agnes, and Noah are now also bootstrapped, and there's even more incest.
#### ``bernd.txt``
If Bernd had been Helge's biological father. This just introduces a touch of incest as Peter (now Bernd's grandson) and Charlotte (Bernd's great-great-granddaughter via Bernd->Regina->Bartosz->Noah->Charlotte) marry. For this tree I added Peter's ancestors, not present in the original.

#### ``full.txt``
This is where it gets interesting! I wanted to create a version of the genealogy that shows how much of everyone's DNA they get from _every_ one of their ancestors, not just the origin world folks at the "leaves" of the family tree. To give a simple example, here's Bartosz's ancestry from the original version:
```
Alexander: 50.0%
Bernd: 25.0%
Egon: 12.5%
Doris: 12.5%
```
and in the "full" version:
```
Regina: 50.0%
Alexander: 50.0%
Claudia: 25.0%
Bernd: 25.0%
Egon: 12.5%
Doris: 12.5%
```
which also shows his "intermediate" ancestors, Regina and Claudia. Note that the percentages no longer add up to 100%. When you get to the bootstrapped Nielsens, there are like 16 different ancestors listed.

Creating the "full" genealogy required a fairly different mathematical method from creating the original genealogy, as I describe below.

#### ``alt.txt``
This is where it gets even more interesting! Since Unknown is really the child of Jonas and _alt_-Martha, not regular Martha, I decided to modify the family tree to include the alt-universe as well. This means that all of the Nielsens have ancestors in both universes (the Dopplers, while bootstrapped, only have ancestry from one universe.) To my surprise, they all had _asymmetric_ ancestry from both universes, but this made sense after thinking about it a little. For example, here's Unknown's ancestry:
```
Hannah: 28.45%
alt-Katharina: 27.59%
Katharina: 13.79%
alt-Jana: 13.79%
Jana: 6.9%
alt-Egon: 2.16%
alt-Alexander: 1.72%
alt-Hannah: 1.72%
Egon: 1.08%
Alexander: 0.86%
alt-Bernd: 0.86%
Bernd: 0.43%
alt-Doris: 0.43%
Doris: 0.22%
```
Hannah is Unknown's grandmother through Jonas, but alt-Hannah is _much_ more distantly related to him (Hannah->Silja->Agnes->Tronte->Ulrich->Martha->Unknown), so he has way more Hannah than alt-Hannah DNA. There are a number of things like this and they're further amplified by bootstrapping. You'll notice that actually there isn't anyone at all whose regular and alt- versions are equally represented in Unknown's ancestry.

#### ``alt_full.txt``
I took the above alt-universe-included genealogy and applied the "full" genealogy method described above. This led to a pretty enormous amount of detail. For example, here's Unknown again, but now with his "full" alt-inclusive genealogy:
```
Jonas: 55.17%
alt-Martha: 55.17%
Hannah: 28.45%
Mikkel: 27.59%
alt-Ulrich: 27.59%
alt-Katharina: 27.59%
Ulrich: 13.79%
Katharina: 13.79%
alt-Tronte: 13.79%
alt-Jana: 13.79%
Unknown: 10.34%
Tronte: 6.9%
Jana: 6.9%
alt-Agnes: 6.9%
Agnes: 3.45%
alt-Bartosz: 3.45%
alt-Silja: 3.45%
alt-Egon: 2.16%
Bartosz: 1.72%
Silja: 1.72%
alt-Regina: 1.72%
alt-Alexander: 1.72%
alt-Hannah: 1.72%
Egon: 1.08%
Regina: 0.86%
Alexander: 0.86%
alt-Claudia: 0.86%
alt-Bernd: 0.86%
Claudia: 0.43%
Bernd: 0.43%
alt-Doris: 0.43%
Doris: 0.22%
```
So this is basically the master list that tells you exactly how much DNA each character has from any given ancestor, alt- or regular universe. Mr. Infinity here has 32 ancestors listed.

## Creating your own custom trees
The file ``custom_genealogy.py`` contains instructions for playing with this program yourself! You can modify the family tree as you please and generate your own genealogies with or without the "full" setting. I tried to make it as friendly as possible even for people who have no programming experience. Instructions are provided within the file as comments.

## Methodology
I did this using some math that should be familiar to most people with a math, stats, or CS degree. I'll also try to explain it for people without that background.
### Mathy Explanation
#### "Regular" Genealogy Method
You can model the family tree as a Markov chain wherein the state associated with each person in the tree transitions to each of their parents with probability 0.5. This is represented by an adjacency matrix in which each person's row has an entry of 0.5 for both of their parents. People whose parents aren't in the family tree ("leaves" or "ancestors") just have an entry of 1 in their own column.

We actually don't do what you might expect, which is to find eigenvectors/stationary distribution. I don't know that it'll even converge to a stationary distribution, since the long-run probability of ending in a given state depends heavily on where you start. We actually exponentiate the matrix to a large power, and it converges to a matrix in which the $[i,j]^{th}$ entry represents the probability of a long random walk starting at person $i$ ends at person $j$. This _will_ converge, roughly because the graph has sinks, and you can reach at least one sink from anywhere in the graph. These long-run probabilities correspond to the ancestry percentages!

#### "Full" Genealogy Method
The above method relies on this convergence to the sinks of the graph, and so to get the ancestry percentages corresponding to the non-sinks, I had to try something totally different. I initally tried a method that "pruned" the graph of the sinks after the first round of calculating ancestry and then ran again, and it worked for a bit, but failed once the graph had been pruned down to the cycles. So for example, it would tell me what % of Jonas is Regina, but not what % is Tronte.

Here's the method I hit upon: I created an _unweighted_ adjacency matrix $M$ where each person has an edge to each of their parents. The $[i,j]^{th}$ entry of the $k^{th}$ power of this matrix represents the number of length $k$ paths from vertex $i$ to vertex $j$. In this context, it represents the number of ways in which person $j$ is an ancestor of person $i$ from $k$ generations back. Each such ancestor contributes $\frac{1}{2^(k+1)}$ of person $i$'s ancestry. So we calculate a matrix $G$ representing each person's full genealogy as follows:
$$
G = \sum_{k=1}^\infty M^k\cdot2^{k+1}
$$
(You actually only need to sum up the first 10 terms or so to get very accurate results.)

Now, depending on your point of view, you might contend these results aren't really accurate. For example, Elizabeth's full ancestry says she's 66.6% Charlotte. This is because she's 50% Charlotte from Charlotte being her mother, 12.5% percent Charlotte from Charlotte being her great-grandmother, and so on. You might contend that she's really still just 50% Charlotte, because the extra 16.6% comes from the fact that _Charlotte is 33.3% Charlotte_, and we're double-counting. Unfortunately I've already spent way way too much time on this project given that it's finals season, I only just realized this issue as I was writing this up, and so I'm not fixing it.

## Less Mathy Explanation
#### "Regular" Genealogy Method
Suppose you want to calculate Jonas's ancestry. Imagine you're standing on his name in the family tree on the floor of Eva's base. you flip a coin and, if heads, you walk to Hannah's name. If tails, you walk to Mikkel's name. If you're at Hannah's name, you stop there, but if you're at Mikkel's, you continue the process, flipping a coin to randomly choose one of the current person's parents, until you end up at a person whose parents aren't in the tree. Depending on your sequence of coin flips you might walk in a circle and end up back at Jonas, or even do that multiple times, but _eventually_ you'll always end up at one of the people at the "ends" of the tree. There's some probability of your "random walk" (that's actually a technical term) ending up at each of those people. For example, there's a 50% chance of ending up at Hannah immediately, plus a little extra probability that you circle back to Jonas and then go to Hannah, or go all the way back to Silja and then Hannah.

For each person in the tree, I use some fancy math to calculate the probability they end up at each of the "ends" of the tree. That probability actually is equal to the percentage of the person you started at's ancestry is from the person you ended at. Neat!

#### "Full" Genealogy Method
This works somewhat differently from the "random walk" method above. We're still taking walks, but they're not random. Suppose I walk from Jonas's name to Tronte, his great-grandfather's, name. I walked across 3 people's names to get there (Mikkel, Ulrich, Tronte), so we say that the "length" of this walk is 3. This corresponds to Jonas's ancestry being $\frac{1}{8}=\frac{1}{2^3}$ Tronte. Given a number $k$, We do some fancy math to calculate how many walks of length $k$ there are from Jonas to each of his ancestors. Then we add $\frac{1}{2^k}$ of that person to Jonas's ancestry. We do this for $k=1$, $k=2$, and so on until we're adding such small pieces to Jonas's ancestry that it doesn't really matter anymore. (And we simultaneously do the same thing for every other person in the tree.)

## Random Observations

Some of these observations aren't things that you can infer from the results of this program, just stuff I noticed while building and thinking about this:

- I mentally divided up the characters into a few different categories, as follows:

    - **People who existed in the origin world:** Egon, Doris, Claudia, Bernd, Jana, Regina, Alexander, Hannah, Katharina, Peter
    - **People who could've existed in the origin world, but didn't**: Literally just Bartosz. No Ulrich so Alexander never came out of the woods to defend Regina from Ulrich and Katharina. Poor Bartosz. Poor Alexander too, he probably just bled out there.
    - **People who could've existed without incest or bootstrapping, but not without time travel**: Just Silja, since Egon and Hannah were both unrelated origin world people.
    - **People who could've existed without bootstrapping, but not without incest or time travel**: Agnes, Noah. Bartosz and Silja are un-bootstrapped, but related as Egon is Bartosz's great-grandfather and Silja's father.
    - **Bootstrapped, incesty people**: Charlotte, Elizabeth, Tronte, Ulrich, Mikkel, Marta, Jonas, and Unknown (Marta/Jonas's child) are all products of bootstrapping and incest.

- There are some interesting patterns that emerge when you loosely group everyone into being either a Tiedemann, Doppler, or Nielsen:

  - **Tiedemanns**: Egon, Doris, Claudia, Bernd, Regina, Alexander, (kinda) Hannah, Bartosz, Silja, Noah, Agnes. Note that all these people are un-bootstrapped. Noah and Agnes then both basically went on to start the two bootstrapped families, respectively the Dopplers and Nielsens.
  - **Dopplers**: Noah, Peter, Charlotte, Elizabeth, Franziska (not included) You can't see this in the output of the program unless you modify the family tree by modifying Noah's ancestors, but interesting to note here: the three Doppler women are all descended 100% from Noah and Peter.
  - **Nielsens**: The big bootstrapped family: Agnes, Unknown, Tronte, Jana, Ulrich, Katharina, Martha, Mikkel, Jonas, (kinda) Hannah, Mads (not included), Magnus (not included). There's actually a certain symmetry here to the Dopplers. Agnes is basically the non-bootstrapped matriarch of the whole family, and in fact, all of these bootstrapped Nielsen men are 100% descended from four non-bootstrapped women! Agnes, Hannah (who is Agnes's grandmother), Jana, Katharina.

