# Created by Dark Angel on 3 January 2025

import streamlit as st
import numpy as np
import random

# Sudoku Generator
def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    board = np.zeros((9, 9), dtype=int)
    for _ in range(11):  # Start with a few prefilled cells
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_valid_move(board, row, col, num) or board[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num
    solve_sudoku(board)
    
    # Remove some numbers to create the puzzle
    puzzle = board.copy()
    for _ in range(random.randint(40, 50)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0
    return puzzle, board

# Sidebar with Game Rules and About
st.sidebar.title("📚 Game Rules")
st.sidebar.write("""
1. Each row, column, and 3x3 grid must contain the numbers 1-9 without repetition.  
2. Some cells are pre-filled and cannot be changed.  
3. Fill in the blank cells with numbers from 1-9.  
4. Click **Check Solution** to verify your answer.  
5. Click **New Puzzle** to start a fresh game.  
""")

st.sidebar.title("ℹ️ About this Game")
st.sidebar.write("""
This Sudoku game is built using Python.  
Sudoku is a logic-based number puzzle that challenges players to fill a 9x9 grid correctly.  
Enjoy solving it!


**© 2025 Dark Angel**
""")

# Streamlit App
st.title("🧩 Sudoku Game")

if 'puzzle' not in st.session_state:
    st.session_state['puzzle'], st.session_state['solution'] = generate_sudoku()

st.write("Fill in the Sudoku grid and press **Check Solution** to validate.")

# Display Sudoku Grid
user_grid = []
for i in range(9):
    row = []
    cols = st.columns(9)
    for j in range(9):
        if st.session_state['puzzle'][i][j] != 0:
            cols[j].text_input(
                label=f"R{i+1}C{j+1}",
                value=str(st.session_state['puzzle'][i][j]),
                disabled=True,
                label_visibility="hidden"  # Hides the label
            )
            row.append(st.session_state['puzzle'][i][j])
        else:
            user_input = cols[j].text_input(
                label=f"R{i+1}C{j+1}",
                value="",
                max_chars=1,
                label_visibility="hidden"  # Hides the label
            )
            row.append(int(user_input) if user_input.isdigit() else 0)
    user_grid.append(row)

# Validate the Solution
if st.button("Check Solution"):
    if np.array_equal(np.array(user_grid), st.session_state['solution']):
        st.success("🎉 Congratulations! You've solved the Sudoku puzzle!")
        st.balloons()
    else:
        st.error("❌ Incorrect solution. Try again!")

# Generate a New Puzzle
if st.button("New Puzzle"):
    st.session_state['puzzle'], st.session_state['solution'] = generate_sudoku()
    st.rerun()
