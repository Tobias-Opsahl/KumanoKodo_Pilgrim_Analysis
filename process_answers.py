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


def write_stats(stats):
    with open(OUTPUT_FILENAME, "w") as outfile:
        outfile.write(f"n_answers = {pprint.pformat(stats['n_answers'])}\n\n")
        outfile.write(f"factor_averages = {pprint.pformat(stats['factor_averages'])}\n\n")
        outfile.write(f"factor_alphas = {pprint.pformat(stats['factor_alphas'])}\n\n")
        outfile.write(f"answer_averages = {pprint.pformat(stats['answer_averages'])}\n\n")


if __name__ == "__main__":
    df = read_and_process_answers()
    stats = make_stats(df)
    write_stats(stats)
    from IPython import embed
    embed()
