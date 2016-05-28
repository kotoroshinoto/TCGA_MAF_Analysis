library(MASS)

#y: vector of gene count
#x: vector of correponding gene length
x <- c(,,...)
y <- c(,,...)

g <- lm(y~x)

#studentized residuals
#find which ones are grester than 2 
#then they are classified as outliers with strong positive effects
studres(g)
