import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import sqlite3
from styles import ModernStyles

class AttendanceWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Attendance Management")
        self.geometry("800x600")
        self.configure(bg=ModernStyles.COLORS['background'])
        
        # Configure modern styles
        ModernStyles.configure_styles()
        
        self.create_widgets()
        self.load_attendance()
    
    def create_widgets(self):
        """Create modern attendance interface"""
        # Header
        header = tk.Frame(self, bg=ModernStyles.COLORS['primary'])
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="Attendance Management",
            font=('Segoe UI', 24, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title.pack(pady=20)
        
        # Input section
        input_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        input_frame.pack(fill="x", padx=20, pady=20)
        
        # Member ID input
        tk.Label(
            input_frame,
            text="Member ID:",
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['surface'],
            fg=ModernStyles.COLORS['text_primary']
        ).pack(side="left", padx=10)
        
        self.member_id_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=ModernStyles.COLORS['background'],
            fg=ModernStyles.COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        self.member_id_entry.pack(side="left", padx=10)
        
        # Buttons
        checkin_btn = tk.Button(
            input_frame,
            text="✅ Check-In",
            command=self.check_in,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['success'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['success'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        checkin_btn.pack(side="left", padx=10)
        
        checkout_btn = tk.Button(
            input_frame,
            text="⏰ Check-Out",
            command=self.check_out,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['warning'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['warning'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        checkout_btn.pack(side="left", padx=10)
        
        # Attendance table
        table_frame = tk.Frame(self, bg=ModernStyles.COLORS['surface'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Create treeview
        cols = ("ID", "Member ID", "Member Name", "Check-In", "Check-Out", "Duration")
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
            "Check-In": 150,
            "Check-Out": 150,
            "Duration": 100
        }
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
    
    def check_in(self):
        """Record check-in"""
        member_id = self.member_id_entry.get()
        if not member_id:
            messagebox.showerror("Error", "Please enter Member ID")
            return
        
        try:
            # Check if member exists
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            
            # Verify member exists
            cur.execute("SELECT name FROM members WHERE id=?", (member_id,))
            member = cur.fetchone()
            
            if not member:
                messagebox.showerror("Error", "Member not found")
                conn.close()
                return
            
            # Check if already checked in today
            today = datetime.now().strftime("%Y-%m-%d")
            cur.execute("""
                SELECT id FROM attendance 
                WHERE member_id=? AND date(checkin_time)=? AND checkout_time IS NULL
            """, (member_id, today))
            
            if cur.fetchone():
                messagebox.showwarning("Warning", "Member already checked in today")
                conn.close()
                return
            
            # Record check-in
            cur.execute(
                "INSERT INTO attendance (member_id, checkin_time) VALUES (?, ?)",
                (member_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Check-in recorded for {member[0]}")
            self.load_attendance()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record check-in: {str(e)}")
    
    def check_out(self):
        """Record check-out"""
        member_id = self.member_id_entry.get()
        if not member_id:
            messagebox.showerror("Error", "Please enter Member ID")
            return
        
        try:
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            
            # Find open check-in
            today = datetime.now().strftime("%Y-%m-%d")
            cur.execute("""
                SELECT id FROM attendance 
                WHERE member_id=? AND date(checkin_time)=? AND checkout_time IS NULL
            """, (member_id, today))
            
            attendance_record = cur.fetchone()
            
            if not attendance_record:
                messagebox.showwarning("Warning", "No open check-in found for today")
                conn.close()
                return
            
            # Record check-out
            cur.execute(
                "UPDATE attendance SET checkout_time=? WHERE id=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), attendance_record[0])
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Check-out recorded successfully")
            self.load_attendance()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record check-out: {str(e)}")
    
    def load_attendance(self):
        """Load attendance records"""
        try:
            conn = sqlite3.connect("gym.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT a.id, a.member_id, m.name, a.checkin_time, a.checkout_time,
                       CASE 
                           WHEN a.checkout_time IS NULL THEN 'Active'
                           ELSE CAST((julianday(a.checkout_time) - julianday(a.checkin_time)) * 24 * 60 AS INTEGER) || ' min'
                       END as duration
                FROM attendance a
                JOIN members m ON a.member_id = m.id
                ORDER BY a.checkin_time DESC
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
            messagebox.showerror("Error", f"Failed to load attendance: {str(e)}")
