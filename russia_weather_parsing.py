import requests
from bs4 import BeautifulSoup
from tkinter import *
import math

class Weather:
    def __init__(self, link="https://rp5.ru/Погода_в_России"):
        self.link = link
        r = requests.get(self.link).text
        self.soup = BeautifulSoup(r, "html.parser")

    def first_parse(self):
        data = self.soup.find_all("div", {'class': 'RuLinks'})
        links = {}
        for tag in data:
            if tag.find_next("b"):
                tag = tag.find_next("a")
                links[tag.get_text()] = "https://rp5.ru" + tag['href']
        return links

    def parse_next(self, link):
        soup = Weather(link).soup
        # Надо попытаться найти погоду
        if soup.find('div', {'id': 'archiveString'}):
            data = soup.find('div', {'id': 'archiveString'})
            temp = data.find_next("span", {'class': 't_0'}).get_text()
            print(temp)
            return temp
        # Погоды нет
        data = soup.find("div", {"class": "countryMap"})
        data = data.find_all("a")
        links = {}
        for tag in data:
            links[tag.get_text()] = "https://rp5.ru" + tag['href']
        return links



class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Погода")

        self.upper_frame = Frame(self.root)
        self.upper_frame.grid(row=0, column=0)

        self.w = Weather()
        one = self.w.first_parse()
        self.set_buttons(one)

        self.lower_frame = Frame(self.root)
        self.lower_frame.grid(row=1, column=0)

        home_btn = Button(self.lower_frame, text="Домой", command=self.home_button_handler)
        home_btn.pack()

    def run(self):
        self.root.mainloop()

    def set_buttons(self, links):
        total_links = len(links)
        columns = math.ceil(total_links / 22)
        # columns = 4
        for i, (name, link) in enumerate(links.items()):
            # print(link)
            row = i // columns
            col = i % columns
            button = Button(self.upper_frame, text=name, command=lambda c=link: self.button_handler(c))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def button_handler(self, c):
        print(type(c))
        self.upper_frame.destroy()
        self.upper_frame = Frame(self.root)
        self.upper_frame.grid(row=0, column=0)
        two = self.w.parse_next(c)
        if isinstance(two, dict):
            self.set_buttons(two)
        else:
            label = Label(self.upper_frame, text=two, font=(None, 22))
            label.pack()
        self.root.update_idletasks()

    def home_button_handler(self):
        self.upper_frame.destroy()
        self.upper_frame = Frame(self.root)
        self.upper_frame.grid(row=0, column=0)

        self.w = Weather()
        one = self.w.first_parse()
        self.set_buttons(one)





if __name__ == '__main__':
    w = Weather()
    ui = UI()
    ui.run()
    print(w.first_parse())
