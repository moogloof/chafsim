from tkinter import *
import models


class Window(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Charges and Fields")
        self.resizable(0, 0)

        self.canvas = Canvas(self, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.info_frame = InfoFrame(self, bd=0, highlightthickness=0)

        self.canvas.grid(row=0, column=0)
        self.info_frame.grid(row=0, column=1)

        self.update()

        p1 = models.Particle(50, 50)
        system = models.System([p1])
        self.display(system)

        self.mainloop()

    def display(self, system):
        for particle in system.get_particles():
            self.canvas.create_oval(particle.x - 5, particle.y - 5, particle.x + 5, particle.y + 5, fill="white")


class InfoFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    Window()
