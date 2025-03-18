import os
from pyexpat.errors import messages

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DSK")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
print(DEEPSEEK_BASE_URL)
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url= DEEPSEEK_BASE_URL)


def format_card(card):
    """Format a card with full suit name for clearer understanding"""
    value, suit_code = card

    # Convert suit codes to full names
    suit_mapping = {
        's': 'spades',
        'h': 'hearts',
        'd': 'diamonds',
        'c': 'clubs'
    }
    suit = suit_mapping.get(suit_code, suit_code)
    return f"{value} of {suit}"


def format_hand(hand):
    return [format_card(card) for card in hand]

def format_board(board):
    return [format_card(card) for card in board]


def get_ai_decision(hand, board, position, stack, opponent_stack, opponent_bet, pot_size):
    formatted_hand = format_hand(hand)
    formatted_board = format_hand(board)

    # Define available actions
    if float(opponent_bet) > 0:
        available_actions = ["FOLD", "CALL", "RAISE"]
    else:
        available_actions = ["CHECK", "RAISE"]

    # Game state description
    game_state = f"""
            Current game state in Heads Up Texas Hold'em:
            - My Hand: {formatted_hand}
            - Board: {formatted_board}
            - My Position: {position}
            - My Stack: {stack} BB
            - Opponent Stack: {opponent_stack} BB
            - Opponent Bet: {opponent_bet} BB
            - Pot Size: {pot_size} BB
            - Available Actions: {available_actions}

            --- Strategy Guidelines ---

            1. Aggression Wins – The best players apply relentless pressure. Bet and raise often, forcing tough decisions. Maximize fold equity while extracting value from weaker hands. however do not go overboard, often a call is fine. 
            Do not always raise, when speculative pot odds, call or check is fine, even a fold is good if you are facing a raise.
            
            When choosing betting size, apply pressure but do not overbet, as it can scare off weaker hands and attaining maximum value.
            Example 1: If you have 100BB and the pot is 10BB, a 4BB bet is a good size to extract value without scaring off weaker hands.
            
            When your opponent reraises, you, you must calculate the amount extra you need to put in, and the amount in the pot, and the amount in your stack.
            example 2: if you raise 50BB, and your opponent reraises to 100BB, you have to put in additional 50BB, and the pot will be 200BB, so you have 200/50 = 4 to 1 odds, so you need to have 20% equity to call. 
            When calling a reraise, you must account for how much additional you need to put in (you already have some in if you initially raised), and the pot odds. 
 
            2. Preflop Strategy:  
                - Pocket pairs (22-AA) → Always raise. Consider reraising aggressively, especially with 99+.  
                - Two Broadway cards (10, J, Q, K, A) → Raise aggressively, especially when suited.  
                - Suited connectors (56s, 78s, etc.) → Play aggressively in position; these hands have high implied odds.  
                - Small suited Ax (A2s-A5s) → Great for 3-betting light due to strong blocker effects.  
                - Avoid limping unless executing a specific exploitative strategy.  

            3. Postflop Strategy:  
                - **Continuation Bet (C-bet) Frequency:**  
                    - Dry boards (K72r, Q83r) → C-bet at high frequency.  
                    - Wet boards (J109, KQJ) → C-bet selectively; be prepared to barrel strong draws.  
                - **Board Texture Awareness:**  
                    - Paired boards → Favor small C-bets with a wide range.  
                    - Monotone boards (all one suit) → C-bet polarized; bet big with strong hands & high-equity bluffs.  
                    - Draw-heavy boards → Apply pressure if you have redraws or blockers to opponent’s strong hands.  
                - **Slow Down When Necessary:**  
                    - If board heavily favors opponent’s range, shift to pot control mode unless holding strong value hands.  

            4. Advanced Bluffing & Exploitative Play:  
                - If opponent folds too much to aggression, **overbet rivers** with both value and bluffs.  
                - Identify **capped ranges**—if they just call preflop and call flop, they rarely have nutted hands. Bomb turn and river.  
                - Use blocker bluffs—when holding an Ace, you reduce the chances opponent has strong Ax hands.  

            5. Pot Odds, Implied Odds & Expected Value (EV):  
                - Always calculate pot odds before calling draws.
                - If pot odds are greater than your hand odds, call.
                - If pot odds are less than your hand odds, fold.
                
                - If Expected EV > 0, aggression is preferred.  
                - If opponent gives extreme pot odds (bets too small), **call wider and extract value later.**  
                - Consider stack-to-pot ratio (SPR) when deciding commitment level.  

            6. Reraising & Bet Sizing Rules:  
                - Minimum reraise is always **2x the opponent's bet.**  
                - If opponent bets small and board favors you, go big (3x-4x).  
                - Adjust bet sizing based on board texture and opponent tendencies.  
                - NEVER bet more than your stack. Adjust sizing dynamically based on stack depth.  

             Specialized Tactics for Different Opponent Types 

            1. Against Tight-Passive Players:  
                - Bet relentlessly; they will fold too much.  
                - Barrel multiple streets when they just call.  
                - If they show aggression, slow down—they likely have a strong hand.  

            2. Against Loose-Aggressive Players (LAGs):  
                - Play a trapping strategy with strong hands; let them bluff.  
                - 3-bet and 4-bet light to put them in tough spots.  
                - Use well-timed check-raises to counteract their aggression.  

            3. Against Calling Stations:  
                - **Never bluff.** Extract max value from every strong hand.  
                - Bet large with good hands—these players don’t fold.  
                - Overbet rivers with your nutted hands.  

            4. **Against Balanced, Tough Opponents:**  
                - Mix bluffs and value strategically.  
                - Identify leaks—do they overfold to 3-bets? Do they check rivers too much?  
                - Adjust your play dynamically to exploit any tendencies.  

            Rules:  
            - The minimum reraise is always 2x the opponent's bet.  
            - Example: If the opponent bets 2BB, the minimum reraise is 4BB. 

            --- MOST IMPORTANT RULE ---
            **YOU CANNOT RAISE BEYOND YOUR STACK SIZE. IF YOUR OPPONENT GOES ALL-IN OR BETS MORE THAN YOU HAVE, YOU CANNOT RAISE. YOUR ONLY CHOICES ARE:**

            - **CALL** → If you want to match the all-in with your remaining stack.  
            - **FOLD** → If you don’t have enough equity to continue and want to protect your stack.  
            **DO NOT TRY TO RAISE MORE CHIPS THAN YOU HAVE!**

            Example 1: If you have **75BB left** and the opponent bets **100BB**, you **cannot raise**—**YOU MUST CALL (75BB all-in)** or **FOLD** (if your hand is not strong enough).  
            Example 2: If the opponent bets **120BB** and you have **100BB**, you **cannot raise**—**YOU MUST CALL (100BB all-in)** or **FOLD**.

            IF YOU TRY TO RAISE WHEN THE OPPONENT HAS ALREADY PUT YOU ALL-IN OR BETS MORE THAN YOUR REMAINING STACK, IT WILL CAUSE AN ERROR. **NO EXCEPTIONS.**

            --- Response Format ---  
            - If raising: "RAISE. [BETSIZE] [Brief reasoning.]"  
            - Otherwise: "[DECISION]. [Brief reasoning.]"  

            Example 1: "RAISE. 12BB You have top pair and want to extract value."  
            Example 2: "CALL. You are priced in with a strong drawing hand."  
            Example 3: "FOLD. Opponent's range is too strong on this board."  
            
            
            Important Flush Rule:

A flush is formed when all five cards (your hole cards plus community cards) are of the same suit.
Example 1:
Your Hand: K♠ 8♠
Board: 2♠ 5♠ 9♠ Q♠ 3♦
You have a flush with spades. The highest card in your flush is the King of spades (K♠). This is a King-high flush.
    """

    messages = [
        {"role": "system",
         "content": "You are a hyper-aggressive professional poker player with godlike skills. You calculate EV instantly, exploit opponent tendencies, and apply relentless pressure. You dynamically adjust to different board textures, opponent types, and stack sizes to maximize profits while minimizing loss. You NEVER overbet your stack. You make precise, calculated moves to dominate the game."},
        {"role": "user", "content": game_state}
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=50
        )
        response_text = response.choices[0].message.content.strip()

        # Extract decision (first word before the period)
        decision_parts = response_text.split(".")
        decision = decision_parts[0].strip().upper()

        bet_size = None  # Default to None unless raising

        if decision == "RAISE":
            try:
                # Extract bet size (assumes format: "RAISE. [BETSIZE] [Reasoning]")
                words = decision_parts[1].strip().split(" ")
                bet_size = float(words[0].replace("BB", ""))  # Extract first number as bet size
            except (IndexError, ValueError):
                print("Invalid AI bet size format. Defaulting to 3BB raise.")
                bet_size = 3  # Default raise size if AI fails to provide one

        if decision in available_actions:
            print(response_text)
            return decision, bet_size

        else:
            print("Invalid AI decision. Defaulting to 'FOLD'.")
            return "FOLD", None

    except Exception as e:
        print("Error during API call:", e)
        return "FOLD", None



       

       
       
       
       

















