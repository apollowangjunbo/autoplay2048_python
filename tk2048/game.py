#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Gabriele Cirulli's 2048 puzzle game.

    Python3/tkinter port by Raphaël Seban <motus@laposte.net>

    Copyright (c) 2014+ Raphaël Seban for the present code.

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

import random
import time

try:
    import Tkinter as tk#GUI接口
    import ttk
    import tkMessageBox as messagebox
except:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
# end try

from src import game2048_score as GS
from src import game2048_grid as GG


class GabrieleCirulli2048 (tk.Tk):

    PADDING =10#边界大小
    START_TILES = 2#初始数据量

    def __init__(self, **kw):#这是构造函数
        tk.Tk.__init__(self)#初始化GUI
        for k, v in kw:
            print("Key = {}, value = {}".format(k, v))
        self.initialize(**kw)
    # end def

    def center_window(self, tk_event=None, *args, **kw):
        self.update_idletasks()
        _width = self.winfo_reqwidth()
        _height = self.winfo_reqheight()
        _screen_width = self.winfo_screenwidth()
        _screen_height = self.winfo_screenheight()
        _left = (_screen_width - _width) // 2
        _top = (_screen_height - _height) // 2
        self.geometry("+{x}+{y}".format(x=_left, y=_top))
    # end def

    def initialize(self, **kw):
        self.title("2048")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(width=False, height=False)
        self.withdraw()
        ttk.Style().configure(".", font="sans 10")
        _pad = self.PADDING
        self.grid = GG.Game2048Grid(self, **kw)
        self.hint = ttk.Label(
            self, text="Hint: use keyboard arrows to move tiles."
        )
        self.score = GS.Game2048Score(self, **kw)
        self.hiscore = GS.Game2048Score(self, label="Highest:", **kw)
        self.grid.pack(side=tk.TOP, padx=_pad, pady=_pad)
        self.hint.pack(side=tk.TOP)
        self.score.pack(side=tk.LEFT)
        self.hiscore.pack(side=tk.LEFT)
        ttk.Button(
            self, text="Quit!", command=self.quit_app,
        ).pack(side=tk.RIGHT, padx=_pad, pady=_pad)
        ttk.Button(
            self, text="New Game", command=self.new_game,
        ).pack(side=tk.RIGHT)
        ttk.Button(
            self, text="AI Game", command=self.ai_new_game,
        ).pack(side=tk.RIGHT)
        self.grid.set_score_callback(self.update_score)
    # end def

    def new_game(self, *args, **kw):
        self.unbind_all("<Key>")
        self.score.reset_score()
        self.grid.reset_grid()
        for n in range(self.START_TILES):
            self.after(
                100 * random.randrange(3, 7), self.grid.pop_tile
            )
        # end if
        self.bind_all("<Key>", self.on_keypressed)
    # end def

    def quit_app(self, **kw):
        if messagebox.askokcancel("Question", "Quit game?"):
            self.quit()
            self.destroy()
        # end if
    # end def

    def run(self, **kw):
        self.center_window()
        self.deiconify()
        self.new_game(**kw)
        self.mainloop()
    # end def

    def on_keypressed(self, tk_event=None, *args, **kw):

        _event_handler = {
            "left": self.grid.move_tiles_left,
            "right": self.grid.move_tiles_right,
            "up": self.grid.move_tiles_up,
            "down": self.grid.move_tiles_down,
            "escape": self.quit_app,
        }.get(tk_event.keysym.lower())
        try:
            _event_handler()
            self.hint.pack_forget()
        except:
            pass

        tiles = self.grid.tiles
        # print("tiles = {}".format(tiles))
        for t in tiles:
            print("Tile id = {}, tile row = {}, tile column = {}, value = {}".
                  format(t, tiles[t].row, tiles[t].column, tiles[t].value))
        print("--------------------------")
        self.getmat()
        print("--------------------------")
        # end try
    # end def

    def update_score(self, value, mode="add"):
        if str(mode).lower() in ("add", "inc", "+"):
            self.score.add_score(value)
        else:
            self.score.set_score(value)
        # end if
        self.hiscore.high_score(self.score.get_score())
    # end def

    def ai_new_game(self, *args, **kw):
        self.unbind_all("<Key>")
        self.score.reset_score()
        self.grid.reset_grid()
        for n in range(self.START_TILES):
            self.after(
                100 * random.randrange(3, 7), self.grid.pop_tile
            )
        # end if
        self.playloops = 0
        self.after(200, self.ai_pressed)  # 多长时间后调用下一次ai_pressed
        self.bind_all("<Key>", self.on_keypressed)

    # end def

    # 定义一个AI程序，按了界面上的ai运行按钮后会定时触发
    # 在这个子程序里面运行一次AI操作
    def ai_pressed(self, tk_event=None, *args, **kw):
        self.playloops = self.playloops + 1
        matrix = self.grid.matrix.matrix

        # get the values of cells
        tiles = self.grid.tiles
        for t in tiles:
            print("Tile id = {}, tile row = {}, tile column = {}, value = {}".
                  format(t, tiles[t].row, tiles[t].column, tiles[t].value))
########################################################核心算法##############
        mat= self.getmat()
        two=list()
        four=list()
        for t in tiles:
            if tiles[t].value==2:
                two.append(tiles[t])
            elif tiles[t].value==4:
                four.append(tiles[t])
        print("--------------------------")


        #lastlist1=copy.deepcopy(tiles)
#用于整理最下方两行错位的状况
        '''if mat[2][0]==0 and mat[2][1]!=0 and mat[2][2]!=0 and mat[2][3]!=0:
            if mat[3][0]!=0 and mat[3][1]!=0 and mat[3][2]!=0 and mat[3][3]!=0 :
                if mat[2][3]==mat[3][2] or mat[2][2]==mat[3][1] or mat[2][1]==mat[3][0]:
                    if mat[3][0]!=mat[3][1] and mat[3][1]!=mat[3][2] and mat[3][2]!=mat[3][3]:
                        print("错位整理")
                        self.grid.move_tiles_left()
                        self.grid.move_tiles_down()'''
        #用于整理最下方两行错位的状况
        dold=False
        r4=self.getrowdifnum(3)
        r3=self.getrowdifnum(2)
        if r4==4 :
            print("第四行满了")
            if r3<4 :
                for i1 in range(0,r3):
                    if mat[3][i1]==mat[2][i1+4-r3]:
                        dold=True
                if dold and mat[3][0]+mat[3][1]+mat[3][2]+mat[3][3]>200:                    
                    print("错位整理")
                    self.grid.move_tiles_left()
                    #time.sleep(2)
                    self.grid.move_tiles_down()
        #用于整理2/3方行错位的状况
        dold=False
        r4=self.getrowdifnum(3)
        r3=self.getrowdifnum(2)
        r2=self.getrowdifnum(1)
        if r4==4 and r3==4:
            print("前两行满了")
            if r2<4 :
                for i1 in range(0,r2):
                    if mat[2][i1]==mat[1][i1+4-r2]:
                        dold=True
                if dold:
                    print("错位整理")
                    self.grid.move_tiles_left()
                    #time.sleep(2)
                    self.grid.move_tiles_down()

#尽可能合并2/4
        lastlist1=list()
        newlist=list()
        for t1 in tiles:
            lastlist1.extend([t1, tiles[t1].row, tiles[t1].column, tiles[t1].value])

        if len(two)>=2 and self.ai_candown(two):
            print("Move down cause 2")
            self.grid.move_tiles_down()
        elif len(four)>=2 and self.ai_candown(four):
            print("Move down cause 4")
            self.grid.move_tiles_down()
        elif len(two)>=2 and self.ai_canright(two):
            print("Move right cause 2")
            self.grid.move_tiles_right()
        elif len(four)>=2 and self.ai_canright(four):
            print("Move right cause 4")
            self.grid.move_tiles_right()
        else:#依次尝试下右左上
            print("Try to move down")
            self.grid.move_tiles_down()
            for t2 in tiles:
                newlist.extend([t2, tiles[t2].row, tiles[t2].column, tiles[t2].value])
            #newlist=list(tiles)
            if self.compare(lastlist1,newlist):#lastlist1==tiles:
                print("Defeat and Try to move right")
                self.grid.move_tiles_right()
                newlist.clear()
                for t3 in tiles:
                    newlist.extend([t3, tiles[t3].row, tiles[t3].column, tiles[t3].value])
                if self.compare(lastlist1,newlist):
                    print("Defeat and Try to move left")
                    self.grid.move_tiles_left()
                    #time.sleep(0.2)
                    print("Then try to move right")
                    self.grid.move_tiles_right()
                    newlist.clear()
                    for t4 in tiles:
                        newlist.extend([t4, tiles[t4].row, tiles[t4].column, tiles[t4].value])
                    if self.compare(lastlist1,newlist):
                        print("Then try to move down")
                        self.grid.move_tiles_up()
                        #time.sleep(0.2)
                        self.grid.move_tiles_down()

        if self.grid.no_more_hints():  # game over
            # self.ai_new_game()  # play ai again
            pass
        else:
            self.after(100, self.ai_pressed)  # ai press again after 200 ms

    def ai_candown(self,num):
        ins=False
        tiles = self.grid.tiles
        val= num[0].value
        for i in range(0,len(num)-1):
            for k in range(i+1,len(num)):
                if num[i].column==num[k].column:#列号相同
                    if num[i].row==num[k].row+1 or num[i].row==num[k].row-1 :#上下挨着
                        return True
                    elif  num[i].row==num[k].row+2 or num[i].row==num[k].row-2 :#上下隔一个
                        ins=False
                        for t in tiles:#看看有没有块在两个中间
                            if (tiles[t].column)==(num[i].column) and (tiles[t].row)==(num[i].row+num[k].row)/2:
                                ins=True
                        if ins==False:
                            return True
                    elif num[i].row==num[k].row+3 or num[i].row==num[k].row-3:#上下隔两个
                        #print("1")
                        ins=False
                        for t in tiles:#看看有没有块在两个中间
                            if (tiles[t].column)==(num[i].column):
                                if tiles[t].row==2 or tiles[t].row==3:
                                    ins=True
                                #print("2")

                        if ins==False:
                            #print("3")
                            return True
                    else:
                        pass
        return False
        #end ai_candown
    def ai_canright(self,num):
        ins=False
        tiles = self.grid.tiles
        val= num[0].value
        for i in range(0,len(num)-1):
            for k in range(i+1,len(num)):
                if num[i].row==num[k].row:#行号相同
                    if num[i].column==num[k].column+1 or num[i].column==num[k].column-1 :#上下挨着
                        return True
                    elif  num[i].column==num[k].column+2 or num[i].column==num[k].column-2 :#上下隔一个
                        ins=False
                        for t in tiles:#看看有没有块在两个中间
                            if (tiles[t].row)==(num[i].row) and (tiles[t].column)==(num[i].column+num[k].column)/2:
                                ins=True
                        if ins==False:
                            return True
                    elif num[i].column==num[k].column+3 or num[i].column==num[k].column-3:#上下隔两个
                        ins=False
                        for t in tiles:#看看有没有块在两个中间
                            if (tiles[t].row)==(num[i].row):
                                if tiles[t].column==2 or tiles[t].column==3:
                                    ins=True

                        if ins==False:
                            return True
                    else:
                        pass
        return False
        #end ai_candown
    def compare(self,a1,b1):
        #tiles = self.grid.tiles
        if len(a1)==len(b1):
            #print("{0}{1}".format(len(a2),len(b2)))
            for i in range(0,len(a1)):
                #print(a2,b2)
                #print("{0}{1}".format(a1[i].id,b1[i].id))
                if a1[i]!=b1[i]:
                    return False
            return True
        else:
            return False
    def getmat(self):
        tiles = self.grid.tiles
        mat=[[0]*4,[0]*4,[0]*4,[0]*4]
        for t in tiles:
            mat[tiles[t].row][tiles[t].column]=tiles[t].value
        #print(mat)
        return mat
    def getrowdifnum(self,r):
        mat=self.getmat()
        num=0
        mylist=list()
        for i in range(0,4):
            if mat[r][i]!=0:
                num+=1
                mylist.append(i)
        if num>=2:
            for k in range(0,len(mylist)-1):
                if mat[r][mylist[k]]==mat[r][mylist[k+1]]:
                    num-=1
        return num









# end class

if __name__ == "__main__":
    GabrieleCirulli2048().run()
# end if
