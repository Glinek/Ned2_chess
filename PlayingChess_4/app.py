import customtkinter as ctk
import math

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        '''Main function generating app's window and configuring all buttons'''
        
        #==== Basic config ====
        self.title("RoboChess")
        self.geometry(f"{250}x{350}")
        
#==== Main APP's loop ===
if __name__ == "__main__":
    app = App()
    app.mainloop()