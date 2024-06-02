from utils.helper import Helper
from utils.analyse import Analyse
from utils.asimov import Asimov
import matplotlib.pyplot as plt

helper = Helper()
asimov = Asimov()
analyse = Analyse()

def plot_entity_counts():
    entity_counts = analyse.count_entities_per_chapter()
    for i, book in enumerate(entity_counts):
        x = book.keys()
        y = book.values()
        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.bar(x, y)
        plt.xlabel("Chapter")
        plt.ylabel("Entity Count")
        plt.title(f"Named Entities Count in Book {i+1} by Chapter")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(f'results/entity_counts_per_chapter_for_book{i+1}.png')

def plot_character_importance():
    analyse.count_character_instances()

def plot_word_counts():
    word_counts = analyse.count_words()
    n = 50
    x = [token for token, _ in word_counts.most_common(n)]
    y = [count for _, count in word_counts.most_common(n)]

    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.xticks(rotation=90)
    plt.title('Most Common Words in The Foundation Trilogy')
    plt.savefig(f'results/{n}_most_common_words.png')

def get_results():
    plot_word_counts()
    # plot_character_importance()
    plot_entity_counts()

if __name__ == '__main__':
    get_results()