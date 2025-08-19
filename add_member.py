import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from styles import ModernStyles

class AddMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent) 
        self.parent = parent  # Store the parent reference
        self.title("Add Member")
        self.geometry("500x700")
        self.configure(bg=ModernStyles.COLORS['background'])
        self.resizable(False, False)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern form widgets"""
        # Header
        header = tk.Frame(self, bg=ModernStyles.COLORS['primary'])
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="Add New Member",
            font=('Segoe UI', 20, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title.pack(pady=20)
        
        # --- Scrollable Form Container ---
        container = tk.Frame(self, bg=ModernStyles.COLORS['background'])
        container.pack(fill="both", expand=True, padx=40, pady=30)

        canvas = tk.Canvas(
            container,
            bg=ModernStyles.COLORS['background'],
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Make the form_frame a child of the canvas
        form_frame = tk.Frame(canvas, bg=ModernStyles.COLORS['background'])
        form_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_frame.bind("<Configure>", on_configure)

        # Enable mousewheel scrolling (Windows and Mac support)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Form fields
        fields = [
            ("Name", "Full Name"),
            ("Age", "Age"),
            ("Gender", "Gender"),
            ("Phone", "Phone Number"),
            ("Address", "Address"),
            ("Membership Type", "Membership Type"),
            ("Start Date", "Start Date (YYYY-MM-DD)"),
            ("End Date", "End Date (YYYY-MM-DD)")
        ]
        
        self.entries = {}
        
        for field_name, placeholder in fields:
            # Label
            label = tk.Label(
                form_frame,
                text=field_name,
                font=('Segoe UI', 12, 'bold'),
                bg=ModernStyles.COLORS['background'],
                fg=ModernStyles.COLORS['text_primary']
            )
            label.pack(anchor="w", pady=(10, 5))
            
            # Entry
            if field_name == "Gender":
                # Dropdown for gender
                entry = ttk.Combobox(
                    form_frame,
                    font=('Segoe UI', 12),
                    values=["Male", "Female", "Other"],
                    state="readonly"
                )
            elif field_name == "Membership Type":
                # Dropdown for membership type
                entry = ttk.Combobox(
                    form_frame,
                    font=('Segoe UI', 12),
                    values=["Monthly", "Quarterly", "Yearly", "Lifetime"],
                    state="readonly"
                )
            else:
                entry = tk.Entry(
                    form_frame,
                    font=('Segoe UI', 12),
                    bg=ModernStyles.COLORS['surface'],
                    fg=ModernStyles.COLORS['text_primary'],
                    relief="solid",
                    bd=1
                )
            
            entry.pack(fill="x", pady=(0, 10))
            self.entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=ModernStyles.COLORS['background'])
        button_frame.pack(fill="x", pady=30)
        
        save_btn = tk.Button(
            button_frame,
            text="Save Member",
            command=self.save_member,
            font=('Segoe UI', 14, 'bold'),
            bg=ModernStyles.COLORS['success'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['success'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            font=('Segoe UI', 14, 'bold'),
            bg=ModernStyles.COLORS['border'],
            fg=ModernStyles.COLORS['text_primary'],
            activebackground=ModernStyles.COLORS['text_secondary'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        cancel_btn.pack(side="right", padx=5)
    
    def save_member(self):
        """Save member with validation"""
        try:
            data = [self.entries[f].get() for f, _ in [
                ("Name", "Full Name"),
                ("Age", "Age"),
                ("Gender", "Gender"),
                ("Phone", "Phone Number"),
                ("Address", "Address"),
                ("Membership Type", "Membership Type"),
                ("Start Date", "Start Date (YYYY-MM-DD)"),
                ("End Date", "End Date (YYYY-MM-DD)")
            ]]
            
            if not all(data):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            # Ensure table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age TEXT,
                    gender TEXT,
                    phone TEXT,
                    address TEXT,
                    membership_type TEXT,
                    start_date TEXT,
                    end_date TEXT
                )
            """)
            cur.execute("""
                INSERT INTO members (name, age, gender, phone, address, membership_type, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            member_id = cur.lastrowid
            conn.close()
            
            self.parent.update_stats(self.parent.stats_frame)
            messagebox.showinfo("Success", f"Member added successfully with ID: {member_id}")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member: {str(e)}")
    
    def update_stats(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        # ...rest of your stats update code...
