import time
import undetected_chromedriver as uc
import Methods as m
import DeepSeekAPiCalls as d

# Configure Chrome Options
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/Users/patricklu/Library/Application\\ Support/Google/Chrome/")
options.add_argument("--profile-directory=Profile 4")  # Ensure correct profile

driver = uc.Chrome(options=options)
driver.get("https://www.pokernow.club/games/pgltnJOTG6U6enUeznKGj_s__")
print("PokerNow is open!")

time.sleep(5)

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
            your_bet = m.your_bet(driver)

            print("\n-------------------- GAME STATE --------------------")
            print(f"Board:         {m.format_cards(board)}")
            print(f"Pot Size:      {pot_size}\n")

            print(f"Your Hand:     {m.format_cards(hand)}")
            print(f"Your Stack:    {stack}")
            print(f"Your Bet:      {your_bet}\n")

            print(f"Opponent Stack: {opponent_stack}")
            print(f"Opponent Bet:   {opponent_bet}")
            print("---------------------------------------------------\n")

            action = d.get_ai_decision(hand, board, position, stack, opponent_stack, opponent_bet, pot_size)
            print(f"AI Decision:   {action}\n")

            m.perform_ai_action(driver, action[0], action[1])
            time.sleep(2)

        else:
                print("Waiting for your turn...")
                while not m.your_turn(driver):
                    time.sleep(5)

except Exception as e:
    print(f"Error: {e}")