# Information Retireval and Text Mining Project

This is a project for the information retrieval and text mining course (KEN4153) at Maastricht University

The data used is retrieved from https://archive.org/stream/AsimovTheFoundation/Asimov_the_foundation_djvu.txt and the PDF version, https://ia801503.us.archive.org/23/items/AsimovTheFoundation/Asimov_the_foundation.pdf

The book is saved in a pickle file and is represented as such, *trilogy = [[{chapter:[paragraphs]},...,{...}],[...],[...]]*, so trilogy[0][chapter_header].values() = list of the paragraphs in each chapter