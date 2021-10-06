# Wikipedia NLP Project
Author: Nitya Krishna Kumar

This project seeks to answer two questions:
1. What are the 100 most commonly used words in the body of the articles 
in these Wikipedia pages? The body is the section with the `<text>` heading.
2. Given a singluar article within the dataset, what are the 10 words that 
would be most useful to detect articles that are similar to it? 

## Additional Notes:
### Dataset
The dataset is a Wikimedia XML data dump. I used Aaron Halfaker's `mwxml`
package to load in this data. Documentation can be found at https://pythonhosted.org/mwxml/.

As the file was extremely large and my computer did not have the proper memory 
required to process such a large file, I have only looked at the first 10,000
articles. To look at a differnt number of articles, simply change the `LIMIT`
variable.

### Question 1
#### Stopwords
There may be additional stopwords other than the ones I have specified. An example
would be words in relation to links (web addresses) in the document. Such words are
not as common, therefore, the likelyhood that they will be among the top 100
words is low. However, it is still important to consider how to incorporate them
as stopwords.

#### Output
The program will output a file named "hundred_largest.csv". This will contain
the top hundred words that have shown up in the top "`LIMIT`" (10,000) articles.




