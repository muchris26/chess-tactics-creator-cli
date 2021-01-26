################################################################################
#
# Chess Tactics Creator - Main function
#
################################################################################

import chess
import chess.engine
import chess.pgn
import fileio

def main(config_info):
    player_name = config_info["Player"]

    # Import the Stockfish analysis engine
    engine = chess.engine.SimpleEngine.popen_uci(config_info["Engine"])

    # Create a chessboard (can place FEN in parens)
    board = chess.Board()

    fens_to_upload = []
    pgn_to_upload = []

    current_fen = board.fen()

    player_color = ""

    pgn_file = open(config_info["PGN File"])

    games = [chess.pgn.read_game(pgn_file) for game_pgn in pgn_file]

    # Remove objects that didn't load correctly
    def test_pgn_list(game):
        if game == None:
            return True
        try:
            pgn_event = '[Event "' + games[i].headers["Event"] + '"]'
        except:
            games.pop(i)
            return True
        return False

    game_count = len(games)
    for i in range(0,game_count):
        test = test_pgn_list(games[i])
        if test == True:
            games.pop(i)
            game_count = game_count - 1

    # Visual confirmation no non-objects
    print(games)

    # primary processing area
    for pgn in games:
        fens = [[board.fen()]]
        game = pgn
        print(game.headers)
        pgn_event = '[Event "' + game.headers["Event"] + '"]'
        pgn_site = '[Site "' + game.headers["Site"] + '"]'
        pgn_date = '[Date "' + game.headers["Date"] + '"]'
        pgn_round = '[Round "' + game.headers["Round"] + '"]'
        pgn_white = '[White "' + game.headers["White"] + '"]'
        pgn_black = '[Black "' + game.headers["Black"] + '"]'
        pgn_result = '[Result "' + game.headers["Result"] + '"]'
        print(pgn_event)
        print(pgn_site)
        print(pgn_date)
        print(pgn_round)
        print(pgn_white)
        print(pgn_black)
        print(pgn_result)
        if game.headers["White"] == player_name:
            player_color = "w"
            print("You are playing White")
        elif game.headers["Black"] == player_name:
            player_color = "b"
            print("You are playing Black")
        print(game.mainline())
        moves = [move for move in game.mainline()]


        for move in moves:
            full_fen = move.board().fen()
            fens[-1].append(move.san())
            fens.append([move.board().fen()])

        for fen in fens:
            
            fen_list = fen[0].split(" ")
            # print(fen_list)
            if fen_list[1] == "b":
                print("Turn: ", fen_list[-1], "B")
            else:
                print("Turn: ", fen_list[-1], "W")
            analysis_board = chess.Board(fen[0])

            position_eval = engine.analyse(analysis_board, chess.engine.Limit(depth=20))
            try:
                next_engine_move = position_eval['pv'][0]
                analysis_board.push(next_engine_move)
                position_eval = engine.analyse(analysis_board, chess.engine.Limit(depth=20))
                # engine_score = position_eval["score"].white()
                engine_score = position_eval["score"].white().score()
                print("Engine Move: ", next_engine_move, " - Engine Score: ", engine_score)
            except:
                print("No More Moves")

            player_board = chess.Board(fen[0])
            try:
                player_board.push_san(fen[1])
                position_eval = engine.analyse(player_board, chess.engine.Limit(depth=20))
                player_score = position_eval["score"].white().score()
                print("Player Move: ", fen[1], " - Player Score: ", player_score)
            except:
                print("No More Moves")

            pgn_data = (pgn_event + '\n' +
                        pgn_site + '\n' +
                        pgn_date + '\n' +
                        pgn_round + '\n' +
                        pgn_white + '\n' +
                        pgn_black + '\n' +
                        pgn_result + '\n' +
                        '[FEN "' + fen[0] + '"]' + '\n' +
                        '\n'

            )

            try:
                compare = int(engine_score)-int(player_score)
                if player_color == "w":
                    if compare > 100 and fen_list[1] == "w":
                        print("Comparison: ", str(compare), "KEY POSITION!!!")
                        fens_to_upload.append(fen[0])
                        pgn_data = pgn_data + "1. " + fen[1] + ' *\n\n'
                        pgn_to_upload.append(pgn_data)

                    else:
                        print("Comparison: ", str(compare))
                elif player_color == "b":
                    if compare < -100 and fen_list[1] == "b":
                        print("Comparison: ", str(compare), "KEY POSITION!!!")
                        fens_to_upload.append(fen[0])
                        pgn_data = pgn_data + "1... " + fen[1] + ' *\n\n'
                        pgn_to_upload.append(pgn_data)
                    else:
                        print("Comparison: ", str(compare))
            except:
                print("Not able to compare")

            print("")

    # Close the Stockfish engine
    engine.quit()

    fileio.writeTXTWithDate("results/fens", fens_to_upload)
    fileio.writeTXTWithDate("results/pgns", pgn_to_upload)
