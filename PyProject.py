import csv
import tkinter as tk
from tkinter import messagebox

class Course:
    def __init__(self,master):
        self.m = master
        self.m.geometry("800x600")
        self.m.configure(bg='#ccd7ed')
        self.ui_setup()

    def ui_setup(self):
        tk.Label(self.m, text='Enter a file path: ', bg='#ccd7ed').grid(row=1, column=1, padx=10, pady=10)
        self.e1 = tk.Entry(self.m)
        self.e1.grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self.m, text='Year: ', bg='#ccd7ed').grid(row=2, column=1, padx=0, pady=10)
        self.years = tk.Spinbox(self.m, from_=1, to=5, width=10, relief="sunken", font=("Arial", 12), bg="lightgrey", fg="blue")
        self.years.grid(row=2, column=2, padx=0, pady=10)

        tk.Label(self.m, text='Department:', bg='#ccd7ed').grid(row=2, column=3, padx=10, pady=10)
        self.e2 = tk.Entry(self.m)
        self.e2.grid(row=2, column=4, padx=10, pady=10)

        tk.Button(self.m, text='Display', width=15, command=self.display).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.m, text='Clear', width=15, command=self.clear).grid(row=3, column=2, padx=10, pady=10)
        tk.Button(self.m, text='Save', width=15, command=self.save).grid(row=3, column=3, padx=10, pady=10)

        tk.Label(self.m, text='Courses: ', bg='#ccd7ed').grid(row=4, column=3, padx=10, pady=10)
        self.listbox_courses = tk.Listbox(self.m, width=40)
        self.listbox_courses.grid(row=5, column=3, padx=10, pady=10)

        tk.Label(self.m, text='Warnings: ', bg='#ccd7ed').grid(row=4, column=1, padx=10, pady=10)
        self.listbox_chosencourses = tk.Listbox(self.m, width=30)
        self.listbox_chosencourses.grid(row=5, column=1, padx=10, pady=10)

        self.listbox_courses.bind("<Double-Button-1>", self.move_course)

    def read_file(self, file):
        file=self.e1.get()
        self.courses = []
        try:
            with open(file, newline='') as csvfile:
                read = csv.reader(csvfile)
                for row in read:
                    self.courses.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
        return self.courses



    def display(self):
        file = self.e1.get()
        courses = self.read_file(file)
        self.listbox_courses.delete(0, tk.END)
        year = self.years.get()
        for course in courses:
            course_dep = course[0].split()[0]
            course_year = course[0].split()
            course_number = course_year[1]
            if self.e2.get() == "" and year == "":
                self.listbox_courses.insert(tk.END, course)
            elif year in course_number[0] and self.e2.get() == "":
                self.listbox_courses.insert(tk.END, course)
            elif self.e2.get() == course_dep and year == "":
                self.listbox_courses.insert(tk.END, course)
            elif self.e2.get() == course_dep and year in course_number[0]:
                self.listbox_courses.insert(tk.END, course)

    def clear(self):
        self.listbox_courses.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.years.delete(0, tk.END)
        self.listbox_chosencourses.delete(0, tk.END)

    def save(self):
        with open("C:\\Users\\ccc\\Desktop\\timetable.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for course in self.listbox_chosencourses.get(0, tk.END):
                writer.writerow([course])

    def move_course(self, event):
        course = self.listbox_courses.get(tk.ACTIVE)
        course_days = course[2].split()
        course_times = course[3].split()

        if self.listbox_chosencourses.size() < 6:
            if course in self.listbox_chosencourses.get(0, tk.END):
                messagebox.showerror("ERROR", "You've already chosen " + course[0])
            else:
                conflict = False
                for chosen_course in self.listbox_chosencourses.get(0, tk.END):
                    chosen_course_full = next(c for c in self.read_file(self.e1.get()) if c[0] == chosen_course)
                    chosen_course_days = chosen_course_full[2].split()
                    chosen_course_times = chosen_course_full[3].split()
                    if self.day_overlap(course_days, chosen_course_days) and self.time_overlap(course_times,chosen_course_times):
                        conflict = True
                        messagebox.showerror("ERROR", "You can't choose this course due to schedule conflict: " + course[0])
                        break
                if not conflict:
                    self.listbox_chosencourses.insert(tk.END, course[0])
        else:
            messagebox.showerror("ERROR", "You can't choose more than 6 courses per semester")

    def time_overlap(self, times1, times2):
        def to_minutes(time_str):
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes

        for time1 in times1:
            start1, end1 = time1.split('-')
            start1, end1 = to_minutes(start1), to_minutes(end1)
            for time2 in times2:
                start2, end2 = time2.split('-')
                start2, end2 = to_minutes(start2), to_minutes(end2)
                if max(start1, start2) < min(end1, end2):
                    return True
        return False

    def day_overlap(self, days1, days2):
        return any(day in days2 for day in days1)


def main():
    korniza = tk.Tk()
    app = Course(korniza)
    korniza.mainloop()

if __name__ == "__main__":
    main()