# SP500 Percentage Predictor
This program predicts a one month price change based off of 10 years of historic data
for each stock in the SP500 using Python. Calculating at least a 90% success rate (9/10 years)
between the same time periods. This produce a csv file that has a years worth of 
stock picks and their respective percentage change during that price change. This is a console Project
## Packages
* Pandas
* Pandas DataReader
* Numpy
* Datetime
* BeautifulSoup4
* MatPlotLib
* MatPlotLib.pyplot
* os & shutil (for deleting and creating paths)
* Pickle
* Requests
## Example Results
 *Ticker* | *Start Date* | *End Date* | *Avg % Change* | *Outlier Year* 
 ---------|--------------|------------|----------------|----------------
 FISV | 06-08 | 07-08 | 3.25 | 2017
 AIZ | 06-08 | 07-08 | 4.629 | 2014
 JWN | 12-31 | 02-01 | -5.26 | 2015
 * Note that start date and end data will be a datetime object, so when reading
 in will have to parse out the year because it does not matter.
 * Percent Change and Year are Float objects
 * Outlier Year is the year where during that time period the stock had an opposite 
 price change. If Outlier Year is a NaN value, then the stock had 100% positive or negative price
 change during that time period.
## Contact
 Phone: (971) 708-4444<br />
 Email: ericsanderson333@gmail.com<br />
 Linkedin: https://www.linkedin.com/in/ericanderson333 <br />
 Bitcoin Wallet: 39PWQqypjfiFdqfn2pSZZ88KaWNf5GhesE <br />
 Please contact me and send me any questions/advice! Thanks!
 


 
 
 
