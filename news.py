from tkinter import *
from PIL import Image, ImageTk
import webbrowser
from webscout import WEBS
import requests
from io import BytesIO
import os

api = input("pls input you newsapi = ")

class NewsApp:
    def __init__(self):
        # initial GUI load
        self.load_gui()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.title('Surya News App')
        self.root.configure(background='black')

        # Create search entry
        self.label = Label(self.root, text="Enter keyword or choose category:", bg='black', fg='yellow')
        self.label.pack()
        self.entry = Entry(self.root, width=50)
        self.entry.pack()

        # Create search button
        search_button = Button(self.root, text="Click to Search", command=self.search_news)
        search_button.pack()

        # Categories
        self.categories_frame = Frame(self.root, bg='black')
        self.categories_frame.pack()

        # Load category images
        category_buttons = []
        categories = ["AI", "Technology", "Entertainment", "Goverment", "General", "War"]
        while categories:
            category_frame = Frame(self.categories_frame, bg='black')
            category_frame.pack(side=TOP, pady=5)

            for _ in range(2):
                if categories:
                    category = categories.pop(0)
                    img_path = f"C:\\Users\\ssrss\\OneDrive\\Desktop\\G.O.A.T\\news\\photos\\{category.lower()}.jpg"
                    if os.path.exists(img_path):
                        img = Image.open(img_path).resize((150, 170))
                        photo = ImageTk.PhotoImage(img)
                        button = Button(category_frame, image=photo, command=lambda cat=category: self.filter_news(cat))
                        button.image = photo
                        button.pack(side=LEFT, padx=5)
                        category_buttons.append(button)

        # Frame to display news items
        self.frame = Frame(self.root, bg='black')
        self.frame.pack(expand=True, fill=BOTH)

        self.root.mainloop()

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def load_news_item(self, index):
        if index >= len(self.data):
            return

        # clear the frame for the new news item
        self.clear()

        # Fetch news item data
        news_item = self.data[index]
        print("News Item:", news_item)  # Debug print

        # Image
        img_url = news_item.get('urlToImage', 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg')
        print("Image URL:", img_url)  # Debug print
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                im = Image.open(img_data).resize((350, 200))
                photo = ImageTk.PhotoImage(im)
            else:
                raise Exception(f"Failed to fetch image: HTTP status code {response.status_code}")
        except Exception as e:
            print(f"Error loading image: {e}")
            img_path = os.path.join(os.path.dirname(__file__), "C:\\Users\\ssrss\\OneDrive\\Desktop\\G.O.A.T\\news\\no_image.jpg")
            im = Image.open(img_path).resize((350, 200))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.frame, image=photo)
        label.image = photo
        label.pack()

        # News title
        title = news_item.get('title', 'No title available')
        heading = Label(self.frame, text=title, bg='black', fg='white', wraplength=350, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        # News body
        body = news_item.get('description', 'No body available')
        body_label = Label(self.frame, text=body, bg='black', fg='white', wraplength=350, justify='left')
        body_label.pack(pady=(2, 20))
        body_label.config(font=('verdana', 10))

        # Button frame
        button_frame = Frame(self.frame, bg='black')
        button_frame.pack(expand=True, fill=BOTH)

        # News source link button
        news_source_url = news_item.get('url', '')
        source_button = Button(button_frame, text="Source", command=lambda: webbrowser.open(news_source_url))
        source_button.pack(side=LEFT, padx=5)

        # News item index update
        if index == len(self.data) - 1:
            index = 0
        else:
            index += 1

        # Next news item button
        next_button = Button(button_frame, text="Next", command=lambda: self.load_news_item(index))
        next_button.pack(side=RIGHT, padx=5)

        # Hide categories frame
        self.categories_frame.pack_forget()
    def fetch_news(self, keyword):
        api_key = (api)
        url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('articles', [])
        else:
            print(f"Error fetching news: {response.status_code}")
            return []

    def filter_news(self, category):
        keyword = category.lower()
        if keyword == '':
            self.clear()
            return

        self.data = self.fetch_news(keyword)
        print("Data:", self.data)  # Debug print

        # Check if data is fetched correctly
        if not self.data:
            print("No news found")
            self.clear()
        else:
            index = 0  # Initialize index to 0
            self.load_news_item(index)

    def search_news(self):
        keyword = self.entry.get()
        if keyword == '':
            self.clear()
            return

        self.data = self.fetch_news(keyword)
        print("Data:", self.data)  # Debug print

        # Check if data is fetched correctly
        if not self.data:
            print("No news found")
            self.clear()
        else:
            index = 0  # Initialize index to 0
            self.load_news_item(index)
            # Hide categories frame
            self.categories_frame.pack_forget()

if __name__ == '__main__':
    news_app = NewsApp()
