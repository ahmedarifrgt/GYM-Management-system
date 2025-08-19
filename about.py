import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
from styles import ModernStyles

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Our Team")
        self.geometry("900x700")
        self.configure(bg=ModernStyles.COLORS['background'])
        
        # Configure modern styles
        ModernStyles.configure_styles()
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create modern about interface"""
        # Main container
        main_frame = tk.Frame(self, bg=ModernStyles.COLORS['background'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main_frame, bg=ModernStyles.COLORS['primary'], height=120)
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="About Our Team",
            font=('Segoe UI', 24, 'bold'),
            bg=ModernStyles.COLORS['primary'],
            fg=ModernStyles.COLORS['surface']
        )
        title.pack(pady=20)
        
        # Team section
        team_frame = tk.Frame(main_frame, bg=ModernStyles.COLORS['surface'])
        team_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Team members data (using your local photo paths)
        team_data = [
            {
                "name": "MD ARIF",
                "role": "Lead Developer",
                "desc": "Responsible for overall architecture and core functionality of the project. "
                        "Extensive experience in software design and implementation.",
                "img": r"D:\CODE\gymmn proj\photo\Screenshot 2025-08-19 220025.png"
            },
            {
                "name": "MD MAINUL ISLAM",
                "role": "Co-Developer",
                "desc": "Handles UI/UX development and integration. Specializes in creating intuitive "
                        "user interfaces and seamless user experiences.",
                "img": r"D:\CODE\gymmn proj\photo\Screenshot 2025-08-19 220140.png"
            }
        ]
        
        # Keep references to images
        self.images = []
        
        # Create team member cards
        for member in team_data:
            member_frame = tk.Frame(team_frame, bg=ModernStyles.COLORS['surface'], relief="solid", bd=1)
            member_frame.pack(fill="x", padx=10, pady=10)
            
            # Horizontal layout: Photo + Info
            card_frame = tk.Frame(member_frame, bg=ModernStyles.COLORS['surface'])
            card_frame.pack(fill="x", padx=20, pady=20)
            
            # Load and display circular photo
            try:
                if os.path.exists(member["img"]):
                    img = Image.open(member["img"]).convert("RGBA")
                    img = img.resize((120, 120))  # Resize for uniform look
                    
                    # Create circular mask
                    mask = Image.new("L", (120, 120), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, 120, 120), fill=255)
                    
                    # Apply mask
                    img.putalpha(mask)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    self.images.append(photo)  # Prevent garbage collection
                    
                    img_label = tk.Label(card_frame, image=photo, bg=ModernStyles.COLORS['surface'])
                    img_label.pack(side="left", padx=20)
                else:
                    raise FileNotFoundError(f"Image not found: {member['img']}")
            except Exception as e:
                print(f"Error loading image for {member['name']}: {e}")
            
            # Member info (right side)
            info_frame = tk.Frame(card_frame, bg=ModernStyles.COLORS['surface'])
            info_frame.pack(side="left", fill="x", expand=True, padx=20)
            
            # Name
            name_label = tk.Label(
                info_frame,
                text=member["name"],
                font=('Segoe UI', 16, 'bold'),
                fg=ModernStyles.COLORS['primary'],
                bg=ModernStyles.COLORS['surface']
            )
            name_label.pack(anchor="w")
            
            # Role
            role_label = tk.Label(
                info_frame,
                text=member["role"],
                font=('Segoe UI', 12, 'italic'),
                fg=ModernStyles.COLORS['text_secondary'],
                bg=ModernStyles.COLORS['surface']
            )
            role_label.pack(anchor="w")
            
            # Description
            desc_label = tk.Label(
                info_frame,
                text=member["desc"],
                font=('Segoe UI', 10),
                fg=ModernStyles.COLORS['text_secondary'],
                bg=ModernStyles.COLORS['surface'],
                wraplength=500,
                justify="left"
            )
            desc_label.pack(anchor="w", pady=10)
        
        # Footer
        footer = tk.Frame(main_frame, bg=ModernStyles.COLORS['surface'])
        footer.pack(fill="x", pady=20)
        
        footer_text = tk.Label(
            footer,
            text="Thank you for your interest in our work. "
                 "We're passionate about creating exceptional digital experiences.",
            font=('Segoe UI', 10),
            fg=ModernStyles.COLORS['text_secondary'],
            bg=ModernStyles.COLORS['surface'],
            wraplength=600,
            justify="center"
        )
        footer_text.pack()
        
        # Close button
        close_btn = tk.Button(
            footer,
            text="Close",
            command=self.destroy,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyles.COLORS['accent'],
            fg=ModernStyles.COLORS['surface'],
            activebackground=ModernStyles.COLORS['primary'],
            activeforeground=ModernStyles.COLORS['surface'],
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        close_btn.pack(pady=10)
