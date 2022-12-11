"""
Entry point for the app
"""
from chess2.app import ChessApplication
import logging as lg
from sys import argv


def main():
    # Loggers init
    lg.basicConfig(
        level=lg.INFO, filename='chess.log',
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    lg.info(f'Chess 2.0 started with {len(argv)} cli argument(s)')

    app = ChessApplication(argv)
    app.exec()
    

if __name__ == '__main__':
    main()
