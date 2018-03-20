##################################################
# Code copyright 2017 Taiki Maeda
# Code released under the MIT license
# https://opensource.org/licenses/mit-license.php
##################################################
import tkinter as tk
import configparser
import os
import shutil
from PIL import Image, ImageTk
import datetime


class BB_Engine(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        # ---------- 外部の設定ファイル・書き込みファイルを読み込み・準備 ----------
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.r_folder = config["setting"]["input_img_folder"]

        self.w_folder = "./annotations"
        if os.path.exists(self.w_folder):
            shutil.rmtree(self.w_folder)
        os.mkdir(self.w_folder)

        # ---------- ラジオボタンの数を，ユーザ設定のラベル数に合わせて自動的に変える ----------
        # ラベル番号(保存する画像のラベルの初期値)
        self.label = 1
        # ラジオボタン初期値
        self.action = tk.IntVar()
        self.action.set(self.label)
        Rb = []
        col = 3
        self.label_quantity = []

        for class_num, class_name in enumerate(config["class_number"]):
            self.label_quantity.append(0)
            class_name = config["class_number"][class_name]
            Rb.append(tk.Radiobutton(self, text=class_name, variable=self.action,
                                     value=class_num, command=self.label_change))
            # ボタン10行おきに列を変えるようにする
            if class_num % 10 == 0:
                col += 1
            Rb[class_num].grid(row=class_num % 10, column=col)

        # ---------- 画像をPILで読み込む ----------
        self.img_name = []
        self.img_list = []
        self._width = []
        self._height = []

        # 全ての画像データをTkinterで扱えるようにする
        filelist = [f for f in os.listdir(self.r_folder)]
        filelist = sorted(filelist)
        #print(filelist)

        for image in filelist:
            self.img_name.append(image)
            # 「.DS_Store」はmacOSの隠しファイルであり，これが読み込みを阻害することがあるから削除
            if self.img_name[0] == ".DS_Store":
                self.img_name.pop(0)
                continue
            path = "{0}/{1}".format(self.r_folder, image)
            img = Image.open(path)
            self.img_list.append(ImageTk.PhotoImage(img))
            self._width.append(img.size[0])
            self._height.append(img.size[1])

        # ---------- 画像表示関連 ----------
        self.width = int(max(self._width))
        self.height = int(max(self._height))
        self.latest_img_num = 0

        # 画像を表示するキャンバス
        self.canvas = tk.Canvas(self, width=self.width,
                                height=self.height)
        self.canvas.grid(row=0, column=0, rowspan=10, columnspan=4)
        self.display_img = self.canvas.create_image(self.width/2, self.height/2,
                                                    image=self.img_list[self.latest_img_num])

        # 選択範囲の初期値
        self.sx = [0, 0]
        self.sy = [0, 0]
        self.square = self.canvas.create_rectangle(0, 0, 0, 0, width=2.0, outline="green", tag="point")
        self.ul_circle = self.canvas.create_oval(0, 0, 0, 0, fill="red", tag="point")
        self.ur_circle = self.canvas.create_oval(0, 0, 0, 0, fill="blue", tag="point")

        # 座標読み取り
        self.canvas.bind("<Button-1>", self.make_square)
        # バインディング
        self.canvas.tag_bind(self.ul_circle, "<Button1-Motion>", self.move_square_ul)
        self.canvas.tag_bind(self.ur_circle, "<Button1-Motion>", self.move_square_ur)

        # ---------- コントロールパネル関連 ----------
        self.exit_button = tk.Button(self, text="終 了", command=self.exit_button, width=20, height=2)
        self.exit_button.grid(row=11, column=0)
        self.button_back = tk.Button(self, text="<< 前(A)", command=self.back_button, width=20, height=2)
        self.button_back.grid(row=11, column=1)
        self.button_next = tk.Button(self, text="次(D) >>", command=self.next_button, width=20, height=2)
        self.button_next.grid(row=11, column=2)
        self.button_save = tk.Button(self, text="保 存(S)", command=self.save_button, width=20, height=2)
        self.button_save.grid(row=11, column=3)
        # キーボードの入力受付
        self.master.bind("<KeyPress>", self.shortcut_key)

        # 現在の画像番号を表示するEntry
        img_num_entry = tk.StringVar()
        self.in_entry = tk.Entry(self, textvariable=img_num_entry)
        self.in_entry.insert(tk.END, "File : {0}".format(self.img_name[self.latest_img_num]))
        self.in_entry.grid(row=12, column=0, pady=5)

        # 作業時の番号
        inum_entry = tk.StringVar()
        self.num_entry = tk.Entry(self, textvariable=inum_entry)
        self.num_entry.insert(tk.END, "num : {0}".format(self.latest_img_num + 1))
        self.num_entry.grid(row=12, column=1, pady=5)

        # ---------- その他の変数初期化・定義 ----------
        self.img_quantity = len(self.img_list)
        self.save_count = 0

        # クリック回数初期化
        self.click_num = 1
        # 保存可能か否か
        self.flag = True

    # ---------- バウンディングボックス関連 ----------
    def make_square(self, event):
        """画像上の2か所を左クリックしたらそれらを対角とする矩形が表示される"""
        # 円半径
        r = 6
        x, y = event.x, event.y
        if self.click_num == 1:
            self.sx[0] = x
            self.sy[0] = y
            self.canvas.coords(self.ul_circle, self.sx[0] - r, self.sy[0] - r, self.sx[0] + r, self.sy[0] + r)
        elif self.click_num == 2:
            self.sx[1] = x
            self.sy[1] = y
            self.canvas.coords(self.ur_circle, self.sx[1] - r, self.sy[1] - r, self.sx[1] + r, self.sy[1] + r)
            self.canvas.coords(self.square, self.sx[0], self.sy[0], self.sx[1], self.sy[1])
            if self.sx[0] >= self.sx[1] or self.sy[0] >= self.sy[1]:
                print("注意：赤丸を左上に，青丸を右下にしてください．")
                self.flag = False
        self.click_num += 1

    def move_square(self):
        """点位置をドラッグで変える"""
        # 円半径
        r = 6
        self.canvas.coords(self.square, self.sx[0], self.sy[0], self.sx[1], self.sy[1])
        self.canvas.coords(self.ul_circle, self.sx[0] - r, self.sy[0] - r, self.sx[0] + r, self.sy[0] + r)
        self.canvas.coords(self.ur_circle, self.sx[1] - r, self.sy[1] - r, self.sx[1] + r, self.sy[1] + r)
        if self.sx[0] >= self.sx[1] or self.sy[0] >= self.sy[1]:
            print("注意：赤丸を左上に，青丸を右下にしてください．")
            self.flag = False
        else:
            self.flag = True

    def move_square_ul(self, event):
        """左上の点を動かす"""
        if self.click_num >= 3:
            self.sx[0] = event.x
            self.sy[0] = event.y
            self.move_square()

    def move_square_ur(self, event):
        """右下の点を動かす"""
        if self.click_num >= 3:
            self.sx[1] = event.x
            self.sy[1] = event.y
            self.move_square()

    # ---------- プログラムの正常終了 ----------
    def end_program(self):
        """作業時におけるアノテーションの作成枚数を記録"""
        # 作業した日時
        now_time = datetime.datetime.today()
        now_time_text = now_time.strftime("%Y/%m/%d %H:%M:%S")
        with open("Latest_Info.txt", "a") as l_file:
            l_file.writelines("{0} に {1} 枚のアノテーションを作成しました．\n".format(now_time_text, self.save_count))

    def exit_button(self):
        """プログラムを終了する"""
        self.end_program()
        exit()

    # ---------- 画像切り替えボタン ----------
    def back_button(self):
        """戻るボタンの挙動"""
        if self.latest_img_num <= 0:
            # 最後にGO
            self.latest_img_num = self.img_quantity - 1
        else:
            # 前の画像に移行
            self.latest_img_num -= 1
        self.canvas.itemconfig(self.display_img, image=self.img_list[self.latest_img_num])
        self.in_entry.delete(0, tk.END)
        self.in_entry.insert(tk.END, "File : {0}".format(self.img_name[self.latest_img_num]))
        self.num_entry.delete(0, tk.END)
        self.num_entry.insert(tk.END, "num : {0}".format(self.latest_img_num + 1))

    def next_button(self):
        """進むボタンの挙動"""
        if self.img_quantity > (self.latest_img_num+1):
            # 次の画像に移行
            self.latest_img_num += 1
        else:
            # 最初にGO
            self.latest_img_num = 0
        self.canvas.itemconfig(self.display_img, image=self.img_list[self.latest_img_num])
        self.in_entry.delete(0, tk.END)
        self.in_entry.insert(tk.END, "File : {0}".format(self.img_name[self.latest_img_num]))
        self.num_entry.delete(0, tk.END)
        self.num_entry.insert(tk.END, "num : {0}".format(self.latest_img_num + 1))

    # ---------- 保存ボタン関連 ----------
    def drawing_reset(self):
        """表示されている描画をすべてリセットする"""
        self.click_num = 1
        self.canvas.delete("point")
        self.square = self.canvas.create_rectangle(0, 0, 0, 0, width=2.0, outline="green", tag="point")
        self.ul_circle = self.canvas.create_oval(0, 0, 0, 0, fill="red", tag="point")
        self.ur_circle = self.canvas.create_oval(0, 0, 0, 0, fill="blue", tag="point")
        self.canvas.tag_bind(self.ul_circle, "<Button1-Motion>", self.move_square_ul)
        self.canvas.tag_bind(self.ur_circle, "<Button1-Motion>", self.move_square_ur)

    def convert_darknet(self, size, box):
        """sx[]とsy[]からダークネット形式に変換する"""
        # 尺度を実サイズに換算
        cw = size[0] / self.width
        ch = size[1] / self.height
        # バウンディングボックスの比率に換算
        dw = 1. / size[0]
        dh = 1. / size[1]
        # 計算
        x = ((box[0] + box[1]) / 2.0) * cw * dw
        y = ((box[2] + box[3]) / 2.0) * ch * dh
        w = (box[1] - box[0]) * dw
        h = (box[3] - box[2]) * dh
        return x, y, w, h

    def save_button(self):
        """保存ボタンの挙動 アノテーションを作成"""
        if self.flag == True:
            if self.click_num >= 3:
                self.drawing_reset()
                b = (float(self.sx[0]), float(self.sx[1]), float(self.sy[0]), float(self.sy[1]))
                #bb = self.convert_darknet((float(self._width[self.latest_img_num]),
                #                           float(self._height[self.latest_img_num])), b)
                bb = [0, 0, 0, 0]
                bb[0] = self.sx[0]
                bb[1] = self.sy[0]
                bb[2] = self.sx[1] - self.sx[0]
                bb[3] = self.sy[1] - self.sy[0]
                # アノテーションを書き込む
                annotation_img = self.img_name[self.latest_img_num]
                annotation_name, ext = os.path.splitext(annotation_img)
                annotation_text_path = self.w_folder + "/" + annotation_name + ".txt"
                annotation_line = "{0} {1} 1 {2} {3} {4} {5}\n".format(annotation_img, self.label, bb[0], bb[1], bb[2], bb[3])
                with open(annotation_text_path, "a") as f:
                    f.writelines(annotation_line)
                # 対応する画像をコピペしてくる
                #annotation_img_path = self.r_folder + "/" + annotation_img
                #if not os.path.exists(self.w_folder + "/" + annotation_img):
                #    shutil.copy(annotation_img_path, self.w_folder + "/" + annotation_img)
                self.save_count += 1
            else:
                print("選択範囲が指定されていません．")
        else:
            print("正確に保存できませんでした．赤丸を左上に，青丸を右下にしてください．")

    # ---------- その他のアクション ----------
    def label_change(self):
        """ラベル(クラス番号)の変更"""
        self.label = self.action.get()

    def shortcut_key(self, event):
        """ショートカットキー"""
        if event.keysym == "d":
            self.next_button()
        elif event.keysym == "a":
            self.back_button()
        elif event.keysym == "s":
            self.save_button()


if __name__ == "__main__":
    root = tk.Tk()
    app = BB_Engine(master=root)
    app.mainloop()
