----------------------------------------------------------------------------------------------------------------
Documentation for COMP370 Final Project

Last Update: November 18th 

----------------------------------------------------------------------------------------------------------------
                            Project:

Hired by a media company concerned with North American coverage of zohran mamdani and:

(1) whether coverage is positive or negative
(2) what topics the coverage focuses on


Value we want to inevetibly provide to the media company:


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Question Formulation

1) Is North American coverage of zohran mamdani positive or negative and what topics does the coverage focus on

    notes: 
    
        very vauge, we wont have any topics,
        nor do we have any idea about the type of media sources we want to focus on, or the scale/region of that 
        essentially doesnt answer any fundamental question (for the media company), lets work on refining that

    value provided to media company:

        not much, just some random information at the moment


2) Is the coverage by national right-leaning media outlets of zohran mamdani positive or negative, and what topics does the coverage focus on

    notes:

        choosing national right wing media outlets is a natural choice, as it is implied that the left wing speaks about ZM positively (could also do the opposite). Will need to do secondary research on prominant right-wing outlets
        next steps are to refine how we define positive or negative, topics category

    value provided to media company:

        Tells them about the right wing media coverage of ZM

3) What percentage of coverage by North American national right-leaning media outlets of zohran mamdani is positive, negative or neutral? What are the 3-8 most prominant topics focused on by this coverage

    notes:

        starting to refine how we are going to classify positive or negative coverage (percentage) - this is going to need some more work and need a comprehensive typology to define positive / negative

    value provided to media company:

        They can use this information to determine what the right wing is saying about this politician, and how consumers of right wing media's opinions are being shaped. This can provide value to the media team



*this is one potential route we can go to get even more specific with the question and provide more value to the media company

4) Before and after the NYC mayoral election, what percentage of coverage by North American national right-leaning media outlets of zohran mamdani is positive, negative or neutral? What are the 3-8 most prominant topics focused on by this coverage

    notes:

        adding an actual time frame (ie this week (post election) versus last month (before the election))
        Can extend further and analyze the topics that have been discussed before and after the election.

    value:
        Can provide insight into the shift in the right-wings opinion of ZM that has occured before and after the election

    
5) Before and after the NYC Mayoral election (on November 4th, 2025), how has the "favourabilty" of coverage (% change) by American National Media across the politicl spectrum changes? What are the 3-8 most prominant topics focused on by this coverage?

    Notes:
        changed from right --> across the spectrum to better adjust to our avaliable data

    value:
        provides the media company with information regarding how/if media coverage has changed before and after the mayoral election

5.5) Before and after the NYC Mayoral election (on November 4th, 2025), how does the favouribility of coverage from american national media change across different media bias' (Right Center, Left). What are the most prominant topics focused on by this coverage by each side of the spectrum? Has there been a change in these trends pre/post mayoral election?

    Notes:
        changed from 5), where we slightly reframe the question to explore different biases instead of exploring opinion before and after the election. 
        should we be open coding seperate topics for each bias? -> no , lets open code a list of 3-8 unified topics and then analyze if there is a difference across the spectrum
    value:
        provides the media company with information regarding what the coverage from different media bias' is like, and if any of this coeverage has changed pre/post election
    
        



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Flow plan --> article collection --> data cleaning --> open coding (devlop our typology) --> manual annotation & characterization--> analysis --> report/communicate

Task 1 : Article collection

    - Split into collecting 250 articles post election, 250 articles pre election 

    - Need to make sure we are being representative with the news outlets chosen (ie, don't use 249 fox articles pre and 1 post, make sure you are being relatively consistent) --> how can we ensure this?

    -Could also collect all across the spectrum, ensuring that we collect an equal number of right , left and neutral leaning

    - May have to peel back on the "only right wing sources" if it proves very scarce to find --> how can we collect enough articles? current api isn't awesome (limit of 100)



Task 2 : Cleaning

    -Clean the data, make a csv with columns:  id, date (pre or post), source, title, opening. 
    -Later we will add columns : "positive or negative coverage, and topic covered"

Task 3: coding

    - Using a totally random sample of 200 articles, start trying to devlop different topics for each article (1), essentially we are just creating another column of the data called 
    "topic label"
    -open code to develop a typology as to whether posts are positive negative or neutral (2)

Task 4; manually annotate & characterize 
    - manually annotate the rest of the (300) articles using your typologies for (1) and (2)
    - Characterize the topics (1) by using tf-idf and an LLM to produce a representative summary (ie just summarizing all the most common words in all the posts included in that topic)

Task 5: Analyze
    - Find some trends pre and post election
    - Communicate these in a report to the media company that hired you

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Article collection

Political Bias--> working plan (nov 18th): collect an equal amount of articles across the political spectrum using a media criteria found in literature and sources available on the API


//The bias bucketing was done using https://www.allsides.com, however this could be a major source of error in the analysis//

//Only using major national media sources//

    Left : "sources": "msnbc,the-huffington-post,the-washington-post,newsweek,politico,vice-news,new-york-magazine, nbc-news, cnn, associated-press",
    Center : "sources": "bloomberg, cbs-news,reuters,abc-news,the-wall-street-journal,usa-today,the-hill,time,axios",
    Right: "sources": "breitbart-news,fox-news,national-review,the-american-conservative,the-washington-times"

    Aim to collect 150-200 left , 150-200 center, 150-200 right, ensure that right and left have a balanced number 


Pre/Post election --> for each of the defined bias sets, collect an equal number of articles pre/post election (November 4th, 2025). 

    On Nov 18th, collect 14 days before and 14 days after election (oct 21 - nov 18th), to aim for equal representation pre/post election



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Open coding

- wrote a quick script that can combine out jsons into a csv, removing the data we dont need (ie author) and keeping the data we do need

conducted open coding on a systemic subset of 200 articles

--> open coding on a set of ~200 articles, to come up with 3-8 types (topics) in a category (article) 
    -goal of this coding: find 3-8 common topics across all of the articles. Be able to annotate the rest of the articles to fit within these topics
    -conduct open coding across all types of media bias , come up with a uniform set of topics and then compare each of them across eachother







