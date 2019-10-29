# GoogPredAPI

Attempt to use the Google Prediction API to predict amazon product ratings based on product review features.

For this task, I use the amazon review data in json format.

## Usage:
`python amazon_predictions.py "bucket/object" "model_id" "project_id"`

## Architecture of the script files:

### amazon_predictions.py
Script to train model on input data and write results to the prediction file. The prediction file has actual
rating alongside the predicted rating.

### PredAPI.ipnb
Script to clean and prepare the data to a format suitable for the prediction API. It also shows the results
of the predictions (accuracy, confusion matrix).
 
### PredAPI10kfold.ipnb
Script to clean and prepare the data to a format suitable for the prediction API. It also shows the results
of the predictions (accuracy, confusion matrix). 

## Modelling Approach and Data description:
The dataset consists of reviews from Amazon. Reviews include product and user information and a 
plaintext review. There are a million json data objects in the data file. I use 3 approaches to test the 
accuracy of my models:

### Approach 1. 
Split the data file into a training set (99% of the data, i.e, 990000 data points) and a test
set (1% of the data-10000 data points).
### Approach 2. 
Same as approach 1, but here I include an additional feature in the training and the test set - 
the categories of the product. To understand the category feature, we need the look at the structure of a
typical data point:

```
{
  'itemID': 'I184686836',
  'rating': 2.0,
  'helpful': {'nHelpful': 1, 'outOf': 1},
  'reviewText':'well the price of this watch is 23 dollars, but it is better to add extra and buy better product',
  'reviewerID': 'U064132109',
  'summary': "doesn't worth it",
  'unixReviewTime': 1348185600,
  'category': [['Clothing, Shoes & Jewelry', 'Women', 'Watches', 'Wrist Watches']],
  'reviewTime': '09 21, 2012'
}
```
Going by the tips given to make the predictions more accurate, I eliminated fields which described the same
attribute. Hence I removed `reviewTime` and  `summary` and insted kept `unixReviewTime` and `reviewText`
respectively.

To avoid complexity, in Approach 1 I avoided having a feature for the categories as there wasn't a straight-forward 
way of converting the catergories into a form acceptable by the API. The categories is a 2 dimensional array with 
each sub-array showing a different way to browse the product in Amazon. 

Google Prediction API suggests that we need to include as many features as possible. So in Approach 2, I convert 
the categories into a string with each element in a subarray seperated by a "-" (indicating hierarchy in the 
category) and each level separated by a "_" instead of spaces as the underlying algorithms automatically separate
all strings on spaces. Also if we have more then one category then each category is separated by a space so that 
the API detects and splits the category feature into different categories. To explain this better let us take an 
example:

`'category': [['Clothing, Shoes & Jewelry', 'Women', 'Watches', 'Wrist Watches'],['Wrist Watches']]`

So here the hierarchy is `'Clothing, Shoes & Jewelry' -> 'Women' -> 'Watches' -> 'Wrist Watches'` and `'Wrist Watches'`

We would represent this as: `'Clothing,_Shoes_&_Jewelry-Women-Watches-Wrist_Watches  Wrist_Watches'`

### Approach 3: 
What Approach 1 and Appraoch 2 lacked was a reasoned way to split the data into training and test sets.
Also, the distribution of the original data is non uniform in the number of data points for each labelled 
ratings. Therefore, in this approach, I use the 10 fold cross validation method. From a million data points,
I prepared a dataset of 100,000 objects split equally among the 5 labelled ratings. On this dataset I used the 
10 fold cross-validation method wherein I split the data into 10 parts of 10,000 each and on each of the 10 
iterations of modelling the data, one of the parts was chosen to be the test set and the rest was made the 
training data on which the model was built.
