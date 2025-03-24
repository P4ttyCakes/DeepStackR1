# DeepStackR1: AI-Powered Poker Assistant

## Project Overview

DeepStackR1 is an advanced Python-based poker assistant that leverages artificial intelligence to make strategic decisions in real-time online poker games. The project combines web automation, AI decision-making, and poker strategy to create an intelligent Poker Bot.

## Features

- **Deepseek-Powered Decision Making**: Utilizes DeepSeek-Chat LLM for strategic poker decisions
- **Web Automation**: Utilizes Selenium for web scraping and interaction with PokerNow Website.
- **Adaptive Strategy**: Implements complex poker strategies based on game context, feeding context to AI model.

##  Technology Stack

- **Language**: Python 3.9+
- **Web Automation**: Selenium, Undetected ChromeDriver
- **AI Integration**: DeepSeek API
- **Key Libraries**: 
  - `openai`
  - `python-dotenv`
  - `selenium`

## Installation

### Prerequisites

- Python 3.9
- Google Chrome
- DeepSeek API Key

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DeepStackR1.git
cd DeepStackR1
```

2. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
# Create .env file
echo "DSK=your_deepseek_api_key" > .env
echo "DEEPSEEK_BASE_URL=https://api.deepseek.com" >> .env
```

## Usage

Run the main script:
```bash
python main.py
```

##  Project Structure

- `main.py`: Primary game control script
- `Methods.py`: Web interaction utilities
- `DeepSeekAPiCalls.py`: AI decision-making logic
- `.env`: Configuration and API credentials


## License

Distributed under the MIT License. See `LICENSE` for more information.
