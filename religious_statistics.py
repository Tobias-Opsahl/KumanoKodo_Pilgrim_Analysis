import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


religious_beliefs = {
    1946: 59.6,  # Ishii
    1947: 71,  # Ishii
    1949: 60,  # Ishii
    1952: 64.7,  # Inoue
    1965: 56,  # Ishii
    1969: 36,  # Ishii ...
    1979: 33.6,
    1984: 29.1,
    1989: 28,
    1994: 26.1,
    1995: 20.3,
    2005: 22.9,
}

important = {
    1979: 46.2,  # Inoue
    1984: 43.8,  # Inoue
    1989: 38.0,  # Inoue
    1994: 34,  # Inoue ...
    1995: 25.6,
    1998: 27,
}


def plot_religious_beliefs():
    years_beliefs, beliefs_values = zip(*sorted(religious_beliefs.items()))
    plt.figure(figsize=(10, 6))
    plt.plot(years_beliefs, beliefs_values, marker="o", linestyle="-", color="b", label="Belief in Religion")

    plt.xlabel("Year", fontsize=18)
    plt.ylabel("Percentage", fontsize=18)
    # plt.title("Percentage of People Believing in Religion in Japan over Time")
    # plt.legend()
    plt.tight_layout()
    plt.savefig("plots/religious_belief_stats.pdf")
    # plt.show()


def plot_religious_importance():
    years_important, important_values = zip(*sorted(important.items()))
    plt.figure(figsize=(10, 6))
    plt.plot(years_important, important_values, marker="s", linestyle="-", color="r", label="Religion is Important")

    # Ensure x-axis has only integer years, without decimals
    ax = plt.gca()  # Get current axis
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Only integer labels
    plt.xlabel("Year", fontsize=18)
    plt.ylabel("Percentage", fontsize=18)
    # plt.title("Percentage of People Considering Religion Important in Japan over Time")
    # plt.legend()
    plt.tight_layout()
    plt.savefig("plots/religious_importance.pdf")
    # plt.show()


if __name__ == "__main__":
    plot_religious_beliefs()
    plot_religious_importance()
