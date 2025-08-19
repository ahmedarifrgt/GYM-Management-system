import tkinter as tk
from tkinter import ttk

class ModernStyles:
    """Modern styling configuration for the gym management system"""
    
    # Color Palette
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'accent': '#3498db',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'light': '#ecf0f1',
        'dark': '#2c3e50',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'text_primary': '#2c3e50',
        'text_secondary': '#7f8c8d',
        'border': '#bdc3c7'
    }
    
    # Typography
    FONTS = {
        'heading': ('Segoe UI', 24, 'bold'),
        'subheading': ('Segoe UI', 18, 'bold'),
        'body': ('Segoe UI', 12),
        'small': ('Segoe UI', 10),
        'button': ('Segoe UI', 11, 'bold')
    }
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        
        # Configure button style
        style.configure(
            'Modern.TButton',
            font=('Segoe UI', 11, 'bold'),
            foreground=ModernStyles.COLORS['surface'],
            background=ModernStyles.COLORS['accent'],
            borderwidth=0,
            focuscolor='none',
            padding=10
        )
        
        style.map(
            'Modern.TButton',
            background=[('active', ModernStyles.COLORS['primary']),
                       ('disabled', ModernStyles.COLORS['border'])]
        )
        
        # Configure entry style
        style.configure(
            'Modern.TEntry',
            font=('Segoe UI', 12),
            fieldbackground=ModernStyles.COLORS['surface'],
            foreground=ModernStyles.COLORS['text_primary'],
            borderwidth=1,
            relief='solid'
        )
        
        # Configure label style
        style.configure(
            'Modern.TLabel',
            font=('Segoe UI', 12),
            background=ModernStyles.COLORS['background'],
            foreground=ModernStyles.COLORS['text_primary']
        )
        
        # Configure frame style
        style.configure(
            'Modern.TFrame',
            background=ModernStyles.COLORS['background']
        )
        
        # Configure treeview style
        style.configure(
            'Modern.Treeview',
            font=('Segoe UI', 11),
            background=ModernStyles.COLORS['surface'],
            foreground=ModernStyles.COLORS['text_primary'],
            fieldbackground=ModernStyles.COLORS['surface'],
            rowheight=30
        )
        
        style.configure(
            'Modern.Treeview.Heading',
            font=('Segoe UI', 12, 'bold'),
            background=ModernStyles.COLORS['primary'],
            foreground=ModernStyles.COLORS['surface']
        )
