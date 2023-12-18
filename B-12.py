import pyxel

class Ball:
    speed = 1
    r = 10 #共通しているところはクラス全体で呼びかける
    color = 6


    def __init__(self):
        self.x = pyxel.rndi(0, 199)
        self.y = 0
        angle = pyxel.rndi(30, 150) #ローカル変数
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        self.point_flags = True

    def move(self):
        self.x += self.vx * Ball.speed
        self.y += self.vy * Ball.speed

pyxel.init(200,200)

pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='77', effects='NN', speed=10)
pyxel.sound(1).set(notes='G2G2', tones='NN', volumes='33', effects='NN', speed=10)

balls = [Ball()]
padx = 100
point = 0
miss = 0
gameover_flag = False

def update():
    global balls,padx,point,miss,gameover_flag

    if gameover_flag:
        return

    padx = pyxel.mouse_x

    for b in balls:
        b.x += (b.vx * Ball.speed)
        b.y += (b.vy * Ball.speed)

        if b.y >= 200:
            if b.point_flags:
                pyxel.play(0,1)
                miss += 1
                if miss >= 10:
                    gameover_flag = True
            b.x = pyxel.rndi(0,199)
            b.y = 0
            new_angles = pyxel.rndi(30,150)
            Ball.speed = Ball.speed * 1.2
            b.vx = pyxel.cos(new_angles)
            b.vy = pyxel.sin(new_angles)
            b.point_flags = True

        if (b.x >= 200 and b.vx > 0) or (b.x <= 0 and b.vx < 0):
            b.vx = b.vx * -1

        if padx-20 <= b.x <= padx+20 and b.y >= 195 and b.point_flags:
            pyxel.play(0,0)
            point = point + 1
            b.point_flags = False
            #ポイントがボールの個数の10倍を超えていたらボールを増やす
            if point >= len(balls) * 10:
                balls.append(Ball())
                Ball.speed = 1



def draw():
    global balls,padx,point,gameover_flag
    if gameover_flag:
         pyxel.text(80,100,"GAME OVER!!",0)
    else:
        pyxel.cls(7)
        for b in balls:
                pyxel.circ(b.x, b.y, Ball.r, Ball.color)
        pyxel.rect(padx-20, 195, 40, 5, 14)
        pyxel.text(100,100,str(point),0)

pyxel.run(update, draw)