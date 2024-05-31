from utils.helper import Helper
from utils.analyse import Analyse
import matplotlib.pyplot as plt

helper = Helper()

entities = helper.load_data('data/entities.pkl')

analyse = Analyse(entities)

def plot_entity_counts_per_chapter():
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
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'results/entity_counts_per_chapter_for_book{i+1}.png')