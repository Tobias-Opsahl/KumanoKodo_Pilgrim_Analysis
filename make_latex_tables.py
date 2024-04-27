from new_questions import factor_grouping, new_questions_to_old_questions
from original_scores import original_answer_averages, original_factor_alphas, original_factor_averages
from results import (answer_averages, factor_alphas, factor_averages, female_factor_averages, japanese_factor_averages,
                     male_factor_averages, non_japanese_factor_averages)


def make_factor_table_averages(new_factor_averages, original_factor_averages):
    """
    Make LaTeX table with rows being labeled with the factors (keys in the arguments),
    and two columns, one for the new averages and one for the original ones.
    """
    header = "\\begin{table}[htbp]\n\\centering\n\\scriptsize\n\\begin{tabular}{|l|c|c|}\n\\hline\nFactor & "
    header += "Kumano Kodo Average & Saint Olav's Way Average \\\\\n\\hline\n"
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
    header += " Kumano Kodo Cronbach's Alpha "
    header += "& Saint Olav's Way Cronbach's Alpha \\\\\n\\hline\n"
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
    header += " Kumano Kodo & Saint Olav's Way \\\\\n\\hline\n"
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


def make_subgroup_table(female, male, japanese, non_japanese):
    header = "\\begin{table}[htbp]\n\\centering\n\\scriptsize\n\\begin{tabular}{|l|c|c|c|c|}\n\\hline\n"
    header += "& Females & Males & Japanese & Non-Japanese\\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}\n"
    caption = "\\caption{Comparison of the factor average values from different subgroups, "
    caption += "divided by gender and nationality.} \n"
    label = "\\label{table:subgroups}\n"
    end_table = "\\end{table}"
    rows = ""
    for factor in female.keys():
        row = f"{factor} & {female[factor]:.2f} "
        row += f"& {male.get(factor, 'N/A'):.2f} "
        row += f"& {japanese.get(factor, 'N/A'):.2f} "
        row += f"& {non_japanese.get(factor, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer + caption + label + end_table
    print(table)
    return table


if __name__ == "__main__":
    t1 = make_factor_table_averages(new_factor_averages=factor_averages,
                                    original_factor_averages=original_factor_averages)
    t2 = make_factor_table_alphas(new_factor_alphas=factor_alphas, original_factor_alphas=original_factor_alphas)
    t3 = make_answer_table(new_answer_averages=answer_averages, original_answer_averages=original_answer_averages,
                           new_questions_to_old_questions=new_questions_to_old_questions)
    t4 = make_subgroup_table(female=female_factor_averages, male=male_factor_averages,
                             japanese=japanese_factor_averages, non_japanese=non_japanese_factor_averages)
