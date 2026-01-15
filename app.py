from flask import Flask, render_template, json
import pandas as pd
import os

app = Flask(__name__)

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths to the CSV result files used in the application
WINNER_CSV     = os.path.join(BASE_DIR, "static/data/results/ucl_winner_top20.csv")
TOP_SCORER_CSV = os.path.join(BASE_DIR, "static/data/results/ucl_top_scorer_top10.csv")
TOP_ASSIST_CSV = os.path.join(BASE_DIR, "static/data/results/ucl_top_assist_top10.csv")
MVP_CSV        = os.path.join(BASE_DIR, "static/data/results/ucl_mvp_top10.csv")

def load_win_probabilities(top_n=20):
    df = pd.read_csv(WINNER_CSV)
    print("Columns in CSV:", df.columns)
    df["Win_Probability"] = pd.to_numeric(df["Win_Probability"])
    df["Win_Probability_pct"] = df["Win_Probability"] * 100
    df = df.sort_values("Win_Probability_pct", ascending=False).head(top_n)

    data = []
    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        data.append({
            "team": row["Team"],
            "prob": round(row["Win_Probability_pct"], 1),
            "rank": rank,
            "logo": row["LogoFile"],
        })
    return data

def get_top_favorite():
    data = load_win_probabilities(top_n=1)
    return data[0]

def load_winner_data(top_n=20):
    df = pd.read_csv(WINNER_CSV)
    df["Win_Probability"] = pd.to_numeric(df["Win_Probability"])
    df["Win_Probability_pct"] = df["Win_Probability"] * 100
    df = df.sort_values("Win_Probability_pct", ascending=False).head(top_n)
    data = []
    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        data.append({
            "team": row["Team"],
            "prob": round(row["Win_Probability_pct"], 1),
            "rank": rank,
            "logo": row.get("LogoFile", None), # Use .get() to avoid errors if the logo column is missing
        })
    return data

def load_top_scorer_data(top_n=10):
    df = pd.read_csv(TOP_SCORER_CSV)

    df["TopScorer_Prob"] = pd.to_numeric(df["TopScorer_Prob"])
    df["TopScorer_Prob_pct"] = df["TopScorer_Prob"] * 100

    df = df.sort_values("TopScorer_Prob_pct", ascending=False).head(top_n)

    data = []
    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        data.append({
            "player": row["Player"],
            "team": row["Team"],
            "prob": round(row["TopScorer_Prob_pct"], 1),
            "goals": float(row["lambda_final_goals"]),
            "rank": rank,
            "logo": row.get("LogoFile", None),
        })
    return data

def load_top_assist_data(top_n=10):
    df = pd.read_csv(TOP_ASSIST_CSV)

    df["TopAssist_Prob"] = pd.to_numeric(df["TopAssist_Prob"])
    df["TopAssist_Prob_pct"] = df["TopAssist_Prob"] * 100

    df = df.sort_values("TopAssist_Prob_pct", ascending=False).head(top_n)

    data = []
    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        data.append({
    "player": row["Player"],
    "team": row["Team"],
    "prob": round(row["TopAssist_Prob_pct"], 1),
    "assists": float(row["lambda_final_assists"]),
    "rank": rank,
    "logo": row.get("LogoFile", None),
})
    return data

def load_mvp_data(top_n=10):
    df = pd.read_csv(MVP_CSV)

    df["MVP_score"] = pd.to_numeric(df["MVP_score"])

    df = df.sort_values("MVP_score", ascending=False).head(top_n)

    data = []
    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        data.append({
            "player": row["Player"],
            "team": row["Team"],
            "score": round(row["MVP_score"], 3),
            "rank": rank,
            "logo": row.get("LogoFile", None),
        })
    return data

@app.route("/")
def index():
    # Home page: displays the main favorite and the top winning probabilities
    favorite = get_top_favorite()
    win_data = load_win_probabilities(top_n=20)
    return render_template("index.html", favorite=favorite, win_data=win_data)

@app.route("/method")
def method():
    return render_template("method.html")

@app.route("/results")
def results():
    # aggregates all computed rankings (teams, scorers, assists, MVP)
    winner_data     = load_winner_data(top_n=20)
    top_scorer_data = load_top_scorer_data(top_n=10)
    top_assist_data = load_top_assist_data(top_n=10)
    mvp_data        = load_mvp_data(top_n=10)

    return render_template(
        "results.html",
        winner_data=winner_data,
        top_scorer_data=top_scorer_data,
        top_assist_data=top_assist_data,
        mvp_data=mvp_data,
    )

@app.route("/files")
def files():
    return render_template("files.html")

if __name__ == "__main__":
    app.run(debug=True)
