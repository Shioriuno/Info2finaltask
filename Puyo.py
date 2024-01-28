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
        #self.check_flag = False
        self.torari_flag = False
        self.check_count = 0
        self.chain_count = 0
        
        self.append_flag = True


        if self.type == 0:
            self.color = 14
        if self.type == 1:
            self.color = 6
        if self.type == 2:
            self.color = 10
        if self.type == 3:
            self.color = 11

    def move(self, app): #左右のみ
        if (pyxel.btnp(pyxel.KEY_LEFT)) and (0 < self.posa):
            self.posa -= 1
        if (pyxel.btnp(pyxel.KEY_RIGHT)) and (self.posa < 10):
            self.posa += 1

    def drop(self, app): #落下
        self.append_flag = App.check(app)
        if self.posb == 14 or any((self.posa == puyo.posa and self.posb == puyo.posb - 1) for puyo in app.puyos):
            #Puyo.check(self,app)
            if self.append_flag:
                app.puyos.append(self)
                print("append")
                print(app.puyos)
            app.movepuyo = Puyo()
            self.check_flag = True
        elif pyxel.frame_count % 5 == 0:
            self.posb += 1
            self.check_flag = False


    def check(self, app):
        if self.check_flag:
            no = 0
            dellist = []
            for puyo in app.puyos:
                if (self.posa + 1 == puyo.posa and self.posb == puyo.posb):
                    if (self.type == puyo.type):
                        print("right"+str(no))
                        dellist.append(no)

                if (self.posa == puyo.posa and self.posb + 1 == puyo.posb):
                    if (self.type == puyo.type):
                        print("down")
                        dellist.append(no)

                print(no)
                no += 1
        
            return dellist #削除対象No.リスト
        

class App:
    def __init__(self):
        pyxel.init(200, 300)

        self.puyos = []
        self.movepuyo = Puyo()
        self.dellist = []

        pyxel.run(self.update, self.draw)


    def check(self): #それぞれのpuyoのcheck()を左端から順に呼び出す
        print("checkstart")
        no = 0
        delnolist = []
        delno = -1
        checklist_order = []
        self.dellist = []
        return_flag = True
        for b in range(15): #左端からpuyosリストのNo.を記録
            for a in range(10):
                no = 0
                for puyo in self.puyos:
                    if (puyo.posa == a and puyo.posb == (14-b)):
                        checklist_order.append(no)
                    no += 1

        print(checklist_order)
        for order in checklist_order: #順番に呼び出す
            print("order"+str(order))
            
            delnolist = self.puyos[order].check(self)
            for d in delnolist: #右or上の削除対象＋自分のNo.を記録
                if d >= 0:
                    self.dellist.append(d)
                    self.dellist.append(order)

            lastpuyo = len(self.puyos) - 1 #さっきまで動いていたpuyoかの判定用

        print("dellist"+str(self.dellist))

        if self.dellist != None:
            self.dellist.sort(reverse=True) #list No.の大きい順に消さないと狂うためソート
            for d in self.dellist:
                print("delete" + str(lastpuyo) + str(d))
                if not (d == lastpuyo or (lastpuyo >= len(self.puyos) - 1)): #削除対象がさっきまで動いていたpuyoではないかチェック
                    del self.puyos[lastpuyo]
                del self.puyos[d]
                checklist_order = []
                return_flag = False

        

        return return_flag
        

    def update(self):
        self.movepuyo.move(self)
        self.movepuyo.drop(self)
        
        # ぷよの座標について
        self.movepuyo.y = self.movepuyo.posb * 20 + 10
        self.movepuyo.x = self.movepuyo.posa * 20 + 10

        #self.dellist = self.movepuyo.check(App)
        #if self.dellist != None:
        
        #if self.movepuyo(self.posa, self.posb) == (5,0):

         #   print("GAMEOVER")

    def draw(self):
        pyxel.cls(7)
        pyxel.circ(self.movepuyo.x, self.movepuyo.y, Puyo.r, self.movepuyo.color)

        i=0
        for b in self.puyos:
            pyxel.circ(b.x, b.y, Puyo.r, b.color)
            pyxel.text(b.x, b.y, str(i), 0)
            i+=1


App()

