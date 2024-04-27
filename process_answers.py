import pprint
from pathlib import Path

import pandas as pd
import pingouin as pg

from constants import ANSWERS_FILENAME, DATA_FOLDER, OUTPUT_FILENAME
from new_questions import factor_grouping, new_questions


def read_and_process_answers():
    answers_file = Path(DATA_FOLDER) / ANSWERS_FILENAME
    df = pd.read_excel(answers_file)

    # Remove Japanese from the questions (column names)
    new_columns = []
    for column in df.columns:
        new_column = column.split("|")[0].strip()  # Remove the Japanese translation (after `|`)
        if new_column == "Experience nature&#39;s magic and mysticism":
            new_column = "Experience nature\'s magic and mysticism"
        new_columns.append(new_column)
    df.columns = new_columns
    df = df.fillna("4. Neutral.")

    # Remove numerical description (Trun `4. Neutral` int 4)
    for question in new_questions:
        for i in range(len(df[question])):
            df.loc[i, question] = int(df.loc[i, question].split(".")[0])
        df[question] = df[question].astype(int)

    return df


def calculate_cronbach_alpha(df, questions):
    """
    Calculates Cronenbachs alpha with pandas. Gives the same results as
    pingouin up to som every small fraction. Uses a simplified version of the formula,
    where the variance and covariances has been substituted with total variance and
    individual variances.
    """
    questions_df = df[questions]
    question_variances = questions_df.var(axis=0, ddof=1)
    total_variance = questions_df.sum(axis=1).var(ddof=1)
    n_questions = len(questions)
    return (n_questions / (n_questions - 1)) * (1 - question_variances.sum() / total_variance)


def make_stats(df=None):
    if df is None:
        df = read_and_process_answers()
    answer_averages = {question: df[question].mean() for question in new_questions}
    factor_averages = {}  # factor_name: factor_average (average of each question grouped)
    alphas = {}  # Chronenbachs alphas, internal consistency meassure
    for factor, questions in factor_grouping.items():
        factor_averages[factor] = df[questions].mean(axis=1).mean()  # Mean of all questions in group
        # alphas[factor] = calculate_cronbach_alpha(df, questions)
        alphas[factor] = pg.cronbach_alpha(df[questions])[0]

    stats = {"answer_averages": answer_averages, "factor_averages": factor_averages,
             "factor_alphas": alphas, "n_answers": df.shape[0]}
    return stats


def make_subgroup_stats(df):
    age_idx = 3
    days_idx = 4
    country_idx = 5
    gender_idx = 6
    # Replace kanji with Romaji
    new_country_column = df.iloc[:, country_idx].copy()
    for i in range(len(new_country_column)):
        if "日" in new_country_column[i]:
            new_country_column[i] = "Japan"
    df.iloc[:, country_idx] = new_country_column

    japanese = df.iloc[:, country_idx] == "Japan"
    non_japanese = df.iloc[:, country_idx] != "Japan"
    females = df.iloc[:, gender_idx] == "Female. "
    males = df.iloc[:, gender_idx] == "Male. "

    n_replies = len(df)
    mean_age = df.iloc[:, age_idx].mean()
    n_japanese = len(df[japanese])
    n_non_japanese = n_replies - n_japanese
    n_females = len(df[females])
    n_males = len(df[males])

    total_days = df.iloc[:, days_idx].mean()
    japanese_days = df[japanese].iloc[:, days_idx].mean()
    non_japanese_days = df[non_japanese].iloc[:, days_idx].mean()
    female_days = df[females].iloc[:, days_idx].mean()
    male_days = df[males].iloc[:, days_idx].mean()

    female_stats = make_stats(df=df[females])
    male_stats = make_stats(df=df[males])
    japanese_stats = make_stats(df=df[japanese])
    non_japanese_stats = make_stats(df=df[non_japanese])

    standard_stats = {
        "n_replies": n_replies, "average_age": mean_age, "n_japanese": n_japanese, "n_non_japanese": n_non_japanese,
        "females": n_females, "males": n_males, "average_days": total_days, "average_days_females": female_days,
        "average_days_males": male_days, "average_days_japanese": japanese_days,
        "average_days_non_japanese": non_japanese_days}

    subgroup_stats = {
        "standard_stats": standard_stats,
        "female_factor_averages": female_stats["factor_averages"],
        "male_factor_averages": male_stats["factor_averages"],
        "japanese_factor_averages": japanese_stats["factor_averages"],
        "non_japanese_factor_averages": non_japanese_stats["factor_averages"]
    }
    return subgroup_stats


def write_stats(stats, subgroup_stats=None):
    with open(OUTPUT_FILENAME, "w") as outfile:
        outfile.write(f"n_answers = {pprint.pformat(stats['n_answers'])}\n\n")
        outfile.write(f"factor_averages = {pprint.pformat(stats['factor_averages'])}\n\n")
        outfile.write(f"factor_alphas = {pprint.pformat(stats['factor_alphas'])}\n\n")
        outfile.write(f"answer_averages = {pprint.pformat(stats['answer_averages'])}\n\n")

        if subgroup_stats is not None:
            outfile.write(f"standard_stats = {pprint.pformat(subgroup_stats['standard_stats'])}\n\n")
            outfile.write(f"female_factor_averages = {pprint.pformat(subgroup_stats['female_factor_averages'])}\n\n")
            outfile.write(f"male_factor_averages = {pprint.pformat(subgroup_stats['male_factor_averages'])}\n\n")
            outfile.write("japanese_factor_averages = ")
            outfile.write(f"{pprint.pformat(subgroup_stats['japanese_factor_averages'])}\n\n")
            outfile.write("non_japanese_factor_averages = ")
            outfile.write(f"{pprint.pformat(subgroup_stats['non_japanese_factor_averages'])}\n\n")


if __name__ == "__main__":
    df = read_and_process_answers()
    stats = make_stats(df)
    subgroup_stats = make_subgroup_stats(df)
    write_stats(stats, subgroup_stats)
