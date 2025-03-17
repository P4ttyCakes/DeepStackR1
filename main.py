

import time
import undetected_chromedriver as uc
from selenium.webdriver import Keys

import Methods as m
import DeepSeekAPiCalls as d
from selenium.webdriver.common.by import By

from Methods import perform_ai_action, in_opening_range

# Configure Chrome Options
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/Users/patricklu/Library/Application\\ Support/Google/Chrome/")
options.add_argument("--profile-directory=Profile 4")  # Ensure correct profile

driver = uc.Chrome(options=options)  # Removed use_subprocess=True
driver.get("https://www.pokernow.club/games/pglD0COYpPA6GnM-rG808heNC")
print("✅ PokerNow is open!")




time.sleep(15)

try:
    while True:
        if m.your_turn(driver) == True:

            hand = m.get_player1_hand(driver)
            board = m.get_board(driver)
            position = m.position(driver)
            stack = m.get_stack(driver)
            opponent_stack = m.opponent_stack(driver)
            opponent_bet = m.opponent_bet(driver)
            pot_size = m.get_pot_size(driver)
            # Format the hand and board for better readability

            print("Board:", board)
            print("Position:", position)
            print("Player 1 Hand:", hand)
            print("Your Stack:", stack)
            print("Your Bet:", m.your_bet(driver))
            print("Opponent Stack:", opponent_stack)
            print("Opponent Bet:", opponent_bet, "\n\n")
            print("Pot Size:", pot_size)


            if len(board) == 0:
                if in_opening_range(hand, position) == False:
                    print("Not in opening range, folding...")
                    m.click_Fold(driver)
                    continue

            print("In opening range, proceeding with the game...")
            action = d.get_ai_decision(hand, board, position, stack, opponent_stack, opponent_bet, pot_size)
            print("AI Decision:", action)
            perform_ai_action(driver, action[0], action[1])
            time.sleep(3)

        else:
            print("Waiting for your turn...")
            time.sleep(3)



except Exception as e:
    print(f"❌ Error: {e}")