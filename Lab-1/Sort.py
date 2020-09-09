#! /usr/bin/env python3

# sort a file full of film names

# define a function that will return the year a film was made
# split the right side of the line at the first ”(”
def filmYear(film):
    return film.rsplit('(',1)[1]

# load the file into a list in Python memory
# and then close the file because the content is now in memory
with open("filmlist", "r") as file:
    filmlist = file.read().splitlines()

# sort by name using library function
#filmlist.sort()

# sort by year using key to library function - the film list
# must end with a year in the format (NNNN)
filmlist.sort(key=filmYear)

# print the list
for film in filmlist:
    print(film)

