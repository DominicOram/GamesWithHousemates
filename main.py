import pygame
import socket               # Import socket module
import pickle
import threading
import time

pygame.init()

DISPLAY = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

crashed = False

rectangle_x = 100
rectangle_y = 100

enemy_rectangle_x = 200
enemy_rectangle_y = 200

x_velocity = 0
y_velocity = 0

MY_PORT = 10000
PLAYER2_PORT = 10000
PLAYER_2_IP = '192.168.0.142'  # The server's hostname or IP address


def start_server():
    HOST = '192.168.0.234' # Get local machine name

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, MY_PORT))
        server.listen()
        conn, addr = server.accept()
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    global enemy_rectangle_x, enemy_rectangle_y
                    enemy_rectangle_x, enemy_rectangle_y = pickle.loads(data)
                    print("Got new position {}".format((enemy_rectangle_x, enemy_rectangle_y)))
                except Exception as e:
                    print("Got error {} when recieving".format(e))


server_thread = threading.Thread(target=start_server, args=(), daemon=True)
server_thread.start()


def send_to_server():
    connected = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                if not connected:
                    s.connect((PLAYER_2_IP, PLAYER2_PORT))
                    connected = True
                s.sendall(pickle.dumps((rectangle_x, rectangle_y)))
                print("Sent new position {}".format((rectangle_x, rectangle_y)))
            except Exception as e:
                print("Got error {} when sending".format(e))
            time.sleep(0.01)


client_thread = threading.Thread(target=send_to_server, args=(), daemon=True)
client_thread.start()

while not crashed:

    gravity = 0.9
    #print("Gravity is at {}".format(gravity))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_velocity = -5
            elif event.key == pygame.K_RIGHT:
                x_velocity = 5
            elif event.key == pygame.K_UP:
                y_velocity = -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_velocity = 0

        #print(event)

    DISPLAY.fill(WHITE)

    y_velocity += gravity

    rectangle_x += x_velocity
    rectangle_y += y_velocity

    if rectangle_y > 500:
        rectangle_y = 500
        y_velocity = 0

    pygame.draw.rect(DISPLAY, BLUE, (rectangle_x, rectangle_y, 100, 50))
    pygame.draw.rect(DISPLAY, RED, (enemy_rectangle_x, enemy_rectangle_y, 100, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

