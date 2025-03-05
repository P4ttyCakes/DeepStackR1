import time
import undetected_chromedriver as uc
import selenium
from selenium.webdriver.common.by import By

# Configure Chrome Options
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/Users/patricklu/Library/Application\\ Support/Google/Chrome/")
options.add_argument("--profile-directory=Profile 4")  # Ensure correct profile

driver = uc.Chrome(options=options)  # Removed use_subprocess=True
driver.get("https://www.pokernow.club/games/pglra_SjWd0YBmBbT7hrovOfb")
print("✅ PokerNow is open!")





time.sleep(5)


def get_player1_hand(driver):
    """Returns the hand of player 1 as a list of card values and suits."""
    hand = []  # List to store card values and suits

    # Find all card containers for player 1
    player1_card_containers = driver.find_elements(By.CSS_SELECTOR, ".table-player-1 .card-container")

    # Iterate through each card container
    for container in player1_card_containers:
        try:
            # Find the card element within the container
            card = container.find_element(By.CSS_SELECTOR, ".card")

            # Find the value element within the card
            value_element = card.find_element(By.CSS_SELECTOR, "span.value")
            card_value = value_element.text

            # Find the suit element within the card and get its inner text
            suit_elements = card.find_elements(By.CSS_SELECTOR, "span.suit")

            # There may be multiple suit spans; we'll get the last one (the main suit)
            card_suit = suit_elements[-1].text  # Get the last span, which represents the card's suit

            # Append the card value and suit to the hand list
            hand.append([card_value, card_suit])

        except Exception as e:
            print("Error extracting card value or suit:", e)
            continue

    return hand

def get_board(driver):
    """Extracts the board cards from the PokerNow table."""
    board = []  # List to store board cards

    # Find all board card containers
    board_card_containers = driver.find_elements(By.CSS_SELECTOR, ".table-cards .card-container")

    for container in board_card_containers:
        try:
            # Find the card element
            card = container.find_element(By.CSS_SELECTOR, ".card")

            # Find the value element
            value_element = card.find_element(By.CSS_SELECTOR, "span.value")
            card_value = value_element.text

            # Find the suit element (last span in case of multiple)
            suit_elements = card.find_elements(By.CSS_SELECTOR, "span.suit")
            card_suit = suit_elements[-1].text  # Get the last suit span

            # Append the card value and suit to the board list
            board.append([card_value, card_suit])

        except Exception as e:
            print("Error extracting board card:", e)
            continue

    return board

try:
    while True:

        hand = get_player1_hand(driver)
        print(hand)


        hand = get_player1_hand(driver)
        board = get_board(driver)

        print("Player 1 Hand:", hand)
        print("Board:", board)

        time.sleep(10)



    # Keep the browser open indefinitely until manually closed
    input("Press Enter to close the browser...")  # Waits for user input before closing







    # Keep the browser open indefinitely until manually closed
    input("Press Enter to close the browser...")  # Waits for user input before closing




except Exception as e:
    print(f"❌ Error: {e}")
