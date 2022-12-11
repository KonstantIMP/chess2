"""
Точка старта приложения
"""
from chess2.app import ChessApplication
from sys import argv


def main():
    # Создание и запуск приложения
    app = ChessApplication(argv)
    app.exec()
    

if __name__ == '__main__':
    main()
