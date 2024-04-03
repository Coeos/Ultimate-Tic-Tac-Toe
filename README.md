# Ultimate Tic Tac Toe AI

## Overview

This Python script implements an artificial intelligence (AI) to play the Ultimate Tic Tac Toe game. Ultimate Tic Tac Toe is an advanced version of the classic Tic Tac Toe, where each square of the 3x3 game board contains another smaller 3x3 board. Winning the smaller boards is crucial to win squares of the larger board.

The AI utilizes a minimax algorithm with alpha-beta pruning for decision-making, evaluating moves based on the current game state to play optimally against a human player or another AI.

## Features

- **Minimax Algorithm with Alpha-Beta Pruning**: The core of the AI's decision-making, allowing it to predict and evaluate future moves efficiently.
- **Dynamic Game State Evaluation**: Evaluates the board to prioritize winning moves, block opponent wins, and select strategically advantageous positions.
- **Customizable Depth**: Allows setting the depth of the minimax algorithm to control the difficulty and foresight of the AI.
- **Flexible Game Flow**: Supports games where the AI plays against a human or itself, with easy input methods for human players.

## Requirements

- Python 3.11
- NumPy library

## Setup

1. Ensure you have Python 3.x installed on your system. If not, download and install it from the official Python website.
2. Install NumPy if you haven't already, by running `pip install numpy` in your terminal or command prompt.
3. Download the Ultimate Tic Tac Toe script to your local machine.

## How to Play

1. Open your terminal or command prompt.
2. Navigate to the directory where you saved the script.
3. Run the script using Python by typing `python Ultimate_Tic_Tac_Toe.py`.
4. Follow the on-screen prompts to play against the AI. You will be asked to input your moves in a `x, y, i, j` format, where `x, y` specify the sub-grid and `i, j` specify the cell within that sub-grid.

## Customizing AI Difficulty

You can adjust the difficulty of the AI by changing the `depth` parameter in the `main()` function. A higher depth value makes the AI more challenging, as it will consider more possible move outcomes before making a decision. However, increasing the depth also requires more processing time.
