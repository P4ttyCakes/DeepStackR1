from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

suited_cards = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}

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

def position(driver):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".dealer-button-ctn.dealer-position-1 .button")
        if elements:
            return "Dealer"
        else:
            return "Not Dealer"
    except Exception as e:
        return "Not Yet: " + str(e)



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


def format_cards(cards):
    suited_cards = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}
    formatted_cards = []

    for card_value, card_suit in cards:
        suit_symbol = suited_cards.get(card_suit, card_suit)
        formatted_cards.append(f"{card_value}{suit_symbol}")

    return " | ".join(formatted_cards)



def get_stack(driver):

    try:

        stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-1 .table-player-stack .bb-value")[0].text
        num = stack.split("B")[0]
    except Exception as e:
        num = 0
    return num


def opponent_stack(driver):
    try:
        stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-2 .table-player-stack .bb-value")[0].text
        num = stack.split("B")[0]
    except Exception as e:
        try:
            stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-10 .table-player-stack .bb-value")[0].text
            num = stack.split("B")[0]
        except Exception as e:
            num = 0
    return num




def opponent_bet(driver):
    try:
        stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-2 .table-player-bet-value .bb-value")[0].text
        num = stack.split("B")[0]
    except Exception as e:
        try:
            stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-10 .table-player-bet-value .bb-value")[0].text
            num = stack.split("B")[0]
        except Exception as e:

            num = 0
    return num

def your_bet(driver):
    try:
        stack = driver.find_elements(By.CSS_SELECTOR, ".table-player-1 .table-player-bet-value .bb-value")[0].text
        num = stack.split("B")[0]
    except Exception as e:
        num = 0
    return num



def your_turn(driver):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".table-player-1.decision-current")
        if elements:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking if it's your turn:", e)
        return False

def get_pot_size(driver):
    try:
        pot_size = driver.find_elements(By.CSS_SELECTOR, ".table-pot-size .main-value .chips-value.presenting-bb .bb-value")[0].text

        num = pot_size.split("B")[0]
    except Exception as e:
        num = 0
    return num


def click_Fold(driver):
    try:
        foldButton = driver.find_element(By.CSS_SELECTOR, "button.button-1.action-button.with-tip.fold.red")
        foldButton.click()

        #UNCESSARY FOLD
        try:
            if driver.find_element(By.CSS_SELECTOR, ".alert-1-buttons"):
                driver.find_element(By.CSS_SELECTOR, "button.button-1.red").click()
                print("Unnecessary fold, Checking Instead")
                click_Check(driver)
        except Exception as e:
            pass


    except Exception as e:
        print("Error clicking fold button:", e)



def click_Check(driver):
    try:
        checkButton = driver.find_element(By.CSS_SELECTOR, "button.button-1.action-button.with-tip.check.green")
        checkButton.click()
    except Exception as e:
        print("Error clicking check button:", e)

def click_Call(driver):
    try:
        callButton = driver.find_element(By.CSS_SELECTOR, "button.button-1.action-button.with-tip.call.green")
        callButton.click()
    except Exception as e:
        print("You cannot call in this position, Checking Instead")
        click_Check(driver)


def perform_ai_action(driver, decision, betsize):
    if decision == "RAISE":

        try:
            raiseButton = driver.find_element(By.CSS_SELECTOR, "button.button-1.action-button.with-tip.raise.green")

            raiseButton.click()

            input_field = driver.find_element(By.CSS_SELECTOR, "div.value-input-ctn input.value")
            input_field.clear()
            input_field.send_keys(str(betsize) + '0')
            time.sleep(2)
            input_field.send_keys(Keys.RETURN)

        except Exception as e:
            print("Error performing raise action:", e)

    elif decision == "FOLD":
        click_Fold(driver)
    elif decision == "CALL":
        click_Call(driver)
    elif decision == "CHECK":
        click_Check(driver)


