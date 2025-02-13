# Load the gapminder package
install.packages("gapminder") # Install the package if not already installed
library(gapminder)
library(dplyr)
library(tidyverse)

install.packages("vcd")
library(vcd)

# Group by continent and calculate average lifeExp per year
continent_lifeExp <- gapminder %>%
  group_by(continent, year) %>%
  summarize(lifeExp = mean(lifeExp), .groups = "drop") %>%
  split(.$continent) %>%
  lapply(function(df) df %>% select(-continent))

# Print the first element of the list to verify
continent_lifeExp[1]
#########################
gapminder_asia <- gapminder %>% filter(continent == "Asia")
pop_mean_summary <- gapminder_asia %>% group_by(country) %>% summarise(mean_pop = mean(pop))
pop_mean_summary

# Step 3: Add the mean population to the gapminder_asia dataset
asia_pop_mean <- gapminder_asia %>%
  left_join(pop_mean_summary, by = "country")

# Step 4: Filter for rows where population exceeds mean and find the first year for each country
result <- asia_pop_mean %>%
  filter(pop > mean_pop) %>%
  group_by(country) %>%
  summarise(initial_year = min(year), .groups = "drop")

result
#######################
gap_year_filtered <- gapminder %>% filter(year %in% c(1987, 1992, 1997, 2002, 2007))
dim(gap_year_filtered)


gap_summary <- gap_year_filtered %>%
  group_by(year, continent) %>%
  summarise(
    lifeExp = mean(lifeExp),
    pop = mean(pop),
    gdpPercap = mean(gdpPercap)
  )

# Reshape the data into a 3-dimensional array
gapminder_array <- array(
  data = c(
    t(matrix(gap_summary$lifeExp, nrow = length(unique(gap_summary$year)), byrow = FALSE)),
    t(matrix(gap_summary$pop, nrow = length(unique(gap_summary$year)), byrow = FALSE)),
    t(matrix(gap_summary$gdpPercap, nrow = length(unique(gap_summary$year)), byrow = FALSE))
  ),
  dim = c(length(unique(gap_summary$year)), length(unique(gap_summary$continent)), 3),
  dimnames = list(
    year = unique(gap_summary$year),
    continent = c('Africa', 'Americas', 'Asia', 'Europe', 'Oceania'),
    var = c("lifeExp", "pop", "gdpPercap")
  )
)

gapminder_array


#######################    
result_min_max <- apply(gapminder_array, c(1, 3), function(x) c(Min = min(x), Max = max(x)))
result_min_max

######################
for (year in c("1987", "1992")) {
  cat("\n, , year =", year, "\n")
  print(gapminder_array[year, , ], quote = FALSE)
}
######################

heart = read_csv('GitProjects/School-Assignments/MATH208/heart.csv')
# Create the contingency table
sex_disease <- table(heart$HeartDisease, heart$Sex)

# Print the contingency table
print(sex_disease)

# Use assocstats to derive statistics, including Cramer's V
assoc_stats <- assocstats(sex_disease)

# Output Cramer's V
cat("\nCramer's V:", assoc_stats$cramer, "\n")
#########################

# Create the contingency table
angina_disease <- table(heart$HeartDisease, heart$ExerciseAngina)

# Print the contingency table
print(angina_disease)

# Calculate the Odds Ratio
odds_ratio <- (angina_disease[2, "Y"] / angina_disease[1, "Y"]) /
  (angina_disease[2, "N"] / angina_disease[1, "N"])

# Output the Odds Ratio
cat("\nOdds Ratio (OR):", odds_ratio, "\n")


#############


# Calculate the Pearson correlation coefficient
correlation <- cor(heart$RestingBP, heart$MaxHR, method = "pearson")

# Output the correlation
cat("\nPearson Correlation Coefficient:", correlation, "\n")










