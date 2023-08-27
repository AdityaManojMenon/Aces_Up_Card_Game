#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 19:34:12 2023

@author: adi
"""

import cards  # required !!!
import random 
################################################################################
# CSE 231 Project 10c
#Write a function that displays the stock, foundatoin, and tableau with cards. Then write a function which deals the cards to all 4 colunms while the stock is not empty.
#Then write a functions which validates and executes the movement of cards from tableau to foundation based on their suit and rank number. 
#Then write a functions which validates and executes the movement of cards within the tableau based on whether a cloumn is empty or not in the tableau. 
#The write a function which checks if the game is won which occurs when stock is empty and the only cards left in the tableau are ace's.
#Write a fucntion does all the error checks when the user is inputting their options
#The main rquires to call the functoins based on user input and returns the updated display after each move. If the move is illegal or in possible and error message is displayed and user is prompted to re enter a valid move. Also the program only breaks when its won or the user quits.             
################################################################################

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    """
    This code defines a function named "init_game" that initializes a game of cards.
    This is achieved by using the functions in the cards.py file.
    """
    stock = cards.Deck() # call the deck class form cards.py
    stock.shuffle()
    tableau = []
    for i in range(4): # 4 because 4 columns in tableau
        inner_list = []
        inner_list.append(stock.deal())
        tableau.append(inner_list)
    foundation = [] #intially foudation is empty
    return stock, tableau, foundation

    
def deal_to_tableau( tableau, stock):
    """
    This fucntion is used to deal cards to each of the 4 columns of the tableau if stock isn't empty.
    """
    num_cols = len(tableau)

    # Deal a card from the stock to each column of the tableau
    for i in range(4): # i is column
        if stock.is_empty() == False: # can only deal cards when stock isn't empty
            deal_card = stock.deal()
            tableau[i].append(deal_card) # deal one card each column of tableau
        else:
            break

    # If the stock has fewer than 4 cards, deal one card to consecutive columns until the stock is empty
    if stock.__len__() < 4:
        i = 0
        while stock.is_empty() == False:
            deal_card = stock.deal()
            tableau[i].append(deal_card)
            i = (i + 1) % 4



def validate_move_to_foundation( tableau, from_col ):
    """
    This function checks if the last card of each column of the tableau could be moved to foundation based on the its suit and rank.
    """

    if len(tableau[from_col]) == 0:
        print("\nError, empty column:{from_col}")
        return False
    
    move_card = tableau[from_col][-1]#last card of eacb column can only be moved if the necessary criterias are satisfied
    if move_card.rank() == 1:
        print(f"\nError, cannot move {move_card}.")
        return False
    for tab in tableau:
        try:
            if tab[-1].rank()==1 and tab[-1].suit() == move_card.suit(): 
                
                return True
            elif move_card.rank() < tab[-1].rank() and move_card.suit()==tab[-1].suit():#if the card is of lower rank with same as the suit as another last card in another column of tableau that card can be moved to foundation therefore returns True.
         
                return True
            else:
                continue
        except:
            continue
    print(f"\nError, cannot move {move_card}.")
    return False


def move_to_foundation( tableau, foundation, from_col ):
    """
    This functions executes the action by first calling the validate function to make sure if the card can be appended to the foundation
    """
    if not validate_move_to_foundation(tableau, from_col):# if not validated returns None
        return None
    else:
        move_card = tableau[from_col].pop()# removes the last card from specified column and moves to foundation when validated.
        foundation.append(move_card)


def validate_move_within_tableau( tableau, from_col, to_col ):
    """
    The fucntion checks if a column is empty and if the last column of any other column can be moved to the empty column.
    """
    if len(tableau[to_col])>0:# if the cloumn already has cards the last card form another column can't be moved to the column with cards
        print("\nError, target column is not empty:", to_col+1)
        return False

    elif len(tableau[from_col]) == 0: # if a column has no cards the program can't move anything from that empty column to non-empty column
        print("\nError, no card in column:", from_col+1)
        return False

    else:
        return True


def move_within_tableau( tableau, from_col, to_col ):
    """
    This function executed the process when the validate function is satisfied.
    """
    if not validate_move_within_tableau( tableau, from_col, to_col ):
        return None # if not validated returns None
    else:
        move_card = tableau[from_col].pop() #removes the last card from specified column and moves to anthoer empty column when validated.
        tableau[to_col].append(move_card)
        return tableau
        

def check_for_win( tableau, stock ):
    """
    The write a function which checks if the game is won which occurs when stock is empty and the only cards left in the tableau are ace's.
    """
    if stock.is_empty() == False: # if stock is not empty game is not yet over so can't win therefore return false
        return False
    for col in tableau:
        for card in col:
            if card.rank() != 1: # when stock is empty if there is any card execpt 4 aces then return false
                return False
    else:
        return True



def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    """
    This fucntion does all the error checks when the user is inputting their options
    """
    while True:
        option = input("\nInput an option (DFTRHQ): ")
        list1 = []
        list_alpha = ["D","F","T","R","H","Q"]
        list_int = [1,2,3,4]
        options = option.split(" ") # converts the options to list
        if len(options) == 1:
            if options[0].upper() in list_alpha and options[0].upper()!="F" and options[0].upper()!="T":
                list1.append(options[0].upper()) # a
                return list1
            else:
                print(f"\nError in option: {option}")
                return []
        elif len(options) == 2:
            if options[0].upper() in list_alpha and int(options[1]) in list_int and options[0].upper()!="T":
                list1.append(options[0].upper())
                list1.append(int(options[1])-1)# changes column number from 1 to 4 back to 0 to 3.
                return list1
            else:
                print(f"\nError in option: {option}")
                return []
        elif len(options) == 3:
            if options[0].upper() in list_alpha and int(options[1]) in list_int and int(options[2]) in list_int and options[0].upper()!="D":
                list1.append(options[0].upper())
                list1.append(int(options[1])-1) # takes the column of the last card
                list1.append(int(options[2])-1) # takes last card to the empty column
                return list1
            else:
                print(f"\nError in option: {option}")
                return []
                continue

def main():
    """
    The main rquires to call the functoins based on user input and returns the updated display after each move. If the move is illegal or in possible and error message is displayed and user is prompted to re enter a valid move. Also the program only breaks when its won or the user quits. 
    """
    print(RULES)
    print(MENU)

    stock, tableau, foundation = init_game() # intializes the stock, tableau, and foundation 
    display( stock, tableau, foundation )#inital display in the beinging of the game
    
    while True:
        ans = get_option()
        if len(ans) == 0:
            continue
        if ans[0] == "D": # deals the cards 
            deal_to_tableau( tableau, stock)
            display( stock, tableau, foundation )

        elif ans[0] == "F":
            move_to_foundation( tableau, foundation, ans[1]) # moves the card to foundation based the suit and rank of the last cards of each column.
            if check_for_win( tableau, stock ) == True: # always checks if the game could be won 
                print("\nYou won!")
                break
            display( stock, tableau, foundation )
            
        elif ans[0] == "T":
            move_within_tableau(tableau, ans[1], ans[2]) # moves the last card of column to an empty column.
            if check_for_win( tableau, stock ) == True:# always checks if the game could be won 
                print("\nYou won!")
                break
            display( stock, tableau, foundation )

        elif ans[0] == "R": # restarts the game
            print("\n=========== Restarting: new game ============")
            print(RULES)
            print(MENU)
            stock, tableau, foundation = init_game()
            display( stock, tableau, foundation )

        elif ans[0] == "H": # displays the rules
            print(MENU)
            display( stock, tableau, foundation )

        elif ans[0] == "Q" or ans[0] == "q": # quits the game
            print("\nYou have chosen to quit.")
            break
        
    
        

if __name__ == '__main__':
     main()
