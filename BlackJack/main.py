import random
import os
from art import logo

def deal_card():
  cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
  card = random.choice(cards)
  return card

def calculate_score(cards):
  if sum(cards) == 21 and len(cards) == 2:
    return 0
  if 11 in cards and sum(cards) > 21:
    cards.remove(11)
    cards.append(1)
  return sum(cards)

def compare(user_score, computer_score):
  if user_score == computer_score:
    print("It's a draw!")
  elif computer_score == 0:
    print("The opponent has a Blackjack. You lose!")
  elif user_score == 0:
    print("You got a Blackjack! You win!")
  elif user_score > 21:
    print("You went over. You lose!")
  elif computer_score > 21:
    print("The opponent went over. You win!")
  else:
    score = max(user_score, computer_score)
    if user_score == score:
      print("You got the higher value. You win!")
    else:
      print("The opponent has a higher value. You lose!")

def play():
  print(logo)
  user = []
  comp = []
  for i in range(2):
    user.append(deal_card())
    comp.append(deal_card())
  game = False
  while game == False:
    user_score = calculate_score(user)
    computer_score = calculate_score(comp)
    print(f"  Your cards: {user}, current score: {user_score}")
    print(f"  Computer's first card: {comp[0]}")
    if computer_score == 0 or user_score == 0 or user_score > 21:
      game = True
    else:      
      if input("Do you want to draw another card? Type 'y' or 'n': ") == 'n':
        game = True
      else:
        user.append(deal_card())
  while computer_score != 0 and computer_score < 17:
    comp.append(deal_card())
    computer_score = calculate_score(comp)
  print(f"   Your final hand: {user}, final score: {user_score}")
  print(f"   Computer's final hand: {comp}, final score: {computer_score}")
  compare(user_score, computer_score)
  
while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
  os.system('cls')
  play()