import tkinter as tk
from tkinter import ttk
from add_member import AddMemberWindow
from view_member import ViewMemberWindow
from attendance import AttendanceWindow
from transaction import TransactionWindow
from about import AboutWindow
import sqlite3
from db import connect_db
from styles import ModernStyles
import tkinter.font as tkfont
from receipt_generator import generate_receipt_pdf

class GymManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("1000x700")
        self.configure(bg=ModernStyles.COLORS['background'])
        
        # Configure modern styles
        ModernStyles.configure_styles()
        
        # Initialize database
        connect_db()
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create modern sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
    
    def create_sidebar(self):
        """Create modern sidebar with gradient effect"""
        sidebar = tk.Frame(self, bg=ModernStyles.COLORS['primary'], width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo/Title area
        logo_frame = tk.Frame(sidebar, bg=ModernStyles.COLORS['primary'])
        logo_frame.pack(fill="x", pady=30)
        
        title_label = tk.Label(
            logo_frame, 
            text="ARIF X MAINUL", 
            font=('Segoe UI', 24, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            logo_frame,
            text="GYM Management System",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['light']
        )
        subtitle_label.pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(sidebar, bg=ModernStyles.COLORS['primary'])
        nav_frame.pack(fill="both", expand=True, padx=20)
        
        buttons = [
            ("Add Member", self.open_add_member, "➕"),
            ("View Members", self.open_view_member, "👥"),
            ("Attendance", self.open_attendance, "📊"),
            ("Transactions", self.open_transaction, "💳"),
            ("About", self.open_about, "ℹ️")
        ]
        
        for text, command, icon in buttons:
            btn = tk.Button(
                nav_frame,
                text=f" {icon} {text}",
                command=command,
                font=('Segoe UI', 12, 'bold'),
                bg=ModernStyles.COLORS['secondary'],
                fg=ModernStyles.COLORS['surface'],
                activebackground=ModernStyles.COLORS['accent'],
                activeforeground=ModernStyles.COLORS['surface'],
                bd=0,
                pady=15,
                padx=20,
                width=20,
                anchor="w",
                cursor="hand2"
            )
            btn.pack(fill="x", pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=ModernStyles.COLORS['accent']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=ModernStyles.COLORS['secondary']))
    
    def create_main_content(self):
        """Create modern main content area"""
        self.main_frame = tk.Frame(self, bg=ModernStyles.COLORS['background'])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        
        # Welcome section
        welcome_frame = tk.Frame(self.main_frame, bg=ModernStyles.COLORS['surface'])
        welcome_frame.pack(fill="x", pady=20)
        
        welcome_label = tk.Label(
            welcome_frame,
            text="Welcome to Gym Management System",
            font=('Segoe UI', 32, 'bold'),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['primary']
        )
        welcome_label.pack(pady=40)
        
        # Stats section
        self.stats_frame = tk.Frame(self.main_frame, bg=ModernStyles.COLORS['surface'])
        self.stats_frame.pack(fill="x", pady=20)
        self.update_stats(self.stats_frame)
        
        # Quick actions (add only once)
        quick_actions = tk.Label(
            self.main_frame,
            text="Select an option from the sidebar to get started",
            font=('Segoe UI', 16),
            bg=ModernStyles.COLORS['background'],
            fg=ModernStyles.COLORS['text_secondary']
        )
        quick_actions.pack(pady=40)
    
    def update_stats(self, parent):
        """Fetch and update stats from the database"""
        # Clear previous stat cards in stats_frame
        for widget in parent.winfo_children():
            widget.destroy()
        
        conn = sqlite3.connect("gym.db")
        cur = conn.cursor()
        
        # Fetch total members
        cur.execute("SELECT COUNT(*) FROM members")
        total_members = cur.fetchone()[0]
        
        # Fetch active members
        cur.execute("""
            SELECT COUNT(*) FROM attendance 
            WHERE date(checkin_time) = date('now') AND checkout_time IS NULL
        """)
        active_today = cur.fetchone()[0] or 0
        cur.execute("SELECT SUM(amount_paid) FROM transactions WHERE date >= date('now', 'start of month')")
        revenue = cur.fetchone()[0] or 0
        
        conn.close()
        
        # Place Refresh Button inside stats_frame for visibility
        refresh_btn = tk.Button(
            parent,
            text="🔄 Refresh Stats",
            command=lambda: self.update_stats(parent),
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['accent'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['primary'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        refresh_btn.pack(side="right", padx=10, pady=10)
        
        # Update stat cards
        self.create_stat_card(parent, "Total Members", str(total_members), 0)
        self.create_stat_card(parent, "Active Today", str(active_today), 1)
        self.create_stat_card(parent, "Revenue This Month", f"${revenue}", 2)
        
        # Move quick actions label creation to create_main_content so it doesn't duplicate
    
    def create_stat_card(self, parent, title, value, column):
        """Create modern stat card"""
        card = tk.Frame(parent, bg=ModernStyles.COLORS['surface'], relief="raised", bd=1)
        card.pack(padx=20, pady=20, fill="x")
        
        title_label = tk.Label(
            card,
            text=title,
            font=('Segoe UI', 14),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_secondary']
        )
        title_label.pack(pady=(20, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Segoe UI', 28, 'bold'),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['primary']
        )
        value_label.pack(pady=(5, 20))
    
    def open_add_member(self):
        AddMemberWindow(self)
    
    def open_view_member(self):
        ViewMemberWindow(self)
    
    def open_attendance(self):
        AttendanceWindow(self)
    
    def open_transaction(self):
        TransactionWindow(self)
    
    def open_about(self):
        AboutWindow(self)

if __name__ == "__main__":
    app = GymManagementSystem()
    app.mainloop()
