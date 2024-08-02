import socket
import time
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


def find(raw: str):
    first = None
    for num, sign in enumerate(raw):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(raw[first + 1:second].split(","))
            return result
    return ""


main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настройка сокета
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирования
main_socket.bind(('192.168.0.108', 56700))  # IP и порт привязываем к порту
main_socket.setblocking(False)  # Непрерывность, не ждём ответа
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных подключений
print("Сокет создался")

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()


class Player(Base):
    __tablename__ = "gamers"
    name = Column(String, primary_key=True)
    password = Column(String(250))
    score = Column(Integer, default=0)

    def __init__(self, name, passw):
        self.name = name
        self.password = passw


Base.metadata.create_all(engine)

players = []
run = True
while run:
    try:
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)
        players.append(new_socket)
    except BlockingIOError:
        pass
    for sock in players:
        try:
            data = sock.recv(1024).decode()
            print("Получил", data)
            data = find(data)
            if data[0] == "final":
                data.remove("final")
                player = s.get(Player, data[0])
                if player.score < int(data[2]):
                    player.score = int(data[2])
                s.merge(player)
                s.commit()
            if data:
                player = Player(data[0], data[1])
                s.add(player)
                s.commit()
                sock.send("<0>".encode())
                sock.close()
                players.remove(sock)
            # run = False
            # break
        except sqlalchemy.exc.IntegrityError:
            s.rollback()
            player = s.get(Player, data[0])
            if data[1] == player.password:
                sock.send(f"<{player.score}>".encode())
            else:
                sock.send("<-1>".encode())
            sock.close()
            players.remove(sock)
            # run = False
            # break

    time.sleep(1)
