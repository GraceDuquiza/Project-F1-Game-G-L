# Project-F1-Game-G-L

This repository contains a command line Formula 1 prediction game for two
players. Actual race results are scraped from **formula1.com** so you can play
after each Grand Prix.

Each player guesses the Top 10 finishers of the season. Points are awarded
as follows:

* **5 points** - the driver is predicted in the correct grid position
* **1 point** - the driver appears in the Top 10 but not in the predicted position

At the end of the game the results are written to `game_results.csv`.

## Running the game

Ensure you have Python 3 installed. Install the dependencies with:

```bash
pip install requests beautifulsoup4
```

Then from the project directory run:

```bash
python3 f1_game.py
```
Follow the prompts to enter the race **year** and **round number**. The script
will fetch the official results for that event. After both players enter their
predictions the program calculates scores and writes them to
`game_results.csv`.

