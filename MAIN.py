from Game_Algorithm import *

#window initialization
root = Tk()
root.title = "Battleship"
root.geometry("800x500+100+100")

#application initialization
app = Game(master=root)
app.mainloop()
