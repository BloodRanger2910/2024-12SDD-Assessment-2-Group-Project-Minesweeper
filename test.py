import pickle

time = 0

highscoredata = ['truck', 'tow', 'car']

# open file in write mode
with open(r'highscore.txt', 'w') as fp:
    for item in highscoredata:
    # write each item on a new line
        fp.write("%s\n" % item)
#compare if time is in top 5
#if time is in top 5 -> insertion sort time into list -> remove after 4th index -> update persistence

# empty list to read list from a file
names = []

# open file and read the content in a list
with open(r'E:\demos\files_demos\account\sales.txt', 'r') as fp:
    for line in fp:
        # remove linebreak from a current name
        # linebreak is the last character of each line
        x = line[:-1]

        # add current item to the list
        names.append(x)

# display list
print(names)

        
