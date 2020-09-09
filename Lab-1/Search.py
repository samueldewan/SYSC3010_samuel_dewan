#! /usr/bin/env python3

# sort a file full of film names

searchfor = input("Enter part of the film " +
                  "name you are searching for: ").lower().strip()

# use the built-in filter function, which will call the first parameter on every
# item in the iterator passed to it and return an interator of only the items
# for which the call to the first parameter returned True
with open("filmlist", "r") as film:
    foundlist = filter(lambda i: searchfor in i.lower(), film)
    
    for name in foundlist:
        print(name.strip())

