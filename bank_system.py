# from customer_account import CustomerAccount
# from admin import Admin
from tkinter import Label, Frame, Entry, Tk, Button, ttk, StringVar, Canvas, messagebox, Radiobutton
from tkinter.filedialog import askopenfilename, asksaveasfilename
from csv import writer


accounts_list = []
admins_list = []

root = Tk


class BankingSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []

        # Tree Styling
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading",
                        background='orange', foreground='black')
        # ====== Variables =============
        self.customer_dictionary = []
        self.admin_dictionary = []
        self.username = StringVar()
        self.password = StringVar()
        self.filename_to_export = StringVar()
        self.filename_to_export_report = StringVar()
        self.transaction_funds = StringVar()
        self.search_string = StringVar()
        self.search_parameter = StringVar()
        self.CURRENTLY_LOGGED_IN_ADMIN = {}
        # ============= INTRO UI =================
        self.introductory_frame = Frame(width=1300, height=700, bg='#000')
        self.introductory_frame.place(x=0, y=0)
        self.introductory_text = Label(self.introductory_frame, bg="#000", fg="#fff", font=(
            "Times New Roman", 48), text='Python Banking System', justify='center')
        self.introductory_text.place(relx=0.5, rely=0.47, anchor='center')
        Button(self.introductory_frame, text="Start", font=("Times New Roman", 18), width=30,
               command=self.show_login_page, bg='orange', fg="#000", bd=3).place(relx=0.5, rely=0.6, anchor='center')

        self.load_bank_data()

    def on_mouse_wheel(self, event):
        self.functionalities_canvas.yview_scroll(
            int(-1 * (event.delta / 120)), "units")

    def show_single_frame(self, frame):
        # color the button accordingly
        all_buttons = self.scrollable_frame.winfo_children()
        for btn in all_buttons:
            if btn.winfo_name() == frame:
                btn.configure(bg='orange', fg='#000')
            else:
                btn.configure(bg='#fff', fg='gray')

        # hide all other frames that have been instantiated
        if hasattr(self, 'empty_frame'):
            self.empty_frame.place_forget()
        if hasattr(self, 'update_admin_frame'):
            self.update_admin_frame.place_forget()
        if hasattr(self, 'all_customer_frame'):
            self.all_customer_frame.place_forget()
        if hasattr(self, 'search_for_customer_frame'):
            self.search_for_customer_frame.place_forget()
        if hasattr(self, 'import_data_frame'):
            self.import_data_frame.place_forget()
        if hasattr(self, 'export_data_frame'):
            self.export_data_frame.place_forget()
        if hasattr(self, 'request_report_frame'):
            self.request_report_frame.place_forget()
        if hasattr(self, 'transfer_funds_frame'):
            self.transfer_funds_frame.place_forget()
        if hasattr(self, 'withdraw_funds_frame'):
            self.withdraw_funds_frame.place_forget()
        if hasattr(self, 'deposit_funds_frame'):
            self.deposit_funds_frame.place_forget()

        # show the appropriate frames
        if frame == 'show_all_customer':
            self.show_all_customer_frame()
        elif frame == 'search':
            self.show_search_customer_frame()
        elif frame == 'import':
            self.show_import_data_frame()
        elif frame == 'export':
            self.show_export_data_frame()
        elif frame == 'management_report':
            self.show_request_report_frame()
        elif frame == 'transfer':
            self.show_transfer_funds_frame()
        elif frame == 'deposit':
            self.show_deposit_funds_frame()
        elif frame == 'withdraw':
            self.show_withdraw_funds_frame()
        elif frame == 'update_admin':
            self.show_update_admin_frame()

    def hide_single_frame(self, frame):
        # hide the appropriate frames
        if frame == 'hide_single_customer_detail':
            self.single_customer_frame.place_forget()
        elif frame == 'hide_update_customer':
            self.update_customer_frame.place_forget()

    def show_deposit_funds_frame(self):
        """ Shows the transfer funds section """

        self.deposit_funds_frame = Frame(width=800, height=500, bg='#000')
        self.deposit_funds_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.deposit_funds_frame, text=5*" " + "Deposit Money" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.3, anchor='center')

        self.deposit_inner_frame = Frame(
            self.deposit_funds_frame, width=600, height=200, bg='#000', bd=3, relief="groove")
        self.deposit_inner_frame.place(relx=0.5, rely=0.58, anchor='center')

        self.customer_list = [i['fname'] + " " + i['lname']
                              for i in self.customer_dictionary]
        self.customer_to_deposit_to = ttk.Combobox(self.deposit_inner_frame, font=(
            "Times New Roman", 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_to_deposit_to.current(0)
        self.customer_to_deposit_to.place(
            relx=0.5, rely=0.2, anchor='center')

        self.fund_entry = Entry(self.deposit_inner_frame, textvariable=self.transaction_funds, font=(
            "Times New Roman", 24), bg='#dadada', width=7, justify='center', fg='#000')
        self.fund_entry.place(relx=0.5, rely=0.48, anchor='center')

        Button(self.deposit_inner_frame, text="Deposit", font=("Times New Roman", 16), width=20,
               command=self.deposit_funds, bg='orange', fg="#000").place(relx=0.5, rely=0.78, anchor='center')

    def show_withdraw_funds_frame(self):
        """ Shows the transfer funds section """

        self.withdraw_funds_frame = Frame(width=800, height=500, bg='#000')
        self.withdraw_funds_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.withdraw_funds_frame, text=5*" " + "Withdraw Money" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.3, anchor='center')

        self.withdraw_inner_frame = Frame(
            self.withdraw_funds_frame, width=600, height=200, bg='#000', bd=3, relief="groove")
        self.withdraw_inner_frame.place(relx=0.5, rely=0.58, anchor='center')

        self.customer_list = [i['fname'] + " " + i['lname']
                              for i in self.customer_dictionary]
        self.customer_to_withdraw_from = ttk.Combobox(self.withdraw_inner_frame, font=(
            "Times New Roman", 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_to_withdraw_from.current(0)
        self.customer_to_withdraw_from.place(
            relx=0.5, rely=0.2, anchor='center')

        self.fund_entry = Entry(self.withdraw_inner_frame, textvariable=self.transaction_funds, font=(
            "Times New Roman", 24), bg='#dadada', width=7, justify='center', fg='#000')
        self.fund_entry.place(relx=0.5, rely=0.48, anchor='center')

        Button(self.withdraw_inner_frame, text="Withdraw", font=("Times New Roman", 16), width=20,
               command=self.withdraw_funds, bg='orange', fg="#000").place(relx=0.5, rely=0.78, anchor='center')

    def withdraw_funds(self):
        withdraw_customer = self.customer_to_withdraw_from.get()
        fund_entry = self.fund_entry.get()

        try:
            fund_entry = int(fund_entry)
            if withdraw_customer not in self.customer_list:
                messagebox.showerror("Money Withdrawal Status",
                                     "Please select a valid customer!")
            else:
                first_name, last_name = withdraw_customer.split(" ")
                customer = [i for i in self.customer_dictionary if i['fname'] ==
                            first_name and i['lname'] == last_name][0]
                customer['balance'] = str(
                    int(customer['balance']) - fund_entry)
                messagebox.showinfo("Money Withdrawal Status",
                                    "Money withdrawal is successful!")
                self.withdraw_funds_frame.place_forget()
                self.transaction_funds.set("")
                self.show_admin_dashboard()
        except ValueError:
            messagebox.showerror("Money Withdrawal Status",
                                 "Please enter a number!")

    def deposit_funds(self):
        deposit_customer = self.customer_to_deposit_to.get()
        fund_entry = self.fund_entry.get()

        try:
            fund_entry = int(fund_entry)
            if deposit_customer not in self.customer_list:
                messagebox.showerror("Money Deposit Status",
                                     "Please select a valid customer!")
            else:
                first_name, last_name = deposit_customer.split(" ")
                customer = [i for i in self.customer_dictionary if i['fname'] ==
                            first_name and i['lname'] == last_name][0]
                customer['balance'] = str(
                    int(customer['balance']) + fund_entry)
                messagebox.showinfo("Money Deposit Status",
                                    "Money deposit is successful!")
                self.deposit_funds_frame.place_forget()
                self.transaction_funds.set("")
                self.show_admin_dashboard()
        except ValueError:
            messagebox.showerror("Money Deposit Status",
                                 "Please enter a number!")

    def show_search_customer_frame(self):
        """ Shows search form, parameters and results """

        self.search_for_customer_frame = Frame(
            self.dashboard_frame, width=1000, height=650, bg='#000')
        self.search_for_customer_frame.place(
            relx=0.6, rely=0.6, anchor='center')
        Label(self.search_for_customer_frame, text=5*" " + "Search customer" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.12, anchor='center')

        self.user_search_entry = Entry(
            self.search_for_customer_frame, textvariable=self.search_string, font=("Times New Roman", 18), bg='#dadada', width=23, fg='#000')
        self.user_search_entry.place(relx=0.04, rely=0.3, anchor='w')
        self.name_checkbutton = Radiobutton(self.search_for_customer_frame, text='Name (First or Last)', font=(
            "Times New Roman", 14), fg='orange', bg='#000', activebackground='#000', variable=self.search_parameter, value="name")
        self.name_checkbutton.place(relx=0.04, rely=0.4, anchor='w')
        self.address_checkbutton = Radiobutton(self.search_for_customer_frame, text='Address', font=(
            "Times New Roman", 14), fg='orange', bg='#000', activebackground='#000', variable=self.search_parameter, value="address")
        self.address_checkbutton.place(relx=0.04, rely=0.5, anchor='w')
        self.balance_checkbutton = Radiobutton(self.search_for_customer_frame, text='Balance', font=(
            "Times New Roman", 14), fg='orange', bg='#000', activebackground='#000', variable=self.search_parameter, value="balance")
        self.balance_checkbutton.place(relx=0.19, rely=0.5, anchor='w')
        self.account_no_checkbutton = Radiobutton(self.search_for_customer_frame, text='Account No.', font=(
            "Times New Roman", 14), fg='orange', bg='#000', activebackground='#000', variable=self.search_parameter, value="account_no")
        self.account_no_checkbutton.place(relx=0.04, rely=0.6, anchor='w')
        self.account_type_checkbutton = Radiobutton(self.search_for_customer_frame, text='Account Type', font=(
            "Times New Roman", 14), fg='orange', bg='#000', activebackground='#000', variable=self.search_parameter, value="account_type")
        self.account_type_checkbutton.place(relx=0.19, rely=0.6, anchor='w')
        Button(self.search_for_customer_frame, text="Search", font=("Times New Roman", 16), width=23,
               bg='orange', fg="#000", command=self.search_for_customer).place(relx=0.04, rely=0.7, anchor='w')

        self.search_customer_tree_frame = Frame(
            self.search_for_customer_frame, width=640, height=410, bg="#1a1a1a", bd=3, relief='groove')
        self.search_customer_tree_frame.place(
            relx=0.68, rely=0.5, anchor='center')
        tree_columns = "full_name", "account_no", "balance"
        self.search_customer_tree = ttk.Treeview(
            self.search_customer_tree_frame, columns=tree_columns, show='headings', height=18, selectmode='browse')
        # centralize all columns
        for i in tree_columns:
            self.search_customer_tree.column(i, anchor='center')
        self.search_customer_tree.place(relx=0.49, rely=0.5, anchor='center')

        # add a scrollbar to the tree
        y_scrollbar = ttk.Scrollbar(
            self.search_customer_tree_frame, orient='vertical', command=self.search_customer_tree.yview)
        self.search_customer_tree.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.place(relx=0.995, rely=0.5, anchor='e', height=390)

        # Tree headings
        self.search_customer_tree.heading(
            "full_name", text="Fullname", anchor='center')
        self.search_customer_tree.heading(
            "account_no", text="Account No.", anchor='center')
        self.search_customer_tree.heading(
            "balance", text="Balance", anchor='center')

        Button(self.search_for_customer_frame, text="View Customer", font=("Times New Roman", 16), width=15,
               command=lambda: self.view_customer("search_tree"), bg='orange', fg="#000").place(relx=0.48, rely=0.87, anchor='center')
        Button(self.search_for_customer_frame, text="Edit Customer", font=("Times New Roman", 16), width=15,
               command=lambda: self.update_customer("search_tree"), bg='orange', fg="#000").place(relx=0.68, rely=0.87, anchor='center')
        Button(self.search_for_customer_frame, text="Close Account", font=("Times New Roman", 16), width=15,
               command=lambda: self.close_account("search_tree"), bg='orange', fg="#000").place(relx=0.88, rely=0.87, anchor='center')

    def show_login_page(self):
        """ Shows the login page """

        self.introductory_frame.place_forget()
        # ============= LOGIN UI =================
        self.login_frame = Frame(width=1300, height=700, bg='#000')
        self.login_frame.place(x=0, y=0)
        self.login_inner_frame = Frame(
            self.login_frame, width=450, height=350, bg='#000', bd=0, relief='groove')
        self.login_inner_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.login_text = Label(self.login_inner_frame, bg="#000", fg="#fff", font=(
            "Times New Roman", 36), text='Admin Login', justify='center')
        self.login_text.place(relx=0.5, rely=0.13, anchor='center')
        Label(self.login_inner_frame, text='Username', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.15, rely=0.3, anchor='w')
        self.username_entry = Entry(self.login_inner_frame, textvariable=self.username, font=("Times New Roman", 18), bg='#dadada',
                                    width=25, fg='#000')
        self.username_entry.place(relx=0.15, rely=0.41, anchor='w')
        Label(self.login_inner_frame, text='Password', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.15, rely=0.55, anchor='w')
        self.password_entry = Entry(self.login_inner_frame, textvariable=self.password, font=("Times New Roman", 18), show='*', bg='#dadada',
                                    width=25, fg='#000')
        self.password_entry.place(relx=0.15, rely=0.66, anchor='w')
        self.password_entry.bind(
            '<Return>', lambda dummy=0: self.login_the_admin())
        Button(self.login_inner_frame, text="Log in", font=("Times New Roman", 16), width=20,
               command=self.login_the_admin, bg='orange', fg="#000", bd=3).place(relx=0.5, rely=0.85, anchor='center')

    def show_admin_dashboard(self):
        """ Shows the admin dashboard """

        # ============= DASHBOARD UI =================
        self.dashboard_frame = Frame(width=1300, height=700, bg='#000')
        self.dashboard_frame.place(x=0, y=0)

        Label(self.dashboard_frame, text=32*" " + "Admin Dashboard" + 32*" ", fg='orange', bg="#000", relief='groove',
              font=("Times New Roman", 36)).place(relx=0.5, rely=0.08, anchor='center')

        self.scrollable_functionalities_frame = Frame(
            width=250, height=520, bd=4, relief='groove')
        self.scrollable_functionalities_frame.place(
            relx=0.135, rely=0.2, anchor="n")

        self.functionalities_canvas = Canvas(
            self.scrollable_functionalities_frame, width=218, height=505)
        scrollbar = ttk.Scrollbar(
            self.scrollable_functionalities_frame, orient='vertical', command=self.functionalities_canvas.yview)
        self.scrollable_frame = Frame(
            self.functionalities_canvas, width=225, bg='green')
        self.scrollable_frame.bind("<Configure>", lambda e: self.functionalities_canvas.configure(
            scrollregion=self.functionalities_canvas.bbox('all')))
        self.scrollable_frame.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.functionalities_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor='nw')
        self.functionalities_canvas.configure(yscrollcommand=scrollbar.set)

        self.functionalities_canvas.place(x=0, y=0)
        scrollbar.place(relx=0.95, rely=0.5, anchor='center', height=490)

        self.empty_frame = Frame(
            width=800, height=520, bd=5, bg="#000", relief='groove')
        self.empty_frame.place(relx=0.6, rely=0.57, anchor='center')

        Button(self.scrollable_frame, text="Show all\ncustomers", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="show_all_customer", command=lambda dummy=0: self.show_single_frame("show_all_customer")).grid(row=0, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Search\ncustomer", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="search", command=lambda dummy=0: self.show_single_frame("search")).grid(row=1, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Deposit\nmoney", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="deposit", command=lambda dummy=0: self.show_single_frame("deposit")).grid(row=2, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Withdraw\nmoney", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="withdraw", command=lambda dummy=0: self.show_single_frame("withdraw")).grid(row=3, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Transfer\nfunds", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="transfer", command=lambda dummy=0: self.show_single_frame("transfer")).grid(row=4, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Import\ncustomer data", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="import", command=lambda dummy=0: self.show_single_frame("import")).grid(row=5, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Export\ncustomer data", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="export", command=lambda dummy=0: self.show_single_frame("export")).grid(row=6, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Request\nmanagement report", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', name="management_report", command=lambda dummy=0: self.show_single_frame("management_report")).grid(row=7, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, width=16, text="Update\nadmin details", font=(
            'Times New Roman bold', 14), bg='#fff', fg='gray', name="update_admin", command=lambda dummy=0: self.show_single_frame("update_admin")).grid(row=8, column=0, pady=15, padx=23)
        Button(self.scrollable_frame, text="Logout", width=16, font=(
            "Times New Roman bold", 14), bg='#fff', fg='gray', command=self.logout_admin).grid(row=9, column=0, pady=15, padx=23)

    def show_update_admin_frame(self):
        """ Shows the update admin section """

        admin_details = self.CURRENTLY_LOGGED_IN_ADMIN
        self.update_admin_frame = Frame(
            self.dashboard_frame, width=1000, height=500, bg='#000')
        self.update_admin_frame.place(relx=0.6, rely=0.5, anchor='center')
        Label(self.update_admin_frame, text=5*" " + "Update admin details" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 28)).place(relx=0.5, rely=0.28, anchor='center')

        self.admin_edit_frame = Frame(
            self.update_admin_frame, width=600, height=270, bg="#000", bd=3, relief='groove')
        self.admin_edit_frame.place(relx=0.5, rely=0.63, anchor='center')

        Label(self.admin_edit_frame, text='First name', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.1, rely=0.12, anchor='w')
        self.admin_first_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.admin_first_name.insert(0, admin_details["fname"])
        self.admin_first_name.place(relx=0.1, rely=0.27, anchor='w')
        # customer last name
        Label(self.admin_edit_frame, text='Last name', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.55, rely=0.12, anchor='w')
        self.admin_last_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.admin_last_name.insert(0, admin_details["lname"])
        self.admin_last_name.place(relx=0.55, rely=0.27, anchor='w')
        # customer user name
        Label(self.admin_edit_frame, text='Username', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.1, rely=0.45, anchor='w')
        self.admin_user_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.admin_user_name.insert(0, admin_details["user_name"])
        self.admin_user_name.place(relx=0.1, rely=0.6, anchor='w')
        # customer address
        Label(self.admin_edit_frame, text='Address', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.55, rely=0.45, anchor='w')
        self.admin_address = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.admin_address.insert(0, admin_details["address"])
        self.admin_address.place(relx=0.55, rely=0.6, anchor='w')

        Button(self.admin_edit_frame, text="Update details", font=("Times New Roman", 16), width=35,
               command=self.update_admin_details, bg='orange', fg="#000").place(relx=0.5, rely=0.85, anchor='center')

    def show_import_data_frame(self):
        """ Shows the import data section """

        self.import_data_frame = Frame(
            self.dashboard_frame, width=1000, height=500, bg='#000')
        self.import_data_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.import_data_frame, text=5*" " + "Import customer data" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.21, anchor='center')

        Label(self.import_data_frame, text="How to Import:\nPress the 'Click here to select .csv file...' below\nSelect an excel (.csv) file.\nClick on the load button.",
              bg="#000", fg="orange", font=("Times New Roman", 18)).place(relx=0.5, rely=0.39, anchor='center')

        Button(self.import_data_frame, text="Click here to select .csv file...", font=("Times New Roman", 16), bg="#000", fg="#fff",
               width=30, relief="groove", command=self.show_import_dialog).place(relx=0.5, rely=0.6, anchor='center')

        self._file = ""
        self.file_selected = Label(
            self.import_data_frame, bg="#000", fg='#fff', font=("Times New Roman", 16))
        self.file_selected.place(relx=0.5, rely=0.68, anchor='center')
        self.import_data_button = Button(self.import_data_frame, text="Load Customer Data", font=("Times New Roman", 16), width=20,
                                         command=self.import_data, bg='orange', fg="#000")

    def show_export_data_frame(self):
        """ Shows the export data section """

        self.export_data_frame = Frame(
            self.dashboard_frame, width=1000, height=500, bg='#000')
        self.export_data_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.export_data_frame, text=5*" " + "Export customer data" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.2, anchor='center')

        Label(self.export_data_frame, text="How to Export:\nPress the 'Click here to select save location' below\nSelect a location and input the filename you want the file to be in.\nClick on the export button.",
              bg="#000", fg="orange", font=("Times New Roman", 18)).place(relx=0.5, rely=0.4, anchor='center')

        Button(self.export_data_frame, text="Click here to select save location", font=("Times New Roman", 16), bg="#000", fg="#fff",
               width=30, relief="groove", command=self.show_export_dialog).place(relx=0.5, rely=0.6, anchor='center')
        self._export_location = ""

        self.export_location_selected = Label(
            self.export_data_frame, text="", bg="#000", fg='#fff', font=("Times New Roman", 16))
        self.export_location_selected.place(
            relx=0.5, rely=0.69, anchor='center')

        self.export_data_button = Button(self.export_data_frame, text="Export Customer Data", font=("Times New Roman", 16), width=20,
                                         command=self.export_data, bg='orange', fg="#000")

    def show_request_report_frame(self):
        """ Shows the request management report section """

        self.request_report_frame = Frame(width=900, height=500, bg='#000')
        self.request_report_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.request_report_frame, text=5*" " + "Request management report" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 28)).place(relx=0.5, rely=0.2, anchor='center')

        Label(self.request_report_frame, text="How to Export:\nPress the 'Click here to select save location' below\nSelect a location and input the filename you want the file to be in.\nClick on the export button.",
              bg="#000", fg="orange", font=("Times New Roman", 18)).place(relx=0.5, rely=0.4, anchor='center')

        Button(self.request_report_frame, text="Click here to select save location", font=("Times New Roman", 16), bg="#000", fg="#fff",
               width=30, relief="groove", command=self.show_report_dialog).place(relx=0.5, rely=0.6, anchor='center')
        self._report_save_location = ""

        self.save_location_selected = Label(
            self.request_report_frame, text="", bg="#000", fg='#fff', font=("Times New Roman", 16))
        self.save_location_selected.place(relx=0.5, rely=0.69, anchor='center')

        self.export_management_button = Button(self.request_report_frame, text="Export Management Report", font=("Times New Roman", 16), width=25,
                                               command=self.export_report_data, bg='orange', fg="#000")

    def show_transfer_funds_frame(self):
        """ Shows the transfer funds section """

        self.transfer_funds_frame = Frame(width=800, height=500, bg='#000')
        self.transfer_funds_frame.place(relx=0.6, rely=0.55, anchor='center')

        Label(self.transfer_funds_frame, text=5*" " + "Transfer funds" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.3, anchor='center')

        self.transfer_inner_frame = Frame(
            self.transfer_funds_frame, width=600, height=200, bg='#000', bd=3, relief="groove")
        self.transfer_inner_frame.place(relx=0.5, rely=0.58, anchor='center')

        self.customer_list = [i['fname'] + " " + i['lname']
                              for i in self.customer_dictionary]
        self.customer_from = ttk.Combobox(self.transfer_inner_frame, font=(
            "Times New Roman", 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_from.current(0)
        self.customer_from.place(relx=0.25, rely=0.2, anchor='center')

        Label(self.transfer_inner_frame, text=' to ', font=("Times New Roman", 16),
              fg='#000', bg='orange').place(relx=0.5, rely=0.2, anchor='center')

        self.customer_to = ttk.Combobox(self.transfer_inner_frame, font=(
            "Times New Roman", 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_to.current(0)
        self.customer_to.place(relx=0.75, rely=0.2, anchor='center')

        self.fund_entry = Entry(self.transfer_inner_frame, textvariable=self.transaction_funds, font=(
            "Times New Roman", 24), bg='#dadada', width=7, justify='center', fg='#000')
        self.fund_entry.place(relx=0.5, rely=0.48, anchor='center')

        Button(self.transfer_inner_frame, text="Tranfer funds", font=("Times New Roman", 16), width=20,
               command=self.transfer_funds, bg='orange', fg="#000").place(relx=0.5, rely=0.78, anchor='center')

    def show_all_customer_frame(self):
        """ Shows all the customers in the bank """

        self.all_customer_frame = Frame(
            self.dashboard_frame, width=1000, height=600, bg='#000')
        self.all_customer_frame.place(relx=0.6, rely=0.6, anchor='center')
        Label(self.all_customer_frame, text=5*" " + "All Customers" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 24)).place(relx=0.5, rely=0.08, anchor='center')

        self.customers_tree_frame = Frame(
            self.all_customer_frame, width=850, height=410, bg="#000", bd=3, relief='groove')
        self.customers_tree_frame.place(relx=0.5, rely=0.48, anchor='center')
        tree_columns = "first_name", "last_name", "account_no", "balance"
        self.all_customer_tree = ttk.Treeview(
            self.customers_tree_frame, columns=tree_columns, show='headings', height=18, selectmode='browse')
        # centralize all columns
        for i in tree_columns:
            self.all_customer_tree.column(i, anchor='center')
        self.all_customer_tree.place(relx=0.49, rely=0.5, anchor='center')

        # add a scrollbar to the tree
        y_scrollbar = ttk.Scrollbar(
            self.customers_tree_frame, orient='vertical', command=self.all_customer_tree.yview)
        self.all_customer_tree.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.place(relx=0.995, rely=0.5, anchor='e', height=390)
        self.load_all_customer_tree()

        Button(self.all_customer_frame, text="View Customer", font=("Times New Roman", 16), width=20,
               command=lambda: self.view_customer("all_customer"), bg='orange', fg="#000").place(relx=0.2, rely=0.89, anchor='center')
        Button(self.all_customer_frame, text="Edit Customer", font=("Times New Roman", 16), width=20,
               command=lambda: self.update_customer("all_customer"), bg='orange', fg="#000").place(relx=0.5, rely=0.89, anchor='center')
        Button(self.all_customer_frame, text="Close Account", font=("Times New Roman", 16), width=20,
               command=lambda: self.close_account("all_customer"), bg='orange', fg="#000").place(relx=0.8, rely=0.89, anchor='center')

    def show_single_customer_frame(self, values):
        """ Shows single customer section """

        customer_details = [
            i for i in self.customer_dictionary if i['account_no'] == str(values[2])][0]
        the_full_name = customer_details["fname"] + \
            " " + customer_details["lname"]

        self.single_customer_frame = Frame(
            width=1300, height=700, bg='#000')
        self.single_customer_frame.place(x=0, y=0)
        if values[-1] == "all_customer":
            Button(self.single_customer_frame, text='⬅', font=("Times New Roman", 16), fg='#000', bg='orange',
                   width=3, command=lambda dummy=0: self.hide_single_frame("hide_single_customer_detail")).place(x=60, y=30)
        else:
            Button(self.single_customer_frame, text='⬅', font=("Times New Roman", 16), fg='#000', bg='orange',
                   width=3, command=lambda dummy=0: self.hide_single_frame("hide_single_customer_detail")).place(x=60, y=30)
        Label(self.single_customer_frame, text=5*" " + "Single Customer Details" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 28)).place(relx=0.5, rely=0.33, anchor='center')

        self.details_frame = Frame(
            self.single_customer_frame, width=750, height=250, bg="#000", bd=3, relief='groove')
        self.details_frame.place(relx=0.5, rely=0.57, anchor='center')

        # customer name
        Label(self.details_frame, text="Name:", font=(
            "Times New Roman", 18), fg='orange', bg='#000').place(relx=0.1, rely=0.15, anchor='w')
        full_name = Label(self.details_frame, text=the_full_name, font=(
            "Times New Roman", 18), fg='#fff', bg='#000')
        full_name.place(relx=0.2, rely=0.15, anchor='w')
        # customer account number
        Label(self.details_frame, text="Account No.:", font=(
            "Times New Roman", 18), fg='orange', bg='#000').place(relx=0.1, rely=0.33, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["account_no"], font=(
            "Times New Roman", 18), fg='#fff', bg='#000')
        full_name.place(relx=0.28, rely=0.33, anchor='w')
        # customer account type
        Label(self.details_frame, text="Account Type:", font=(
            "Times New Roman", 18), fg='orange', bg='#000').place(relx=0.1, rely=0.49, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["account_type"], font=(
            "Times New Roman", 18), fg='#fff', bg='#000')
        full_name.place(relx=0.3, rely=0.49, anchor='w')
        # customer balance
        Label(self.details_frame, text="Account Balance:", font=(
            "Times New Roman", 18), fg='orange', bg='#000').place(relx=0.1, rely=0.67, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["balance"], font=(
            "Times New Roman", 18), fg='#fff', bg='#000')
        full_name.place(relx=0.34, rely=0.67, anchor='w')
        # customer address
        Label(self.details_frame, text="Address:", font=(
            "Times New Roman", 18), fg='orange', bg='#000').place(relx=0.1, rely=0.85, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["address"], font=(
            "Times New Roman", 18), fg='#fff', bg='#000')
        full_name.place(relx=0.225, rely=0.85, anchor='w')

    def show_update_customer_frame(self, values):
        """ Shows update customer section """

        customer_details = [
            i for i in self.customer_dictionary if i['account_no'] == str(values[2])][0]
        the_account_type = customer_details["account_type"]

        self.update_customer_frame = Frame(
            width=1300, height=700, bg='#000')
        self.update_customer_frame.place(x=0, y=0)
        if values[-1] == "all_customer":
            Button(self.update_customer_frame, text='⬅', font=("Times New Roman", 16), fg='#000', bg='orange',
                   width=3, command=lambda dummy=0: self.hide_single_frame("hide_update_customer")).place(x=60, y=30)
        else:
            Button(self.update_customer_frame, text='⬅', font=("Times New Roman", 16), fg='#000', bg='orange',
                   width=3, command=lambda dummy=0: self.hide_single_frame("hide_update_customer")).place(x=60, y=30)
        Label(self.update_customer_frame, text=5*" " + "Update customer details" + 5*" ", fg='#fff', bg="#000", relief='groove',
              font=("Times New Roman", 28)).place(relx=0.5, rely=0.28, anchor='center')

        self.customer_edit_frame = Frame(
            self.update_customer_frame, width=750, height=350, bg="#000", bd=3, relief='groove')
        self.customer_edit_frame.place(relx=0.5, rely=0.6, anchor='center')

        # customer first name
        Label(self.customer_edit_frame, text='First name', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.1, rely=0.08, anchor='w')
        self.customer_first_name = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.customer_first_name.insert(0, customer_details["fname"])
        self.customer_first_name.place(relx=0.1, rely=0.19, anchor='w')
        # customer last name
        Label(self.customer_edit_frame, text='Last name', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.55, rely=0.08, anchor='w')
        self.customer_last_name = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.customer_last_name.insert(0, customer_details["lname"])
        self.customer_last_name.place(relx=0.55, rely=0.19, anchor='w')
        # customer account number
        Label(self.customer_edit_frame, text='Account number', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.1, rely=0.32, anchor='w')
        self.customer_account_no = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.customer_account_no.insert(0, customer_details["account_no"])
        self.customer_account_no.place(relx=0.1, rely=0.44, anchor='w')
        # customer account type
        Label(self.customer_edit_frame, text='Account type', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.55, rely=0.32, anchor='w')
        account_types = ["Savings", "Current"]
        self.customer_account_type = ttk.Combobox(self.customer_edit_frame, font=(
            "Times New Roman", 18), values=['----'*8]+account_types, state='readonly', width=18)
        self.customer_account_type.current(
            account_types.index(the_account_type)+1)
        self.customer_account_type.place(relx=0.55, rely=0.44, anchor='w')
        # customer account balance
        Label(self.customer_edit_frame, text='Account balance', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.1, rely=0.58, anchor='w')
        self.customer_account_balance = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.customer_account_balance.insert(0, customer_details["balance"])
        self.customer_account_balance.place(relx=0.1, rely=0.7, anchor='w')
        # customer address
        Label(self.customer_edit_frame, text='Address', font=("Times New Roman", 18), bg='#000',
              fg='#fff').place(relx=0.55, rely=0.58, anchor='w')
        self.customer_account_address = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=("Times New Roman", 18), width=19)
        self.customer_account_address.insert(0, customer_details["address"])
        self.customer_account_address.place(relx=0.55, rely=0.7, anchor='w')

        Button(self.customer_edit_frame, text="Update customer details", font=("Times New Roman", 16), width=35,
               command=lambda: self.save_customer_update(values[2], values[-1]), bg='orange', fg="#000").place(relx=0.5, rely=0.88, anchor='center')

    def update_admin_details(self):
        admin_first_name = self.admin_first_name.get()
        admin_last_name = self.admin_last_name.get()
        admin_user_name = self.admin_user_name.get()
        admin_address = self.admin_address.get()
        self.CURRENTLY_LOGGED_IN_ADMIN['fname'] = admin_first_name
        self.CURRENTLY_LOGGED_IN_ADMIN['lname'] = admin_last_name
        self.CURRENTLY_LOGGED_IN_ADMIN['user_name'] = admin_user_name
        self.CURRENTLY_LOGGED_IN_ADMIN['address'] = admin_address

        messagebox.showinfo("Update Status", "Update was successful!")
        self.update_admin_frame.place_forget()
        self.show_admin_dashboard()

    def save_customer_update(self, account, path):
        customer_first_name_entry = self.customer_first_name.get()
        customer_last_name_entry = self.customer_last_name.get()
        customer_account_no_entry = self.customer_account_no.get()
        customer_account_type_entry = self.customer_account_type.get()
        customer_account_balance_entry = self.customer_account_balance.get()
        customer_account_address_entry = self.customer_account_address.get()

        # update the customer here
        get_customer = [
            i for i in self.customer_dictionary if i['account_no'] == str(account)][0]
        get_customer["fname"] = customer_first_name_entry
        get_customer["lname"] = customer_last_name_entry
        get_customer["account_no"] = customer_account_no_entry
        get_customer["account_type"] = customer_account_type_entry
        get_customer["balance"] = customer_account_balance_entry
        get_customer["address"] = customer_account_address_entry

        messagebox.showinfo("Update Status", "Customer update is successful!")
        # redirect to previous section
        self.update_customer_frame.place_forget()
        if path == "all_customer":
            self.show_all_customer_frame()
        else:
            self.show_search_customer_frame()

    def search_for_customer(self):
        search_entry = self.search_string.get()
        search_criteria = self.search_parameter.get()

        if search_entry:
            if not search_criteria:
                messagebox.showerror(
                    "Search Status", "Please select a search criteria!")
            else:
                query = search_entry.casefold()
                if search_criteria == "name":
                    results = [i for i in self.customer_dictionary if query in i["fname"].casefold(
                    ) or query in i["lname"].casefold()]
                elif search_criteria == "address":
                    results = [
                        i for i in self.customer_dictionary if query in i["address"].casefold()]
                elif search_criteria == "balance":
                    results = [
                        i for i in self.customer_dictionary if query in i["balance"].casefold()]
                elif search_criteria == "account_no":
                    results = [
                        i for i in self.customer_dictionary if query in i["account_no"].casefold()]
                elif search_criteria == "account_type":
                    results = [
                        i for i in self.customer_dictionary if query in i["account_type"].casefold()]

                # if there are results, show them on the tree
                if results:
                    self.load_search_customer_tree(results)

    def load_search_customer_tree(self, results):
        self.show_search_customer_frame()

        for customer in results:
            full_name = customer["fname"] + " " + customer["lname"]
            details = (full_name, customer["account_no"], customer["balance"])
            self.search_customer_tree.insert("", 'end', values=details)

    def load_all_customer_tree(self):
        # Add the tree headings
        self.all_customer_tree.heading(
            "first_name", text="First Name", anchor='center')
        self.all_customer_tree.heading(
            "last_name", text="Last Name", anchor='center')
        self.all_customer_tree.heading(
            "account_no", text="Account No.", anchor='center')
        self.all_customer_tree.heading(
            "balance", text="Balance", anchor='center')

        for customer in self.customer_dictionary:
            details = (customer["fname"], customer["lname"],
                       customer["account_no"], customer["balance"])
            self.all_customer_tree.insert("", 'end', values=details)

    def view_customer(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        if the_values:
            self.show_single_customer_frame(the_values+[tree_type])

    def update_customer(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        if the_values:
            self.show_update_customer_frame(the_values+[tree_type])

    def close_account(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        # Do the removing from db
        account_number = the_values[2]
        for index, value in enumerate(self.customer_dictionary):
            if value['account_no'] == str(account_number):
                break

        del self.customer_dictionary[index]
        messagebox.showinfo("Account Removal",
                            "Account was removed successfully!")
        if tree_type == "all_customer":
            self.show_all_customer_frame()
        else:
            self.show_search_customer_frame()

    def show_import_dialog(self):
        self._file = askopenfilename(defaultextension='.csv', filetypes=[
                                     ('XLS Worksheet', '*.csv')])
        if self._file:
            self.import_data_button.place(relx=0.5, rely=0.78, anchor='center')
        else:
            self.import_data_button.place_forget()

        self.file_selected.config(text=self._file)

    def show_export_dialog(self):
        self._export_location = asksaveasfilename(defaultextension='.csv', filetypes=[
            ('XLS Worksheet', '*.csv')])
        if self._export_location:
            self.export_data_button.place(relx=0.5, rely=0.78, anchor='center')
        else:
            self.export_data_button.place_forget()

        self.export_location_selected.config(text=self._export_location)

    def show_report_dialog(self):
        self._report_save_location = asksaveasfilename(
            defaultextension='.txt', filetypes=[('Text Document', '*.txt')])
        if self._report_save_location:
            self.export_management_button.place(
                relx=0.5, rely=0.78, anchor='center')
        else:
            self.export_management_button.place_forget()

        self.save_location_selected.config(text=self._report_save_location)

    def import_data(self):
        self.admin_dictionary = []
        self.customer_dictionary = []

        with open(self._file, "r") as fp:
            file_content = fp.readlines()

        for line in file_content[1:]:
            splitted = line.strip().split('"')
            address = splitted[1]
            if splitted[-1] != ',,,,':  # admin user
                _dict = {}
                names = splitted[0].split(',')
                other_info = splitted[2].split(',')
                _dict["fname"] = names[0]
                _dict["lname"] = names[1]
                _dict["account_no"] = ""
                _dict["account_type"] = ""
                _dict["balance"] = ""
                _dict["address"] = address
                _dict["is_admin"] = "1"
                _dict["user_name"] = other_info[2]
                _dict["password"] = other_info[3]
                _dict["full_admin_rights"] = other_info[4]
                self.admin_dictionary.append(_dict)
            else:  # customers
                _dict = {}
                names = splitted[0].split(',')
                _dict["fname"] = names[0]
                _dict["lname"] = names[1]
                _dict["account_no"] = names[2]
                _dict["account_type"] = names[3]
                _dict["balance"] = names[4]
                _dict["address"] = address
                _dict["is_admin"] = ""
                _dict["user_name"] = ""
                _dict["password"] = ""
                _dict["full_admin_rights"] = ""
                self.customer_dictionary.append(_dict)

        messagebox.showinfo(
            "Load Status", "Customer data import was successful!")
        self.import_data_frame.place_forget()
        self.show_admin_dashboard()

    def export_data(self):
        # Do the export here...
        header = ["First Name", "Last Name", "Account No.", "Account Type", "Balance",
                  "Address", "Is_Admin", "Username", "Password", "Full_Admin_Rights"]
        customer_data = [[i["fname"], i["lname"], i["account_no"], i["account_type"], i["balance"], i["address"],
                          i["is_admin"], i["user_name"], i["password"], i["full_admin_rights"]] for i in self.customer_dictionary]
        admin_data = [[i["fname"], i["lname"], i["account_no"], i["account_type"], i["balance"], i["address"],
                       i["is_admin"], i["user_name"], i["password"], i["full_admin_rights"]] for i in self.admin_dictionary]
        with open(self._export_location, 'w', encoding='UTF8', newline="") as fp:
            data_writer = writer(fp)
            data_writer.writerow(header)
            data_writer.writerows(customer_data)
            data_writer.writerows(admin_data)
        # show messagebox for success
        messagebox.showinfo("Export Status", "Export was successful!")
        self.filename_to_export.set("")
        self.export_data_frame.place_forget()
        self.show_admin_dashboard()

    def export_report_data(self):
        # Do the export here...
        total_sum = sum([int(i["balance"])
                        for i in self.customer_dictionary])
        with open(self._report_save_location, 'w') as fp:
            fp.write(
                f"Total number of customers: {len(self.customer_dictionary)}\n")
            fp.write(
                f"Sum of all the money all accounts have: {total_sum}\n")
            fp.write("Sum of interest payable for one year: 48%\n")
            fp.write("Total amount of overdrafts : 2340")

        # show messagebox for success
        messagebox.showinfo("Export Status", "Export was successful!")
        self.filename_to_export_report.set("")
        self.request_report_frame.place_forget()
        self.show_admin_dashboard()

    def transfer_funds(self):
        fund_entry = self.fund_entry.get()
        customer_from = self.customer_from.get()
        customer_to = self.customer_to.get()
        try:
            fund_entry = int(fund_entry)
            if customer_from not in self.customer_list or customer_to not in self.customer_list or customer_to == customer_from:
                messagebox.showerror("Fund Transfer Status",
                                     "Please select two different valid customers!")
            else:
                cus_from_first_name, cus_from_last_name = customer_from.split(
                    " ")
                cus_to_first_name, cus_to_last_name = customer_to.split(" ")
                cus_from = [i for i in self.customer_dictionary if i['fname'] ==
                            cus_from_first_name and i['lname'] == cus_from_last_name][0]
                cus_to = [i for i in self.customer_dictionary if i['fname'] ==
                          cus_to_first_name and i['lname'] == cus_to_last_name][0]
                cus_from['balance'] = str(
                    int(cus_from['balance']) - fund_entry)
                cus_to['balance'] = str(fund_entry + int(cus_to['balance']))
                messagebox.showinfo("Fund Transfer Status",
                                    "Transfer of funds is successful!")
                self.transfer_funds_frame.place_forget()
                self.transaction_funds.set("")
                self.show_admin_dashboard()
        except ValueError:
            messagebox.showerror("Fund Transfer Status",
                                 "Please enter a number!")

    def login_the_admin(self):
        """ Check the credentials provided and login the admin """

        username, password = self.username.get(), self.password.get()
        admin_usernames = [i['user_name'] for i in self.admin_dictionary]

        if username and password:
            if username in admin_usernames:
                the_admin_logged = [
                    i for i in self.admin_dictionary if i["user_name"] == username][0]
                the_password = [i["password"]
                                for i in self.admin_dictionary if i["user_name"] == username][0]
                if password == the_password:
                    self.login_frame.place_forget()
                    self.username.set("")
                    self.password.set("")
                    self.show_admin_dashboard()
                    self.CURRENTLY_LOGGED_IN_ADMIN = the_admin_logged
                else:
                    messagebox.showinfo(
                        "Login Failed", "Username or password is incorrect")
            else:
                messagebox.showinfo(
                    "Login Failed", "Username or password is incorrect")
                self.username_entry.focus()

    def logout_admin(self):
        self.dashboard_frame.place_forget()
        self.show_login_page()
        self.username_entry.focus()

    # FUNCTIONS THAT CAME WITH THE FILE ARE BELOW
    def load_bank_data(self):
        global accounts_list, admins_list

        with open('bank-store.csv', "r") as fp:
            file_content = fp.readlines()

            for line in file_content[1:]:
                splitted = line.strip().split('"')
                address = splitted[1]
                if splitted[-1] != ',,,,':  # admin user
                    _dict = {}
                    names = splitted[0].split(',')
                    other_info = splitted[2].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = ""
                    _dict["account_type"] = ""
                    _dict["balance"] = ""
                    _dict["address"] = address
                    _dict["is_admin"] = "1"
                    _dict["user_name"] = other_info[2]
                    _dict["password"] = other_info[3]
                    _dict["full_admin_rights"] = other_info[4]
                    self.admin_dictionary.append(_dict)
                    admins_list.append(_dict)
                else:  # customers
                    _dict = {}
                    names = splitted[0].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = names[2]
                    _dict["account_type"] = names[3]
                    _dict["balance"] = names[4]
                    _dict["address"] = address
                    _dict["is_admin"] = ""
                    _dict["user_name"] = ""
                    _dict["password"] = ""
                    _dict["full_admin_rights"] = ""
                    self.customer_dictionary.append(_dict)
                    accounts_list.append(_dict)

        # # create customers
        # account_no = 1234
        # customer_1 = CustomerAccount(
        #     "Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], account_no, 5000.00)
        # self.accounts_list.append(customer_1)

        # account_no += 1
        # customer_2 = CustomerAccount("David", "White", [
        #                              "60", "Holborn Viaduct", "London", "EC1A 2FD"], account_no, 3200.00)
        # self.accounts_list.append(customer_2)

        # account_no += 1
        # customer_3 = CustomerAccount("Alice", "Churchil", [
        #                              "5", "Cardigan Street", "Birmingham", "B4 7BD"], account_no, 18000.00)
        # self.accounts_list.append(customer_3)

        # account_no += 1
        # customer_4 = CustomerAccount("Ali", "Abdallah", [
        #                              "44", "Churchill Way West", "Basingstoke", "RG21 6YR"], account_no, 40.00)
        # self.accounts_list.append(customer_4)

        # # create admins
        # admin_1 = Admin("Julian", "Padget", [
        #                 "12", "London Road", "Birmingham", "B95 7TT"], "id1188", "1441", True)
        # self.admins_list.append(admin_1)

        # admin_2 = Admin("Cathy",  "Newman", [
        #                 "47", "Mars Street", "Newcastle", "NE12 6TZ"], "id3313", "2442", False)
        # self.admins_list.append(admin_2)

    # def search_admins_by_name(self, admin_username):
    #     # STEP A.2
    #     pass

    # def search_customers_by_name(self, customer_lname):
    #     # STEP A.3
    #     pass

    # def main_menu(self):
    #     # print the options you have
    #     print()
    #     print()
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("Welcome to the Python Bank System")
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("1) Admin login")
    #     print("2) Quit Python Bank System")
    #     print(" ")
    #     option = int(input("Choose your option: "))
    #     return option

    # def run_main_options(self):
    #     loop = 1
    #     while loop == 1:
    #         choice = self.main_menu()
    #         if choice == 1:
    #             username = input("\n Please input admin username: ")
    #             password = input("\n Please input admin password: ")
    #             msg, admin_obj = self.admin_login(username, password)
    #             print(msg)
    #             if admin_obj != None:
    #                 self.run_admin_options(admin_obj)
    #         elif choice == 2:
    #             loop = 0
    #     print("\n Thank-You for stopping by the bank!")

    # def transferMoney(self, sender_lname, receiver_lname, receiver_account_no, amount):
    #     # ToDo
    #     pass

    # def admin_login(self, username, password):
    #     # STEP A.1
    #     pass

    # def admin_menu(self, admin_obj):
    #     # print the options you have
    #     print(" ")
    #     print("Welcome Admin %s %s : Avilable options are:" %
    #           (admin_obj.get_first_name(), admin_obj.get_last_name()))
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("1) Transfer money")
    #     print("2) Customer account operations & profile settings")
    #     print("3) Delete customer")
    #     print("4) Print all customers detail")
    #     print("5) Sign out")
    #     print(" ")
    #     option = int(input("Choose your option: "))
    #     return option

    # def run_admin_options(self, admin_obj):
    #     loop = 1
    #     while loop == 1:
    #         choice = self.admin_menu(admin_obj)
    #         if choice == 1:
    #             sender_lname = input("\n Please input sender surname: ")
    #             amount = float(
    #                 input("\n Please input the amount to be transferred: "))
    #             receiver_lname = input("\n Please input receiver surname: ")
    #             receiver_account_no = input(
    #                 "\n Please input receiver account number: ")
    #             self.transferMoney(sender_lname, receiver_lname,
    #                                receiver_account_no, amount)
    #         elif choice == 2:
    #             # STEP A.4
    #             pass

    #         elif choice == 3:
    #             # Todo
    #             pass

    #         elif choice == 4:
    #             # Todo
    #             pass

    #         elif choice == 5:
    #             loop = 0
    #     print("\n Exit account operations")

    # def print_all_accounts_details(self):
    #     # list related operation - move to main.py
    #     i = 0
    #     for c in self.accounts_list:
    #         i += 1
    #         print('\n %d. ' % i, end=' ')
    #         c.print_details()
    #         print("------------------------")


if __name__ == '__main__':
    root = Tk()
    root.title("Python Banking System")
    root.geometry("1300x700+33+20")
    root.resizable(0, 0)
    app = BankingSystem()
    # app.run_main_options()
    root.mainloop()
