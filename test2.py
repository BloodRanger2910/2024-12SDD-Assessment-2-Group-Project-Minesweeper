import pickle

# list of highscoredata
highscoredata = ['4', '2', '5']

# Write list to binary file
def write_list(a_list):
    # store list in binary file
    with open('highscore.txt', 'wb') as fp:
        pickle.dump(highscoredata, fp)

# Read list to memory
def read_list():
    # for reading also binary mode is important
    with open('highscore.txt', 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list


write_list(highscoredata)
r_highscoredata = read_list()
print('List is', r_highscoredata)