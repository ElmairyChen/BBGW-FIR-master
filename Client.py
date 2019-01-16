import sys
import os
import random
import time
import pickle
import pygame
import threading
from pygame.locals import *
from socket import socket,AF_INET,SOCK_STREAM
from util import connected_domain
from util import five_in_a_row

#def send_point(socket,point):
#    socket.send(point)

def receive_point(socket):
    while True:
    	pos_enemy = pickle.loads(socket.recv(1024))
    	if pos_enemy is not None:
       		enemy_down_real.append(pos_enemy)

enemy_down_real=[]



class CheckerBoard(object):
    """ A class that draw a checker board in memory """
    def __init__(self):
        self.length = 600
        self.width = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.length,self.width))
        pygame.display.set_caption("Five In a Row")

        self.draw_lines(15, 15)

#    def send_point(socket,point):
#        socket.send(point)
#
#    def receive_point(socket):
#        pos_enemy = pickle.loads(socket.recv(1024))
#        if pos_enemy is not None:
#               self.enemy_down_real.append(pos_enemy)


    def draw_lines(self, row, col):
        color = 0,0,0
        width = 1
        board = 20

        white = 255,255,255
        black = 0,0,0

        self.points = {}
        self.grid_witdh = self.width / row
        # record all points
        for r in xrange(row):
            pos_x_start = board
            pos_y = (self.width / row) * r + board
            for p in xrange(col):
                self.points[(pos_x_start+p*(self.length/col), pos_y)] = (r,p)

        mouse_down_x = mouse_down_y = 0
        self.mouse_down_real = []
        #self.enemy_down_real = []
        delay_draw = False
        rtn = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x, mouse_down_y = event.pos
                    pos_real = self.check_mouse_down(mouse_down_x, mouse_down_y)       
                    if pos_real is not None:
                        point=pickle.dumps(pos_real)
#                        threading.Thread(target=receive_point,args=(clientsocket,)).start()
                        clientsocket.send(point)
                        #threading.Thread(target=send_point,args=(clientsocket,point,)).start()
                        #self.mouse_down_real.append(pickle.loads(clientsocket.recv(1024)))
                        self.mouse_down_real.append(pos_real)
                       # when you take one step, enemy will take one step too
                       # pos_enemy = self.take_one_step()
                       # threading.Thread(target=receive_point,args=(clientsocket,)).start()
                 #       pos_enemy = pickle.loads(clientsocket.recv(1024))
                        delay_draw = True
                  #      if pos_enemy is not None:
                   #          self.enemy_down_real.append(pos_enemy)
                        

            self.screen.fill((218,165,32))

            # draw 15*15 lines
            for r in xrange(row):
                pos_y = (self.width / row) * r + board
                pos_x_start = board
                pos_x_end = (self.length/col)*(col-1) + board
                pygame.draw.line(self.screen, color, (pos_x_start,pos_y), (pos_x_end,pos_y), width)
            for c in xrange(col):
                pos_x = (self.length / col) * c + board
                pos_y_start = board
                pos_y_end = (self.width/row)*(row-1) + board
                pygame.draw.line(self.screen, color, (pos_x,pos_y_start), (pos_x,pos_y_end), width)

            # draw five black points for positioning
            for pos in [(col/5,row/5), (col/5,row/5*4-1), (col/5*4-1,row/5),
                    (col/5*4-1,row/5*4-1), (col/2,row/2)]:
                for real_pos in self.points:
                    if pos == self.points[real_pos]:
                        real_pos = real_pos
                        color = 0,0,0
                        radius = 5
                        point_width = 0
                        pygame.draw.circle(self.screen, color, real_pos, radius, point_width)
                        break

            # draw points that you input and machine take
            for point in self.mouse_down_real:
                if piece == 'black':
                     pygame.draw.circle(self.screen, black, point, self.grid_witdh/2-1, 0)
                if piece == 'white':
                     pygame.draw.circle(self.screen, white, point, self.grid_witdh/2-1, 0)
            for point in enemy_down_real:
                if piece == 'black':
                     pygame.draw.circle(self.screen, white, point, self.grid_witdh/2-1, 0)
                if piece == 'white':
                     pygame.draw.circle(self.screen, black, point, self.grid_witdh/2-1, 0)

            pygame.display.update()

            # machine will play fast than what you can image,
            # but i let him sleep several seconds pretending to think
            if delay_draw:
                # check is game over
                # take the check to this because the code will get in
                # here when begin a new round
                rtn = self.check_gameover()
                self.do_if_gameover(rtn)

                
             #   pygame.draw.circle(self.screen, white, self.machine_down_real[-1], self.grid_witdh/2-1, 0)
                delay_draw = False
                pygame.display.update()

                # check is game over again
                # this is check for machine 
               # rtn = self.check_gameover()
               # self.do_if_gameover(rtn)

    def check_mouse_down(self, mouse_down_x, mouse_down_y):
        available_points = set(self.points.keys()) - set(self.mouse_down_real) - set(enemy_down_real)
        min_distance = self.grid_witdh ** 2
        p = (0,0)
        for point in available_points:
            current_distance = (point[0]-mouse_down_x)**2 + (point[1]-mouse_down_y)**2
            if current_distance < min_distance:
                min_distance = current_distance
                p = point
                #print point
                #print mouse_down_x,mouse_down_y
        if min_distance != self.grid_witdh ** 2:
            return p
        else:
            return None

    #def take_one_step(self):
    #    available_points = set(self.points.keys()) - set(self.mouse_down_real) -\
    #                    set(self.machine_down_real)
    #    if len(available_points) != 0:
    #        # pick one point
    #        return random.choice(list(available_points))
    #    else:
    #        return None

    def check_gameover(self):
        # check is game over:
        # you or machine has five in a row
        if self.find_connected_domain(self.mouse_down_real):
            return 1

       # if self.find_connected_domain(self.machine_down_real):
        #    return 2

        return 0

    def find_connected_domain(self, points):
        new_points = []
        for point in points:
            new_points.append(self.points[point])

        connected_domains = connected_domain(new_points)
        for index, domain in connected_domains.iteritems():
            if self.find_five_in_a_row(domain):
                return True

    def find_five_in_a_row(self, points):
        # First version
        # return True if there are five points
        """
        if len(points) < 5:
            return False
        else:
            return True
        """

        # Second version
        # find five point in a row
        if five_in_a_row(points) is None:
            return False
        else:
            return True


    def do_if_gameover(self, rtn):
        color = 255,255,255
        if rtn == 0:
            pass
        else:
            myfont = pygame.font.Font(None, 70)
            textImage = myfont.render("You Win", True, color)
            self.screen.blit(textImage, (self.length/3, self.width/3))
            pygame.display.update()
            time.sleep(1)
            clientsocket.close()
            pygame.quit()
            sys.exit()
            os._exit()

class Piece(object):
    """ An instance of Piece is a point in checker board """
    def __init__(self, pos, is_black):
        self.pos = pos
        if is_black:
            self.color = 0,0,0
        else:
            self.color = 255,255,255
    def pre_draw(self):
        pass



if __name__ == "__main__":

	if(len(sys.argv)<3):
		print 'Usage:python client.py ip port'
		sys.exit()
	host = sys.argv[1]
	port = int(sys.argv[2])
	clientsocket = socket(AF_INET, SOCK_STREAM)
	clientsocket.connect((host, port))
        clientsocket.send(' ')
	piece=clientsocket.recv(1024)
	print "you got ",piece," piece"
        threading.Thread(target=receive_point,args=(clientsocket,)).start()
	checker_board = CheckerBoard()
        
