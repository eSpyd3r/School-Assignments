heights = c(145.5, 189.7, 183, 135.3, 175, 178, 162, 102, 168.8, 195.2)
names(heights) = LETTERS[1:10]
print(heights)
#Output:
#  A     B     C     D     E     F     G     H     I     J 
# 145.5 189.7 183.0 135.3 175.0 178.0 162.0 102.0 168.8 195.2

heights_eval <- rep(0,10)
heights_eval[heights < 150] <- "short"
heights_eval[heights >= 150 & heights <= 185] <- "pass"
heights_eval[heights > 185] <- "tall"
print(heights_eval)
#Output:
#[1] "short" "tall"  "pass"  "short" "pass"  "pass"  "pass"  "short" "pass"  "tall"

print(names(heights[heights >= 150 & heights <= 185]))
#Output:
#[1] "C" "E" "F" "G" "I"

heights_price <- rep(0,10)
heights_price[heights_eval == "short"] <- 3
heights_price[heights_eval == "pass"] <- 4
heights_price[heights_eval == "tall"] <- 5
print(sum(heights_price))
#Output:
#[1] 39
############

shopping_list <- list(
  Grocery = list(
    Dairy = c("Milk","Cheese"),
    Meat = c("Chicken","Sausage","Bacon"),
    Spices = c("Cinnamon")
  ),
  Pharmacy = c("Soap","Toothpaste","Toilet Paper")
)

shopping_list$Pharmacy #Output:[1] "Soap"         "Toothpaste"   "Toilet Paper"
shopping_list[1][[2]] #Output: Error in shopping_list[1][[2]] : subscript out of bounds
shopping_list[[1]][[3]] #Output: [1] "Cinnamon"
shopping_list$Grocery[2][1] #Output: $Meat [1] "Chicken" "Sausage" "Bacon"
#General concept: [] returns list, [[]] returns object itself, not list of object

shopping_list[[1]][[2]][2] #Output: [1] "Sausage"
shopping_list$Grocery$Meat[2] #Output: [1] "Sausage"
shopping_list[[1]][2][[1]][[2]] #Output: [1] "Sausage"

shopping_list$Hardware = c("Packaging Tape", "Pack of Nails")
shopping_list
#Output:
#$Grocery
#$Grocery$Dairy
#[1] "Milk"   "Cheese"
#
#$Grocery$Meat
#[1] "Chicken" "Sausage" "Bacon"  
#
#$Grocery$Spices
#[1] "Cinnamon"
#
#
#$Pharmacy
#[1] "Soap"         "Toothpaste"   "Toilet Paper"
#
#$Hardware
#[1] "Packaging Tape" "Pack of Nails"

shopping_list$Grocery$Spices = NULL
shopping_list$Grocery$Veggies <- c("Onions", "Carrots")
shopping_list

#$Grocery
#$Grocery$Dairy
#[1] "Milk"   "Cheese"
#
#$Grocery$Meat
#[1] "Chicken" "Sausage" "Bacon"  
#
#$Grocery$Veggies
#[1] "Onions"  "Carrots"
#
#
#$Pharmacy
#[1] "Soap"         "Toothpaste"   "Toilet Paper"
#
#$Hardware
#[1] "Packaging Tape" "Pack of Nails" 
#############

column_names <- names(data_q3)
column_types <- sapply(data_q3, typeof)
names(column_types) = column_names
print(column_types)
# Output:
#  carat       cut     color   clarity     depth     table     price         x         y         z
# "double" "integer" "integer" "integer"  "double"  "double" "integer"  "double"  "double"  "double" 

unique(data_q3$cut)
#Output:
#[1] Ideal     Premium   Good      Very Good Fair     
#Levels: Fair < Good < Very Good < Premium < Ideal
# There are 5 different/"unique" cuts in the data set

head(subset(data_q3, cut == "Premium"), 5)
#Output:
# A tibble: 5 × 10
#carat cut     color clarity depth table price     x     y     z
#<dbl> <ord>   <ord> <ord>   <dbl> <dbl> <int> <dbl> <dbl> <dbl>
#1  0.21 Premium E     SI1      59.8    61   326  3.89  3.84  2.31
#2  0.29 Premium I     VS2      62.4    58   334  4.2   4.23  2.63
#3  0.22 Premium F     SI1      60.4    61   342  3.88  3.84  2.33
#4  0.2  Premium E     SI2      60.2    62   345  3.79  3.75  2.27
#5  0.32 Premium E     I1       60.9    58   345  4.38  4.42  2.68

distinct(subset(data_q3, (cut == "Premium") | (cut == "Ideal")), clarity)
#Output:
# A tibble: 8 × 1
#clarity
#<ord>  
#1 SI2    
#2 SI1    
#3 VS2    
#4 VS1    
#5 I1     
#6 VVS2   
#7 VVS1   
#8 IF  

########

data_q4$year = NULL
names(data_q4)
#Output:
#[1] "month"          "day"            "dep_time"       "sched_dep_time" "dep_delay"      "arr_time"      
#[7] "sched_arr_time" "arr_delay"      "carrier"        "flight"         "tailnum"        "origin"        
#[13] "dest"           "air_time"       "distance"       "hour"           "minute"         "time_hour"

data_q4_filtered = subset(data_q4, (month == 12) & (day == 25))
head(data_q4_filtered, 6)
#Output:
# A tibble: 6 × 18
#month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay carrier flight tailnum origin dest 
#<int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl> <chr>    <int> <chr>   <chr>  <chr>
#1    12    25      456            500        -4      649            651        -2 US        1895 N156UW  EWR    CLT  
#2    12    25      524            515         9      805            814        -9 UA        1016 N32404  EWR    IAH  
#3    12    25      542            540         2      832            850       -18 AA        2243 N5EBAA  JFK    MIA  
#4    12    25      546            550        -4     1022           1027        -5 B6         939 N665JB  JFK    BQN  
#5    12    25      556            600        -4      730            745       -15 AA         301 N3JLAA  LGA    ORD  
#6    12    25      557            600        -3      743            752        -9 DL         731 N369NB  LGA    DTW  
# ℹ 5 more variables: air_time <dbl>, distance <dbl>, hour <dbl>, minute <dbl>, time_hour <dttm>
data_q4_filtered$dep_hour <- data_q4_filtered$dep_time%/%100
head(data_q4_filtered[c("dep_time", "dep_hour")])
#Output:
# A tibble: 6 × 2
#dep_time dep_hour
#<int>    <dbl>
#1      456        4
#2      524        5
#3      542        5
#4      546        5
#5      556        5
#6      557        5

sum(is.na(data_q4_filtered))
#Output: [1] 24

sum(is.na(data_q4_filtered$dep_time))
#Output: [1] 4







