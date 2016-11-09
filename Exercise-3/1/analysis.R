library(ggplot2)

data(diamonds)
summary(diamonds)

# Variables for easier access
carat   = diamonds$carat
cut     = diamonds$cut
color   = diamonds$color
clarity = diamonds$clarity
depth   = diamonds$depth
price   = diamonds$price
volume  = diamonds$x * diamonds$y * diamonds$z
table   = diamonds$table


maxCorrelation = function()
{
  priceCaratCor   = cor(price, carat)
  priceDepthCor   = cor(price, depth)
  priceVolumeCor  = cor(price, volume)
  priceTableCor   = cor(price, table)
  
  correlationsList = c("Price-Carat with corr coefficient" = priceCaratCor, 
                       "Price-Depth with corr coefficient " = priceDepthCor,
                       "Price-Volume with corr coefficient" = priceVolumeCor,
                       "Price-Table with corr coefficient" = priceTableCor)
  
  sortedCorrelations = sort(correlationsList, decreasing = TRUE)
  
  return(sortedCorrelations)
}

main = function ()
{
  print("Correlations for: ")
  print( maxCorrelation())
  
  # Density plot for carat since it is the one, for which the price correlates the most
  #qplot(carat, data = diamonds, geom = "density")  -- DONE
  
  # The plot leads to the assumption that price and carat might have a exponential model as relation
  #qplot(log(carat), log(price), data = diamonds) + geom_smooth(method="lm") -- DONE
  
  # Depth seems to be Normal distributed, but why isn't it reflected in the price?
  qplot(depth, data = diamonds, geom = "density") #
  
  # Strong correlation also with price and volume, so plot price/volume scatter plot
  # Clearly, price rises exponentially with volume, but there are quiet a lot of outliers maybe due to carat?
  # Also the variance seems to increase with volume
  #qplot(log(volume), log(price), data=diamonds) + geom_smooth(method = "lm")
  
  #g = qplot(log(carat), log(price), data=diamonds)
  #g + geom_point() + facet_grid(. ~ cut)
  
  #g2 = qplot(log(carat), log(price), data=diamonds)
  #g2 + geom_point(color="red") + facet_grid(. ~ color)
  
  # Shows really nicely the difference that clarity has on the price!
  #p = qplot(log(carat), log(price), colour=clarity, data=diamonds)
  #p
  
  # Strong correlation between carat and volume obviously
  print(cor(carat,volume))
  
  # Shows that volume and carat are correlated 
  #p = qplot(log(carat), log(price), data=diamonds) + geom_point(aes(size=volume))
  #p
  
  # Shows no influence of depth on price
  #p = qplot(log(carat), log(price), alpha=depth, data=diamonds)
  #p
  
  # Carat and volume have a linear relationship altough quiet a lot outliers! How can that be??
  #p = qplot(carat, volume, data=diamonds)
  #p
  
  
  pdf(file="mypdf.pdf")
  # Shows how price per carat is distributed over colors (see reference link on pc for explanation!)
  p = qplot(color, price/carat, data = diamonds, geom = "boxplot")
  p
  dev.off()
  
   
}

main()