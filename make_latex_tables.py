from results import factor_averages, factor_alphas, answer_averages
from original_scores import original_answer_averages, original_factor_alphas, original_factor_averages


def make_factor_table_averages(new_factor_averages, original_factor_averages):
    """
    Make LaTeX table with rows being labeled with the factors (keys in the arguments),
    and two columns, one for the new averages and one for the original ones.
    """
    header = "\\begin{tabular}{lcc}\n\\hline\nFactor & New Average & Original Average \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}"
    rows = ""
    for factor in new_factor_averages.keys():
        row = f"{factor} & {new_factor_averages[factor]:.2f} "
        row += f"& {original_factor_averages.get(factor, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer
    print(table)


def make_factor_table_alphas(new_factor_alphas, original_factor_alphas):
    """
    Make LaTeX table with rows being labeled with the factors (keys in the arguments),
    and two columns, one for the new Cronbach's alphas values and one for the original ones.
    """
    header = "\\begin{tabular}{lcc}\n\\hline\nFactor & New Cronbach's Alpha "
    header += "& Original Cronbach's Alpha \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}"
    rows = ""
    for factor in new_factor_alphas.keys():
        row = f"{factor} & {new_factor_alphas[factor]:.2f} & {original_factor_alphas.get(factor, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer
    print(table)


def make_answer_table(new_answer_averages, original_answer_averages):
    """
    Make LaTeX table with rows being the questions (key in the argument dicts) and two columns,
    one with the new question averages and one with the original ones.
    """
    header = "\\begin{tabular}{lcc}\n\\hline\nQuestion & New Average & Original Average \\\\\n\\hline\n"
    footer = "\\hline\n\\end{tabular}"
    rows = ""
    for question in new_answer_averages.keys():
        row = f"{question} & {new_answer_averages[question]:.2f} & "
        row += f"{original_answer_averages.get(question, 'N/A'):.2f} \\\\\n"
        rows += row
    table = header + rows + footer
    print(table)


if __name__ == "__main__":
    make_factor_table_averages(factor_averages=factor_averages, original_factor_averages=original_factor_averages)
    make_factor_table_alphas(factor_alphas=factor_alphas, original_factor_alphas=original_factor_alphas)
    make_answer_table(answer_averages=answer_averages, original_answer_averages=original_answer_averages)
