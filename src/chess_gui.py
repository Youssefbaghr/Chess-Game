import chess
import tkinter as tk
import chess.engine

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")

        self.board = chess.Board()
        self.selected_piece = None
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        self.message_label = tk.Label(self.root, text="Player's turn: You", bg='lightgray', width=30)
        self.message_label.pack()

        self.ai_captured_label = tk.Label(self.root, text="AI Captured Pieces: ", bg='lightgray')
        self.ai_captured_label.pack()

        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_drop)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                x0, y0 = col * 50, row * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_pieces(self):
        piece_symbols = {
            chess.PAWN: "♙", chess.KNIGHT: "♘", chess.BISHOP: "♗", chess.ROOK: "♖", chess.QUEEN: "♕", chess.KING: "♔",
            -chess.PAWN: "♟", -chess.KNIGHT: "♞", -chess.BISHOP: "♝", -chess.ROOK: "♜", -chess.QUEEN: "♛", -chess.KING: "♚"
        }

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_symbol = piece_symbols.get(piece.piece_type, None)
                if piece_symbol:
                    col, row = chess.square_file(square), 7 - chess.square_rank(square)
                    player_color = "blue" if piece.color == chess.WHITE else "red"
                    self.canvas.create_text(col * 50 + 25, row * 50 + 25, text=piece_symbol, font=("Arial", 24), fill=player_color, tags="piece")

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()

    def get_square(self, x, y):
        return x // 50, y // 50

    def on_click(self, event):
        col, row = self.get_square(event.x, event.y)
        square = chess.square(col, 7 - row)
        if self.selected_piece is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_piece = square
                self.highlight_legal_moves(square)
                self.canvas.tag_raise("selected")
        else:
            move = chess.Move(self.selected_piece, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.check_game_status()
                self.message_label.config(text="Player's turn: Stockfish", bg='lightgray')
                self.root.after(500, self.ai_move)
            self.selected_piece = None
            self.clear_highlight()

    def on_drag(self, event):
        if self.selected_piece:
            col, row = self.get_square(event.x, event.y)
            x0, y0 = col * 50 + 10, row * 50 + 10
            x1, y1 = x0 + 30, y0 + 30
            self.canvas.coords("selected", x0, y0, x1, y1)

    def on_drop(self, event):
        if self.selected_piece:
            col, row = self.get_square(event.x, event.y)
            square = chess.square(col, 7 - row)
            move = chess.Move(self.selected_piece, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.check_game_status()
                self.message_label.config(text="Player's turn: Stockfish", bg='lightgray')
                self.root.after(500, self.ai_move)
            self.selected_piece = None
            self.clear_highlight()

    def highlight_legal_moves(self, square):
        legal_moves = [move.to_square for move in self.board.legal_moves if move.from_square == square]
        for square in legal_moves:
            col, row = chess.square_file(square) * 50, (7 - chess.square_rank(square)) * 50
            x0, y0 = col, row
            x1, y1 = col + 50, row + 50
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="green", tags="legal")

    def clear_highlight(self):
        self.canvas.delete("legal")

    def ai_move(self):
        with chess.engine.SimpleEngine.popen_uci("Your stockfich paths") as engine:
            result = engine.play(self.board, chess.engine.Limit(time=2.0))
            if result.move is not None:
                # Check if a piece was captured by AI
                captured_piece = self.board.piece_at(result.move.to_square)
                if captured_piece is not None:
                    captured_piece_symbol = self.get_piece_symbol(captured_piece)
                    self.ai_captured_label.config(text=f"AI Captured Pieces: {captured_piece_symbol}")
            self.board.push(result.move)
            self.update_board()
            self.check_game_status()
            self.message_label.config(text="Player's turn: You", bg='lightgray')

    def get_piece_symbol(self, piece):
        piece_symbols = {
            chess.PAWN: "♙", chess.KNIGHT: "♘", chess.BISHOP: "♗", chess.ROOK: "♖", chess.QUEEN: "♕", chess.KING: "♔",
            -chess.PAWN: "♟", -chess.KNIGHT: "♞", -chess.BISHOP: "♝", -chess.ROOK: "♜", -chess.QUEEN: "♛", -chess.KING: "♚"
        }
        return piece_symbols.get(piece.piece_type, "")

    def check_game_status(self):
        result = self.board.result()
        if result != "*":
            if result == "1-0":
                winner = "You win!"
            elif result == "0-1":
                winner = "AI wins!"
            else:
                winner = "It's a draw!"
            self.message_label.config(text=f"Game over. {winner}", bg='lightgray')
