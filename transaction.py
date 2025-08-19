import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from receipt_generator import generate_receipt_pdf
from styles import ModernStyles

class TransactionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Transaction Management")
        self.geometry("800x600")
        self.configure(bg=ModernStyles.COLORS['background'])
        
        # Configure modern styles
        ModernStyles.configure_styles()
        
        self.create_widgets()
        self.load_transactions()
    
    def create_widgets(self):
        """Create modern transaction interface"""
        # Header
        header = tk.Frame(self, bg=ModernStyles.COLORS['primary'])
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="Transaction Management",
            font=('Segoe UI', 24, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title.pack(pady=20)
        
        # Input section
        input_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        input_frame.pack(fill="x", padx=20, pady=20)
        
        # Member ID
        tk.Label(
            input_frame,
            text="Member ID:",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.member_id_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['background'],
            fg=ModernStyles.COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        self.member_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Amount
        tk.Label(
            input_frame,
            text="Amount ($):",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.amount_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['background'],
            fg=ModernStyles.COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Payment type
        tk.Label(
            input_frame,
            text="Payment Type:",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.payment_type = tk.StringVar(value="Monthly")
        payment_combo = ttk.Combobox(
            input_frame,
            textvariable=self.payment_type,
            values=["Monthly", "Quarterly", "Yearly", "Lifetime", "Other"],
            state="readonly",
            font=('Segoe UI', 12)
        )
        payment_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg=ModernStyles.COLORS['surface'])
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        add_payment_btn = tk.Button(
            button_frame,
            text="💳 Add Payment",
            command=self.add_payment,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['success'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['success'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        add_payment_btn.pack(side="left", padx=5)
        
        generate_receipt_btn = tk.Button(
            button_frame,
            text="📄 Generate Receipt",
            command=self.generate_receipt_for_member,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['accent'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['accent'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        generate_receipt_btn.pack(side="left", padx=5)
        
        # Transactions table
        table_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Create treeview
        cols = ("ID", "Member ID", "Member Name", "Amount", "Date", "Payment Type")
        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set,
            style='Modern.Treeview'
        )
        
        # Configure columns
        column_widths = {
            "ID": 50,
            "Member ID": 80,
            "Member Name": 150,
            "Amount": 100,
            "Date": 100,
            "Payment Type": 100
        }
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
    
    def add_payment(self):
        """Add new payment"""
        member_id = self.member_id_entry.get()
        amount = self.amount_entry.get()
        payment_type = self.payment_type.get()
        
        if not member_id or not amount:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return
        
        try:
            # Check if member exists
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            
            cur.execute("SELECT name FROM members WHERE id=?", (member_id,))
            member = cur.fetchone()
            
            if not member:
                messagebox.showerror("Error", "Member not found")
                conn.close()
                return
            
            # Add transaction
            cur.execute(
                "INSERT INTO transactions (member_id, amount_paid, date) VALUES (?, ?, ?)",
                (member_id, amount, datetime.now().strftime("%Y-%m-%d"))
            )
            conn.commit()
            conn.close()
            
            # Generate receipt
            generate_receipt_pdf(member_id, amount)
            
            messagebox.showinfo("Success", f"Payment recorded for {member[0]}")
            self.load_transactions()
            
            # Clear fields
            self.member_id_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {str(e)}")
    
    def generate_receipt_for_member(self):
        """Generate receipt for entered member"""
        member_id = self.member_id_entry.get()
        amount = self.amount_entry.get()
        
        if not member_id or not amount:
            messagebox.showerror("Error", "Please enter Member ID and Amount")
            return
        
        try:
            amount = float(amount)
            generate_receipt_pdf(member_id, amount)
            messagebox.showinfo("Success", "Receipt generated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def load_transactions(self):
        """Load transaction history"""
        try:
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT t.id, t.member_id, m.name, t.amount_paid, t.date
                FROM transactions t
                JOIN members m ON t.member_id = m.id
                ORDER BY t.date DESC, t.id DESC
                LIMIT 100
            """)
            rows = cur.fetchall()
            conn.close()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add new items
            for row in rows:
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
