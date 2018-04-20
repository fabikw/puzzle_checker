# Puzzle Answer Checker

This small webapp is used to check answers (of puzzles or whatever) for correctness in the absence of an online checker, without having to look at the correct answer. It needs an `answers.csv` file separated with `|` with the puzzle name (or identifier) as first element and answer as second element (ALLCAPSANDNOSPACES).

The `answers.csv` must be compiled by a person that doesn't care about seeing the answers.

The program supports persistent state in case the server goes down. Puzzles correctly solved (and a timestamp) are collected in a `correct.txt` file that is read at the beginning. The names of the puzzles in that file must match those in the `answers.csv` when restoring or they won't be recognized as solved (but the app will run properly).
