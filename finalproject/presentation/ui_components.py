import customtkinter
import datetime


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, window):
        super().__init__(master=window, fg_color="#0d0d0d", corner_radius=20)
        self.window = window

        self.elastic()

        self.dashboard_item = self.navigation_item(
            "Dashboard", 0, self.window.dashboard
        )
        self.transaction_item = self.navigation_item(
            "Transaction", 1, self.window.transaction
        )
        self.history_item = self.navigation_item("History", 2, self.window.history)

        self.navigate(self.dashboard_item, self.window.dashboard)

    def elastic(self):
        self.grid_columnconfigure(index=0, weight=1)

    def navigation_item(self, text, index, active_frame):
        navigation_item = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            text=text,
            text_color="#fbfbfb",
            hover=False,
            font=("Roboto Medium", 15),
        )
        navigation_item.bind(
            "<Button-1>", lambda event: self.navigate(navigation_item, active_frame)
        )
        navigation_item.grid(row=index)
        return navigation_item

    def navigate(self, active_button, active_frame):
        # Highlight item
        for button in self.winfo_children():
            if button is active_button:
                button.configure(text_color="#0ec35f")
            else:
                button.configure(text_color="#fbfbfb")

        # Show content
        for child in self.window.winfo_children():
            if not isinstance(child, Sidebar):
                if child is active_frame:
                    child.grid(row=0, column=1, sticky="news", padx=10, pady=10)
                else:
                    child.grid_forget()


class Dashboard(customtkinter.CTkFrame):
    def __init__(self, window, controller):
        super().__init__(master=window, fg_color="#0d0d0d", corner_radius=20)


class Transaction(customtkinter.CTkFrame):
    def __init__(self, window, controller):
        super().__init__(master=window, fg_color="#0d0d0d", corner_radius=20)
        self.controller = controller

        self.elastic()

        # Label
        self.create_label("Add Transaction", 0, 20)
        self.create_label("Type", 1, 16)
        self.create_label("Amount", 2, 16)
        self.create_label("Date and time", 3, 16)
        self.create_label("Category", 4, 16)
        self.create_label("Note", 5, 16)

        # Entry
        self.type = self.create_segmentbutton(["Income", "Expense"], 1)
        self.amount = self.create_entry_box("VND", 2)
        self.date_time = self.create_entry_box(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3
        )
        self.category = self.create_optionmenu(controller.get_categories(), 4)
        self.note = self.create_entry_box("optional", 5)

        # Save button
        self.create_save_button(6)

    def elastic(self):
        self.grid_rowconfigure(index=1, weight=27)
        for i in range(2, 6):
            self.grid_rowconfigure(index=i, weight=27)
        self.grid_rowconfigure(index=6, weight=48)

        self.grid_columnconfigure(index=0, weight=18)
        self.grid_columnconfigure(index=1, weight=65)

    def create_save_button(self, row):
        def save():
            try:
                self.controller.save_transaction(
                    type=self.type,
                    amount=self.amount,
                    date_time=self.date_time,
                    category=self.category,
                    note=self.note,
                )
            except Exception:
                button_content = customtkinter.StringVar("Invalid input")
                self.after(1000, lambda: button_content.set("Save Transaction"))

        button_content = None
        save_button = customtkinter.CTkButton(
            master=self,
            height=47,
            corner_radius=12,
            fg_color="#4f84f6",
            text_color="#eaeeef",
            text="Save Transaction",
            font=("Roboto Medium", 20),
            textvariable=button_content,
            command=save,
        )

        save_button.grid(row=row, column=0, columnspan=2)

    def create_label(self, text, row, font_size):
        label = customtkinter.CTkLabel(
            master=self,
            text=text,
            text_color="#f9f9f9",
            font=("Roboto Medium", font_size),
        )
        label.grid(row=row, column=0, sticky="news", padx=(15, 0))

    def create_entry_box(self, placeholder_text, row):
        user_input = None
        entry_box = customtkinter.CTkEntry(
            master=self,
            textvariable=user_input,
            height=47,
            corner_radius=12,
            fg_color="#2d3041",
            text_color="#d2d3d9",
            placeholder_text_color="#8c90a4",
            placeholder_text=placeholder_text,
            font=("Roboto Medium", 16),
        )
        entry_box.grid(row=row, column=1, sticky="we")
        return user_input

    def create_optionmenu(self, menu_list, row):
        user_input = None
        optionmenu = customtkinter.CTkOptionMenu(
            master=self,
            height=47,
            corner_radius=12,
            fg_color="#2d3041",
            button_color="#2d3041",
            dropdown_fg_color="#2d3041",
            text_color="#d2d3d9",
            font=("Roboto Medium", 16),
            dropdown_font=("Roboto Medium", 16),
            hover=False,
            values=menu_list,
            variable=user_input,
        )
        optionmenu.grid(row=row, column=1, sticky="we")
        return user_input

    def create_segmentbutton(self, menu_list, row):
        user_input = None
        segmentedbutton = customtkinter.CTkSegmentedButton(
            master=self,
            width=60,
            height=42,
            corner_radius=17,
            border_width=3,
            selected_color="#527ff5",
            selected_hover_color="#527ff5",
            unselected_color="#2c2f40",
            unselected_hover_color="#2c2f40",
            text_color="#b8ceef",
            font=("Roboto Medium", 16),
            values=menu_list,
            variable=user_input,
        )
        segmentedbutton.grid(row=row, column=1, sticky="we")
        return user_input


class History(customtkinter.CTkFrame):
    def __init__(self, window, controller):
        super().__init__(master=window, fg_color="#0d0d0d", corner_radius=20)


class MainWindow(customtkinter.CTk):
    def __init__(self, controller):
        self.new_window()
        self.elastic()
        self.content_area(controller)
        self.sidebar()

    def new_window(self):
        super().__init__(fg_color="#1b1b1b")
        self.geometry("683x384")
        self.title("Personal Finance Manager")

    def elastic(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=4)

    def content_area(self, controller):
        self.dashboard = Dashboard(self, controller)
        self.transaction = Dashboard(self, controller)
        self.history = Dashboard(self, controller)

    def sidebar(self):
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
