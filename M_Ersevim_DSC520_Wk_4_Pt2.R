# Assignment: ASSIGNMENT Week 4, Question #2
# Name: Ersevim, Michael
# Date: 2021-09-25

library(ggplot2)
library(readr)
library(pastecs)
library(dplyr)
library(plyr)
library(hrbrthemes)
library(readxl)
theme_set(theme_minimal())

## Set the working directory to the root of your DSC 520 directory
setwd("/Users/mersevim/OneDrive - Waste Management/Documents/GitHub/dsc520/data")
dir() # check - it works

house_df <- read_excel("week-7-housing.xlsx", col_names = TRUE)

head(house_df)
tail(house_df)

#a.	Use the apply function on a variable in your dataset

sapply(house_df$`Sale Price`,sum)

#b.	Use the aggregate function on a variable in your dataset

aggregate(`Sale Price` ~ bedrooms + present_use, house_df, mean)

#c.	Use the plyr function on a variable in your dataset - more specifically, I want to see you split 
#some data, perform a modification to the data, and then bring it back together

house_df2 <- ddply(house_df, .(sq_ft_lot), mutate,
               Round_Lot = round(sq_ft_lot/100,0)*100) #Creates a new variable which is lot size rounded to nearest 100 ft^2
               
head(house_df2)

#d.	Check distributions of the data

ggplot(house_df2, aes(`Sale Price`)) + geom_histogram(bins=50) + ggtitle("Count of prices") + xlab("Price") + ylab("Counts")

#e.	Identify if there are any outliers
#what is min cut off? Are errors rentals/lease prices? In $000's?

outliers_bed <- house_df2[house_df2$square_feet_total_living  > 2500 & house_df2$bedrooms == 0,] # houses this large and expensive should have >0 bedrooms!!
outliers_price <- house_df2[house_df2$`Sale Price`  > 25000,] #house prices this cheap are likely lease/rental monthly costs

head(outliers_bed)
head(outliers_price)
#f.	Create at least 2 new variables
#take log of sale price
#calculate price/square foot

house_df2$logofprice <- log(house_df2$'Sale Price')

house_df2$costpersqfoot <- (house_df2$'Sale Price'/house_df2$square_feet_total_living)



