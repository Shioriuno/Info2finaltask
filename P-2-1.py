import pyxel

class Puyo:
    r = 10

    def __init__(self):
        self.x = 130
        self.y = 10
        self.vx = 0
        self.vy = 1
        self.posa = 5
        self.posb = 0
        self.type = pyxel.rndi(0, 3)
        self.check_flag = False
        self.torari_flag = False
        self.check_count = 0
        self.chain_count = 0

        if self.type == 0:
            self.color = 14
        if self.type == 1:
            self.color = 6
        if self.type == 2:
            self.color = 10
        if self.type == 3:
            self.color = 11

    def move(self, app):
        if (pyxel.btnp(pyxel.KEY_LEFT)) and (0 < self.posa):
            self.posa -= 1
        if (pyxel.btnp(pyxel.KEY_RIGHT)) and (self.posa < 10):
            self.posa += 1

    def drop(self, app):
        if pyxel.frame_count % 5 == 0:
            self.posb += 1

            for puyo in app.puyos:
                if (self.posa == puyo.posa) and (self.posb == puyo.posb - 1):
                    app.puyos.append(Puyo())
                    app.movepuyo = Puyo()
                    self.check_flag = True

            if self.posb == 15 or any((self.posa == puyo.posa and self.posb == puyo.posb) for puyo in app.puyos):
                app.puyos.append(self)
                app.movepuyo = Puyo()
                self.check_flag = True
                print(self.check_flag)

    def check(self, app):
        if self.check_flag:
            no = 0
            dellist = []
            for puyo in app.puyos:
                if (self.posa == puyo.posa and self.posb == puyo.posb - 1)and (self.type == puyo.type):
                    self.chain_count += 1
                    dellist.append(no)
                    print("checker")
                if (self.posa == puyo.posa and self.posb == puyo.posb + 1)and (self.type == puyo.type):
                    self.chain_count += 1
                    dellist.append(no)
                    print("checker")
                if (self.posa == puyo.posa - 1 and self.posb == puyo.posb)and (self.type == puyo.type):
                    self.chain_count += 1
                    dellist.append(no)
                    print("checker")
                if (self.posa == puyo.posa + 1 and self.posb == puyo.posb)and (self.type == puyo.type):
                    self.chain_count += 1
                    dellist.append(no)
                    print("checker")
                no += 1
                #print(self.chain_count)
            if self.chain_count >= 2:
                #App.delpuyo.append(self)
                #del App.delpuyo
                print(type(dellist))
                print("delete")
                
                return dellist

class App:
    def __init__(self):
        pyxel.init(200, 300)

        self.puyos = []
        self.movepuyo = Puyo()
        self.delpuyo = []

        self.dellist = []

        pyxel.run(self.update, self.draw)

    def update(self):
        self.movepuyo.move(self)
        self.movepuyo.drop(self)
        for p in self.puyos:
            p.check(self)
#        self.puyos.check(self)

        # ぷよの座標について
        self.movepuyo.y = self.movepuyo.posb * 20 + 10
        self.movepuyo.x = self.movepuyo.posa * 20 + 10

        self.dellist = self.movepuyo.check(App)
        if self.dellist != None:
            for d in self.dellist:
                print(d)
                del self.puyos[d]

        #if self.movepuyo(self.posa, self.posb) == (5,0):

         #   print("GAMEOVER")

    def draw(self):
        pyxel.cls(7)
        pyxel.circ(self.movepuyo.x, self.movepuyo.y, Puyo.r, self.movepuyo.color)

        for b in self.puyos:
            pyxel.circ(b.x, b.y, Puyo.r, b.color)


App()