from new_questions import new_questions_to_old_questions, factor_grouping
from original_scores import original_answer_averages, original_factor_alphas, original_factor_averages
from results import answer_averages, factor_alphas, factor_averages


def make_factor_table_averages(new_factor_averages, original_factor_averages):
    """
    Make LaTeX table with rows being labeled with the factors (keys in the arguments),
    and two columns, one for the new averages and one for the original ones.
    """
    header = "\\begin{table}[htbp]\n\\centering\n\\scriptsize\n\\begin{tabular}{|l|c|c|}\n\\hline\nFactor & "
    header += "New Average & Original Average \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}\n"
    caption = "\\caption{Comparison of the mean values of the factors for the new (Kumano Kodo) "
    caption += " answers and the original (Saint Olav's Way) answers. The factor grouping found by "
    caption += " the analysis on the Saint Olav's Way \\parencite{vistad2020long} was used for both values. }\n"
    label = "\\label{table:factor_averages}\n"
    end_table = "\\end{table}"
    rows = ""
    for factor in new_factor_averages.keys():
        row = f"{factor} & {new_factor_averages[factor]:.2f} "
        row += f"& {original_factor_averages.get(factor, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer + caption + label + end_table
    print(table)
    return table


def make_factor_table_alphas(new_factor_alphas, original_factor_alphas):
    """
    Make LaTeX table with rows being labeled with the factors (keys in the arguments),
    and two columns, one for the new Cronbach's alphas values and one for the original ones.
    """
    header = "\\begin{table}[htbp]\n\\centering\n\\scriptsize\n\\begin{tabular}{|l|c|c|}\n\\hline\nFactor & "
    header += "New Cronbach's Alpha "
    header += "& Original Cronbach's Alpha \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}\n"
    caption = "\\caption{Comparison of Chronenbachs alpha (internal consistency) for the new (Kumano Kodo) "
    caption += " answers and the original (Saint Olav's Way) answers. The factor grouping found by "
    caption += " the analysis on the Saint Olav's Way \\parencite{vistad2020long} was used for both values. }\n"
    label = "\\label{table:factor_alphas}\n"
    end_table = "\\end{table}"
    rows = ""
    for factor in new_factor_alphas.keys():
        row = f"{factor} & {new_factor_alphas[factor]:.2f} & {original_factor_alphas.get(factor, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer + caption + label + end_table
    print(table)
    return table


def make_answer_table(new_answer_averages, original_answer_averages, new_questions_to_old_questions):
    """
    Make LaTeX table with rows being the questions (key in the argument dicts) and two columns,
    one with the new question averages and one with the original ones, sorted by decreasing new average.
    Add a caption to the table.
    """
    header = "\\begin{table}[htbp]\n\\centering\n\\scriptsize\n\\begin{tabular}{|l|c|c|}\n\\hline\nQuestion & "
    header += "New Average & Original Average \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}\n"

    caption = "\\caption{Comparison of individual answer means for the new (Kumano Kodo) answers and the "
    caption += "original (Saint Olav's Way) answers.}\n"
    label = "\\label{tab:answer_table}\n"
    end_table = "\\end{table}"

    rows = ""

    # Sorting the new_answer_averages by decreasing value
    sorted_new_answers = sorted(new_answer_averages.items(), key=lambda x: x[1], reverse=True)

    for question, avg in sorted_new_answers:
        old_question = new_questions_to_old_questions[question]
        original_avg = original_answer_averages.get(old_question, "N/A")
        row = f"{question} & {avg:.2f} & {original_avg:.2f} \\\\\n"
        rows += row

    table = header + rows + footer + caption + label + end_table
    print(table)
    return table


def make_comprehensive_factor_table():
    header = "\\begin{longtable}{|p{0.15\\textwidth}|p{0.55\\textwidth}|c|c|}\n"
    header += "\\hline\nFactor Grouping & Question & New Mean & Original Mean \\\\\n\\hline\n"
    header += "\\endfirsthead\n"
    header += "\\multicolumn{4}{c}{{\\bfseries Table \\thetable{} -- continued from previous page}} \\\\\n"
    header += "\\hline\nFactor Grouping & Question & New Mean & Original Mean \\\\\n\\hline\n"
    header += "\\endhead\n"
    header += "\\hline \\multicolumn{4}{|r|}{{Continued on next page}} \\\\ "
    header += "\\hline\n\\endfoot\n\\hline\n\\endlastfoot\n"

    # Factor Groupings
    rows = ""
    for factor_group, questions in factor_grouping.items():
        factor_name = factor_group.split(" ", 1)[1]  # Splitting to get rid of the numbering
        factor_score = factor_averages.get(factor_group, "N/A")
        # factor_alpha = factor_alphas.get(factor_group, "N/A")
        # original_factor_score = original_factor_averages.get(factor_group, "N/A")
        # original_factor_alpha = original_factor_alphas.get(factor_group, "N/A")

        # Adding factor information row
        rows += f"\\multicolumn{{4}}{{|l|}}{{\\textbf{{Factor: {factor_name} - New Avg: {factor_score:.2f}, "
        rows += "Alpha: {factor_alpha:.2f} - Original Avg: {original_factor_score:.2f}, "
        rows += "Alpha: {original_factor_alpha:.2f}}}}} \\\\\n\\hline\n"

        # Adding questions for this factor
        for question in questions:
            old_question = new_questions_to_old_questions.get(question, question)  # Fallback to question if not found
            new_mean = answer_averages.get(question, "N/A")
            original_mean = original_answer_averages.get(old_question, "N/A")
            rows += f"& {question} & {new_mean:.2f} & {original_mean:.2f} \\\\\n"
        rows += "\\hline\n"

    footer = "\\end{longtable}"
    caption = "\\caption{Comprehensive Comparison of Factors, Cronbach's Alpha, and Questionnaire Responses.}\n"
    label = "\\label{tab:comprehensive_factor_comparison}\n"

    # Combine all parts
    table = header + rows + footer + caption + label

    print(table)
    return table


if __name__ == "__main__":
    t1 = make_factor_table_averages(new_factor_averages=factor_averages,
                                    original_factor_averages=original_factor_averages)
    t2 = make_factor_table_alphas(new_factor_alphas=factor_alphas, original_factor_alphas=original_factor_alphas)
    t3 = make_answer_table(new_answer_averages=answer_averages, original_answer_averages=original_answer_averages,
                           new_questions_to_old_questions=new_questions_to_old_questions)
    from IPython import embed
    embed()
