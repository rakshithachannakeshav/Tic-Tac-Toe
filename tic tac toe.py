import gradio as gr  # Import Gradio for creating the web interface
import numpy as np  # Import NumPy for numerical operations

# Function to check if there's a winner
def check_winner(board):
    for i in range(3):
        if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
            return "Player 1 wins!"  # Check if Player 1 wins
        if np.all(board[i, :] == -1) or np.all(board[:, i] == -1):
            return "Player 2 wins!"  # Check if Player 2 wins
    if board[0, 0] == board[1, 1] == board[2, 2] != 0 or board[0, 2] == board[1, 1] == board[2, 0] != 0:
        return "Player 1 wins!" if board[1, 1] == 1 else "Player 2 wins!"  # Check diagonals
    if np.all(board != 0):
        return "It's a draw!"  # Check if the board is full and it's a draw
    return None  # No winner or draw yet

# Function to make a move on the board
def make_move(board, move, player):
    row, col = divmod(move, 3)  # Convert move index to row and column
    if board[row, col] == 0:
        board[row, col] = player  # Update board with player's move
        winner = check_winner(board)  # Check for a winner after the move
        return board.tolist(), winner
    return board.tolist(), "Invalid move!"  # Return "Invalid move!" if cell is already occupied

# Function to play the game
def play_game(move, board, player, score1, score2):
    board = np.array(board)  # Convert board to a NumPy array
    board, result = make_move(board, move, player)  # Make the move
    if result is None:
        next_player = -player  # Switch player if no winner
    else:
        next_player = player  # Keep the same player if game is over
        if result == "Player 1 wins!":
            score1 += 1  # Update Player 1's score
        elif result == "Player 2 wins!":
            score2 += 1  # Update Player 2's score
        elif result == "It's a draw!":
            score1 += 1  # Update scores for both players if it's a draw
            score2 += 1
    return board, result, next_player, score1, score2  # Return updated board, result, next player, and scores

# Function to reset the game
def reset_game():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "", 1  # Return initial empty board, empty result, and reset player to 1

# Function to update the display
def update_display(board, result, player, score1, score2):
    display_board = np.where(np.array(board) == 1, 'X', np.where(np.array(board) == -1, 'O', ''))  # Convert board to display format
    return display_board.tolist(), result, player, f"Player 1: {score1} | Player 2: {score2}"  # Return display board, result, player, and formatted scores

with gr.Blocks() as demo:  # Create a Gradio Blocks interface
    board = gr.State(value=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])  # Initialize board state
    player = gr.State(value=1)  # Initialize player state
    score1 = gr.State(value=0)  # Initialize Player 1's score
    score2 = gr.State(value=0)  # Initialize Player 2's score
    
    gr.Markdown("### Tic Tac Toe Game")  # Add game title
    gr.Markdown("Player 1: X, Player 2: O")  # Add player instructions

    board_display = gr.DataFrame(interactive=False)  # Create a DataFrame to display the board
    status = gr.Textbox(label="Game Status")  # Create a Textbox to display game status
    scores = gr.Textbox(label="Scores", interactive=False)  # Create a Textbox to display scores

    move_input = gr.Slider(0, 8, step=1, label="Move (0-8)")  # Create a Slider for move input
    submit_button = gr.Button("Make Move")  # Create a Button to submit the move
    reset_button = gr.Button("Reset Game")  # Create a Button to reset the game

    # Define click behavior for the submit button
    submit_button.click(play_game, [move_input, board, player, score1, score2], [board, status, player, score1, score2]).then(
        update_display, [board, status, player, score1, score2], [board_display, status, player, scores]
    )

    # Define click behavior for the reset button
    reset_button.click(reset_game, [], [board, status, player]).then(
        update_display, [board, status, player, score1, score2], [board_display, status, player, scores]
    )

demo.launch()  # Launch the Gradio interface