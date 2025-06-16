import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.formula1.com"

def scrape_actual_top10(year: int, round_num: int):
    """Return the top 10 finishers for a race from formula1.com."""
    races_url = f"{BASE_URL}/en/results.html/{year}/races.html"
    res = requests.get(races_url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.resultsarchive-table tbody tr")
    if round_num < 1 or round_num > len(rows):
        raise ValueError("Invalid round number")
    race_href = rows[round_num - 1].find("a").get("href")
    race_url = BASE_URL + race_href

    res = requests.get(race_url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    result_rows = soup.select("table.resultsarchive-table tbody tr")[:10]
    results = []
    for row in result_rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            driver_name = " ".join(cells[3].get_text(strip=True).split())
            results.append(driver_name)
    if len(results) < 10:
        raise RuntimeError("Could not scrape enough results")
    return results

def get_predictions(player_name: str):
    print(f"Enter predictions for {player_name} (Top 10):")
    predictions = []
    for i in range(1, 11):
        driver = input(f"Position {i}: ").strip()
        predictions.append(driver)
    return predictions

def score_predictions(predictions, actual):
    score = 0
    lower_actual = [d.lower() for d in actual]
    for idx, driver in enumerate(predictions):
        d_lower = driver.lower()
        if d_lower == lower_actual[idx]:
            score += 5
        elif d_lower in lower_actual:
            score += 1
    return score

def main():
    print("F1 Top 10 Prediction Game")
    year = int(input("Year: "))
    round_num = int(input("Round number: "))
    try:
        actual_top10 = scrape_actual_top10(year, round_num)
    except Exception as exc:
        print(f"Failed to fetch results: {exc}")
        return

    p1_preds = get_predictions("Player 1")
    p2_preds = get_predictions("Player 2")

    players = [("Player 1", p1_preds), ("Player 2", p2_preds)]
    results = []
    for name, preds in players:
        score = score_predictions(preds, actual_top10)
        result = {"Player": name, "Score": score}
        for i, d in enumerate(preds):
            result[f"P{i+1}"] = d
        results.append(result)

    fieldnames = ["Player"] + [f"P{i+1}" for i in range(10)] + ["Score"]
    with open("game_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print("Results saved to game_results.csv")

if __name__ == "__main__":
    main()
