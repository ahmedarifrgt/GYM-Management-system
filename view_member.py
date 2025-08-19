import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from styles import ModernStyles

class ViewMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("View Members")
        self.geometry("1000x600")
        self.configure(bg=ModernStyles.COLORS['background'])
        
        # Configure modern styles
        ModernStyles.configure_styles()
        
        self.create_widgets()
        self.load_members()
    
    def create_widgets(self):
        """Create modern view members interface"""
        # Header
        header = tk.Frame(self, bg=ModernStyles.COLORS['primary'])
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="Member Directory",
            font=('Segoe UI', 24, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title.pack(pady=20)
        
        # Search and filter section
        search_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        search_frame.pack(fill="x", padx=20, pady=20)
        
        # Search box
        search_label = tk.Label(
            search_frame,
            text="Search:",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        )
        search_label.pack(side="left", padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_members)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['background'],
            fg=ModernStyles.COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # Filter dropdown
        filter_label = tk.Label(
            search_frame,
            text="Filter by:",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        )
        filter_label.pack(side="left", padx=10)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_var,
            values=["All", "Monthly", "Quarterly", "Yearly", "Lifetime"],
            state="readonly",
            font=('Segoe UI', 11)
        )
        filter_combo.pack(side="left", padx=10)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_members())
        
        # Table frame
        table_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview with scrollbar
        tree_frame = tk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Columns
        cols = ("ID", "Name", "Age", "Gender", "Phone", "Membership Type", "Start Date", "End Date")

        # Treeview style (dark text)
        style = ttk.Style(self)
        style.configure(
            "Modern.Treeview",
            font=('Segoe UI', 11),
            foreground="black",   # Dark row text
            rowheight=28
        )
        style.configure(
            "Modern.Treeview.Heading",
            font=('Segoe UI', 12, 'bold'),
            foreground="black"    # Dark column header text
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set,
            style='Modern.Treeview'
        )
        
        # Configure columns
        column_widths = {
            "ID": 50,
            "Name": 150,
            "Age": 50,
            "Gender": 80,
            "Phone": 120,
            "Membership Type": 100,
            "Start Date": 100,
            "End Date": 100,
        }
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Action buttons
        button_frame = tk.Frame(self, bg=ModernStyles.COLORS['background'])
        button_frame.pack(fill="x", padx=20, pady=20)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.load_members,
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
        refresh_btn.pack(side="left", padx=5)
        
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete",
            command=self.delete_member,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['danger'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['danger'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        delete_btn.pack(side="right", padx=5)
    
    def load_members(self):
        """Load members from database"""
        try:
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, age, gender, phone, membership_type, start_date, end_date 
                FROM members 
                ORDER BY id DESC
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
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")
    
    def filter_members(self, *args):
        """Filter members based on search and membership type"""
        search_term = self.search_var.get().lower()
        membership_filter = self.filter_var.get()
        
        # Get all items
        items = self.tree.get_children()
        
        for item in items:
            values = self.tree.item(item)['values']
            name = str(values[1]).lower()
            membership_type = str(values[5])
            
            # Apply filters
            show_item = True
            
            if search_term and search_term not in name:
                show_item = False
            
            if membership_filter != "All" and membership_type != membership_filter:
                show_item = False
            
            if show_item:
                self.tree.item(item, tags=())
                self.tree.item(item, values=values)
            else:
                self.tree.detach(item)
    
    def delete_member(self):
        """Delete selected member"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this member?"):
            try:
                member_id = self.tree.item(selected[0])['values'][0]
                conn = sqlite3.connect("gym.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM members WHERE id=?", (member_id,))
                conn.commit()
                conn.close()
                
                self.tree.delete(selected[0])
                messagebox.showinfo("Success", "Member deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete member: {str(e)}")
