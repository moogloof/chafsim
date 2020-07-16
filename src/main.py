from tkinter import *
import models
import math


class Window(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Charges and Fields")
        self.resizable(0, 0)

        p1 = models.Particle(100, 300)
        p2 = models.Particle(700, 300, -1)
        system = models.System([p1, p2])

        self.canvas = Canvas(self, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.info_frame = InfoFrame(system, self, bd=0, highlightthickness=0)

        self.canvas.bind("<Motion>", self.info_frame.update)

        self.canvas.grid(row=0, column=0)
        self.info_frame.grid(row=0, column=1)

        self.update()

        self.display(system)

        self.mainloop()

    def display(self, system):
        arrow_sep = 50
        for x in range(self.canvas.winfo_width() // arrow_sep):
            for y in range(self.canvas.winfo_height() // arrow_sep):
                f = system.get_field(x * arrow_sep, y * arrow_sep)

                if not f:
                    continue

                f[0] /= 20000
                f[1] /= 20000

                self.canvas.create_oval(x * arrow_sep - 2, y * arrow_sep - 2,
                    x * arrow_sep + 2, y * arrow_sep + 2,
                    outline="white", fill="white")

                self.canvas.create_line(x * arrow_sep, y * arrow_sep,
                    x * arrow_sep + f[0], y * arrow_sep + f[1],
                    fill="white")

        for particle in system.get_particles():
            self.canvas.create_oval(particle.x - 5, particle.y - 5, particle.x + 5, particle.y + 5, outline="red", fill="red")


class InfoFrame(Frame):
    def __init__(self, field, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.x_label_var = StringVar()
        self.x_label = Label(self, textvariable=self.x_label_var, width=15)
        self.y_label_var = StringVar()
        self.y_label = Label(self, textvariable=self.y_label_var, width=15)
        self.field_label_var = StringVar()
        self.field_label = Label(self, textvariable=self.field_label_var, width=30)

        self.x_label.grid(row=0, column=0)
        self.y_label.grid(row=0, column=1)
        self.field_label.grid(row=1, column=0, columnspan=2)

        self.field = field

    def update(self, mov):
        self.x_label_var.set(f"X: {mov.x}")
        self.y_label_var.set(f"Y: {mov.y}")

        f = self.field.get_field(mov.x, mov.y)
        if f:
            f = self.field.distance((0, 0), f)
            f = round(f)
        else:
            f = "NaN"

        self.field_label_var.set(f"Field: {f}")


if __name__ == "__main__":
    Window()
