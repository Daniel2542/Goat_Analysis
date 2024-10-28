import streamlit as st
import pandas as pd

def goat():
    st.header("Goat(Ronaldo & Messi) Analysis")
    df = pd.read_csv('dataset/data.csv')
    df.head(10)

    df.info()

    st.write("Creating each player dataset")
    ronaldo_df = df[df['Player'] == 'Cristiano Ronaldo']
    st.dataframe(ronaldo_df)

    messi_df = df[df['Player'] == 'Lionel Messi']
    st.dataframe(messi_df)

    st.write("Number of goals for each player")
    len(ronaldo_df)
    len(messi_df)

    st.write(f"Cristiano Ronaldo goals: {len(ronaldo_df)}")
    st.write(f"Lionel Messi goals: {len(messi_df)}")

    st.subheader("Playing position Analysis")
    st.write("Number of goals scored when each player played as a Centre forward")
    playing_position = df[df["Playing_Position"] == "CF"]
    st.dataframe(playing_position)

    chris_goals = playing_position[playing_position["Player"] == "Cristiano Ronaldo"]
    st.dataframe(chris_goals)

    messi_goals = playing_position[playing_position["Player"] == "Lionel Messi"]
    st.dataframe(messi_goals)

    st.write(f"Cristiano Ronaldo goals: {len(chris_goals)}")
    st.write(f"Lionel Messi goals: {len(messi_goals)}")

    st.subheader("Method for scoring goals")
    st.write("Goals scored as tap-ins as an example")
    tap_in = df[df["Type"] == "Tap-in"]
    st.dataframe(tap_in)
    chris_tap = tap_in[tap_in["Player"] == "Cristiano Ronaldo"]
    messi_tap = tap_in[tap_in["Player"] == "Lionel Messi"]

    st.write(f"Cristiano tap ins are: {len(chris_tap)}")
    st.write(f"Lionel Messi tap ins are: {len(messi_tap)}")

    st.subheader("Number of seasons")
    st.write("Number of seasons in the dataset")
    df["Season"]
    df.loc[df["Season"] == "Dec-13", "Season"] = "12/13"
    df.loc[df["Season"] == "11-Dec", "Season"] = "11/12"

    df["Season"].unique()

    st.write("Number of seasons played by each player")
    st.dataframe(df.groupby("Season")["Player"].value_counts())

    st.subheader("Goals per games")
    st.write("Total number of goals per games")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.info()
    ronaldo_games = df.groupby("Player")["Date"].agg(lambda x: len(x.unique())).iloc[0]
    messi_games = df.groupby("Player")["Date"].agg(lambda x: len(x.unique())).iloc[1]

    chris_goals = len(ronaldo_df)
    messi_goals = len(messi_df)

    st.write(f"Cristiano Ronaldo goals: {chris_goals} in {ronaldo_games} games.")
    st.write(f"Lionel Messi goals: {messi_goals} in {messi_games} games.")

    st.subheader("Goals per game ratio")
    ronaldo_goals_per_game = chris_goals / ronaldo_games
    messi_goals_per_game = messi_goals / messi_games

    st.write(f"Cristiano Ronaldo goals per game ratio: {ronaldo_goals_per_game}")
    st.write(f"Lionel Messi goals per game ratio: {messi_goals_per_game}")

    st.subheader("Total competitions participated in")
    df["Competition"].value_counts()

    st.write("Combining two similar leagues together")
    df.loc[df["Competition"] == "Troph�e des Champions", "Competition"] = "Trophée des Champions"
    df.loc[df["Competition"] == "Champions League", "Competition"] = "UEFA Champions League"

    df["Competition"].value_counts()
    st.dataframe(df.groupby("Player")["Competition"].agg(lambda x: len(x.unique())))

    st.subheader("Total goals per competition by player")
    st.dataframe(df.groupby("Player")["Competition"].value_counts())

    st.subheader("Goals per game per competition by player")
    goals_per_competition = df.groupby(["Player", "Competition"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")).reset_index()
    st.dataframe(goals_per_competition)
    # df.groupby(["Player", "Competition"])["Date"].agg(lambda x: len(x.unique()))

    goals_per_competition["goals_per_game"] = goals_per_competition["total_goals"] / goals_per_competition[
        "total_games"]
    st.dataframe(goals_per_competition.head(10))

    st.subheader("Total number of games per season")
    goals_per_season = df.groupby(["Player", "Season"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")).reset_index()
    st.dataframe(goals_per_season)

    st.subheader("Total number of goals per season per competition")
    goals_season_competition = df.groupby(["Player", "Season", "Competition"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")
    ).reset_index()

    goals_season_competition["goals_per_game"] = goals_season_competition["total_goals"] / goals_season_competition[
        "total_games"]

    st.dataframe(goals_season_competition)

    league_goals = df[df["Competition"].isin(["Premier league", "Laliga", "Serie A", "Ligue 1", "Saudi Pro League", "Liga Portugal"])]
    st.dataframe(league_goals.head(10))

    st.write("Converting matchday values to integers")
    league_goals["Matchday"] = league_goals["Matchday"].astype(int)
    league_goals.info()
    st.success("Values successfully converted")

    league_goals.sort_values(by="Matchday", ascending=True)
    goals_per_matchday = league_goals.groupby("Matchday")["Player"].value_counts()
    st.dataframe(goals_per_matchday.head(40))

    st.subheader("Champions league goals per player")
    champions_league = df[df["Competition"].isin(["UEFA Champions League", "UEFA Cahmpions League Qualifying"])]
    st.dataframe(champions_league.head(10))

    champions_league.groupby("Player").size()
    champions_league.groupby(["Player", "Season"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")
    ).reset_index()

    st.subheader("Competition stage goals ")
    st.write("Knockout goals")
    champions_league["Matchday"].value_counts()
    knockout = champions_league[
        champions_league["Matchday"].isin(["last 16", "Quarter-Finals", "Semi-Finals", "Final"])]
    knockout["Matchday"].value_counts()
    knockout.groupby("Player").size()

    st.subheader("Goals per day of week/month/year")

    st.write("Goals per day of week")
    df["Date"].head()
    df["Day_of_week"] = df["Date"].dt.day_name()

    st.dataframe(df.head())

    st.write("Goals per month ")
    df["Month"] = df["Date"].dt.month_name()

    st.dataframe(df.head())

    st.dataframe(df.groupby("Month")["Player"].value_counts())

    st.write("Goals per year")
    df["Year"] = df["Date"].dt.year

    st.dataframe(df.head())
    st.dataframe(df.groupby("Year")["Player"].value_counts())

    st.subheader("Home and Away goals")
    df["Venue"].value_counts()

    home_away = df.groupby(["Player", "Venue"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")
    ).reset_index()

    home_away["goals_per_game"] = home_away["total_goals"] / home_away["total_games"]
    st.dataframe(home_away)

    st.subheader("Home and away goals per season")
    df.groupby(["Player", "Season", "Venue"]).agg(
        total_goals=("Player", "size"),
        total_games=("Date", "nunique")
    ).reset_index()

    st.subheader("Clubs per player")
    st.dataframe(df.groupby("Player")["Club"].value_counts(normalize=True))

    st.subheader("Goals per opponent")
    goals_opponent = df.groupby("Player")["Opponent"].value_counts()
    st.dataframe(goals_opponent.head(10))

    st.dataframe(df.groupby("Player")["Opponent"].agg(lambda x: len(x.unique())))

    st.subheader("Unique positions played")
    df.groupby("Player")["Playing_Position"].value_counts()
    df["Type"].value_counts()
    penalties = df[df["Type"] == "Solo run"]
    st.dataframe(penalties.groupby("Player")["Type"].value_counts())

goat()



























