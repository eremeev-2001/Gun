
from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

class ball():
    
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.k=0
        
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME

       
        if self.x >= 800:
           self.vx  = self.vx*-1
        if self.y >= 600:
            self.vy = ((self.vy+self.k-2)*-1)
            self.k = 0
        
        canv.move(self.id,self.vx,self.vy+self.k)
        self.x += self.vx
        self.y += self.vy+self.k
        self.k+=2
        
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if  (self.x -obj.x)**2+(self.y-obj.y)**2 < (self.r+obj.r)**2  :
            return True        
        else:
            return False    


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.x-20 != 0:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfigure(self.id, fill='orange')
        else:
            canv.itemconfigure(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfigure(self.id, fill='orange')
        else:
            canv.itemconfigure(self.id, fill='black')


class target():
    def __init__(self):
        global all_points
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canv.create_oval(0,0,0,0)        
        self.new_target()
        
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 50)
        self.dx = rnd(1,3)
        self.dy = rnd(1,3)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfigure(self.id, fill=color)
        self.move()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global all_points
        canv.coords(self.id, -10, -10, -10, -10)
        all_points += points
        canv.itemconfigure(id_points, text=all_points)

    def move(self):
        if self.live == 1:
            x1, y1, x2, y2 = canv.coords(self.id)
            canv.move(self.id, self.dx, self.dy)
            self.x = self.x + self.dx
            self.y = self.y + self.dy
   
            if x2 >= int(canv["width"]):
                self.dx = rnd(1,3)*-1
            if x1 <= 0:
                self.dx = rnd(1,3)    
            if y2 >= int(canv["height"]):
                self.dy = rnd(1,3)*-1
            if y1 <= 0:
                self.dy = rnd(1,3)
                                
            root.after(20, self.move)
    


bullet = 0
balls = []
targets = []
all_points=0

def new_game(event=''):
    global gun, t1, screen1, balls, bullet
    g1 = gun()

    targets.clear()        
    t1 = target()
    t1.new_target()
    targets.append(t1)
    t2 = target()
    t2.new_target()
    targets.append(t2)
    t3 = target()
    t3.new_target()
    targets.append(t3)
    
    bullet = 0
    balls = []
    screen1 = canv.create_text(400, 300, text='', font='28')
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    livetarget = len(targets)           
    while livetarget > 0:
        for b in balls:
            b.move()
            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
                    livetarget = livetarget - 1
                    
            if (livetarget == 0):
                canv.itemconfigure(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                break
            
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
        
    time.sleep(1)
    canv.itemconfigure(screen1, text='')
    canv.delete(g1.id)
    for b in balls:
        canv.delete(b.id)
    canv.delete(t1.id)
    root.after(750, new_game)

id_points = canv.create_text(30,30,text = all_points,font = '28')
new_game()

root.mainloop()
