# TODO: try different dictionaries and compare performance
# TODO: combine different dictionaries
# TODO: turn into Shiny app?

# libraries
library(tidyverse)
library(qdapDictionaries)



########## EDIT THE STRING OF THE DAY ##########
# first letter should be the center character
str_of_day <- "naopych"



# store letters
ltrs <- NA
for (i in 1:7) {
  ltrs[i] <- substr(str_of_day, i, i)
}

# letters not in string of the day
`%!in%` <- Negate(`%in%`)
badLetters <- letters[which(letters %!in% ltrs)]

# create df of accepted words
df <- data.frame(DICTIONARY) %>% 
  select(word) %>%    # only word column
  filter(nchar(word) >= 4) %>%    # only words length >= 4
  filter(grepl(ltrs[1], word) &    # only words with center letter
           !grepl(paste(badLetters, collapse = "|"), word, fixed = FALSE)) %>%    # only words with accepted letters
  arrange(word)    # alphabetize

# view df
View(df)
