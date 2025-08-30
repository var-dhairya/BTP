#!/usr/bin/env python3
"""
Interactive Indian Map Interface for Geography Quiz System
This provides a visual interface where users can click on states to get questions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
import time
from typing import Dict, List, Optional

class IndianMapInterface:
    """
    Interactive interface for the Indian States Geography Quiz System.
    Provides a visual map where users can click on states to get questions.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🇮🇳 Indian States Geography Quiz")
        self.root.geometry("1200x800")
        
        # API configuration
        self.api_base_url = "http://localhost:5000"
        self.current_student = None
        self.current_question = None
        self.session_start_time = None
        
        # State coordinates (simplified for demo - in real app, use actual map coordinates)
        self.state_coordinates = {
            "Jammu and Kashmir": (400, 50),
            "Himachal Pradesh": (420, 100),
            "Punjab": (380, 120),
            "Uttarakhand": (450, 150),
            "Haryana": (400, 160),
            "Delhi": (420, 170),
            "Rajasthan": (320, 200),
            "Uttar Pradesh": (450, 200),
            "Bihar": (500, 220),
            "Jharkhand": (480, 250),
            "West Bengal": (520, 250),
            "Sikkim": (540, 200),
            "Assam": (580, 200),
            "Arunachal Pradesh": (620, 180),
            "Nagaland": (600, 200),
            "Manipur": (610, 220),
            "Mizoram": (600, 240),
            "Tripura": (580, 240),
            "Meghalaya": (570, 220),
            "Odisha": (480, 280),
            "Chhattisgarh": (420, 280),
            "Madhya Pradesh": (380, 250),
            "Gujarat": (300, 250),
            "Maharashtra": (350, 300),
            "Goa": (320, 320),
            "Karnataka": (360, 340),
            "Kerala": (380, 380),
            "Tamil Nadu": (400, 360),
            "Telangana": (400, 300),
            "Andhra Pradesh": (420, 320)
        }
        
        self.setup_ui()
        self.load_states_data()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🇮🇳 Indian States Geography Quiz", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Student section
        student_frame = ttk.LabelFrame(main_frame, text="👤 Student Information", padding="10")
        student_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Student ID
        ttk.Label(student_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W)
        self.student_id_var = tk.StringVar(value="demo001")
        student_id_entry = ttk.Entry(student_frame, textvariable=self.student_id_var, width=15)
        student_id_entry.grid(row=0, column=1, padx=(10, 20))
        
        # Student Name
        ttk.Label(student_frame, text="Name:").grid(row=0, column=2, sticky=tk.W)
        self.student_name_var = tk.StringVar(value="Demo Student")
        student_name_entry = ttk.Entry(student_frame, textvariable=self.student_name_var, width=20)
        student_name_entry.grid(row=0, column=3, padx=(10, 20))
        
        # Grade
        ttk.Label(student_frame, text="Grade:").grid(row=0, column=4, sticky=tk.W)
        self.grade_var = tk.StringVar(value="5")
        grade_combo = ttk.Combobox(student_frame, textvariable=self.grade_var, 
                                  values=[str(i) for i in range(1, 13)], width=5)
        grade_combo.grid(row=0, column=5, padx=(10, 20))
        
        # Create/Login button
        self.login_btn = ttk.Button(student_frame, text="Login/Create Student", 
                                   command=self.login_student)
        self.login_btn.grid(row=0, column=6, padx=(10, 0))
        
        # Map canvas
        map_frame = ttk.LabelFrame(main_frame, text="🗺️ Interactive Map", padding="10")
        map_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        self.map_canvas = tk.Canvas(map_frame, width=800, height=500, bg="lightblue")
        self.map_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind canvas events
        self.map_canvas.bind("<Button-1>", self.on_map_click)
        
        # Quiz section
        quiz_frame = ttk.LabelFrame(main_frame, text="❓ Quiz Questions", padding="10")
        quiz_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Question display
        self.question_text = tk.Text(quiz_frame, height=6, width=40, wrap=tk.WORD)
        self.question_text.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Options
        self.option_vars = []
        self.option_buttons = []
        for i in range(4):
            var = tk.StringVar()
            self.option_vars.append(var)
            btn = ttk.Button(quiz_frame, textvariable=var, 
                           command=lambda x=i: self.select_answer(x))
            btn.grid(row=i+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
            self.option_buttons.append(btn)
        
        # Submit button
        self.submit_btn = ttk.Button(quiz_frame, text="Submit Answer", 
                                   command=self.submit_answer, state="disabled")
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Progress info
        self.progress_text = tk.Text(progress_frame, height=4, width=100)
        self.progress_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to start quiz")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        map_frame.columnconfigure(0, weight=1)
        map_frame.rowconfigure(0, weight=1)
        quiz_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
    
    def load_states_data(self):
        """Load states data and draw the map."""
        try:
            # Get states list from API
            response = requests.get(f"{self.api_base_url}/states/list")
            if response.status_code == 200:
                states_data = response.json()
                self.draw_map(states_data)
            else:
                self.draw_demo_map()
        except:
            self.draw_demo_map()
    
    def draw_map(self, states_data):
        """Draw the interactive map with states."""
        self.map_canvas.delete("all")
        
        # Draw state boundaries (simplified)
        for state_name, (x, y) in self.state_coordinates.items():
            # State circle
            self.map_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                      fill="lightgreen", outline="darkgreen", width=2)
            
            # State name
            self.map_canvas.create_text(x, y+25, text=state_name, 
                                      font=("Arial", 8), anchor=tk.N)
            
            # Make it clickable
            self.map_canvas.create_rectangle(x-15, y-15, x+15, y+15, 
                                          outline="", fill="", tags=state_name)
    
    def draw_demo_map(self):
        """Draw a demo map if API is not available."""
        self.map_canvas.delete("all")
        self.map_canvas.create_text(400, 250, text="Demo Map\nClick on states to get questions", 
                                  font=("Arial", 16), anchor=tk.CENTER)
        
        # Draw some demo states
        for i, (state_name, (x, y)) in enumerate(list(self.state_coordinates.items())[:10]):
            self.map_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                      fill="lightgreen", outline="darkgreen", width=2)
            self.map_canvas.create_text(x, y+25, text=state_name, 
                                      font=("Arial", 8), anchor=tk.N)
            self.map_canvas.create_rectangle(x-15, y-15, x+15, y+15, 
                                          outline="", fill="", tags=state_name)
    
    def on_map_click(self, event):
        """Handle map clicks to select states."""
        if not self.current_student:
            messagebox.showwarning("Login Required", "Please login first!")
            return
        
        # Find which state was clicked
        clicked_item = self.map_canvas.find_closest(event.x, event.y)
        tags = self.map_canvas.gettags(clicked_item)
        
        if tags and tags[0] in self.state_coordinates:
            selected_state = tags[0]
            self.start_quiz_for_state(selected_state)
        else:
            self.status_var.set("Click on a state to start quiz")
    
    def login_student(self):
        """Login or create a student."""
        student_id = self.student_id_var.get().strip()
        name = self.student_name_var.get().strip()
        grade = self.grade_var.get().strip()
        
        if not all([student_id, name, grade]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            # Try to create student
            data = {
                "student_id": student_id,
                "name": name,
                "grade": int(grade),
                "favorite_state": "Maharashtra"
            }
            
            response = requests.post(f"{self.api_base_url}/student/create", json=data)
            
            if response.status_code in [200, 201]:
                self.current_student = student_id
                self.status_var.set(f"Logged in as {name}")
                self.load_student_progress()
                messagebox.showinfo("Success", f"Welcome {name}!")
            else:
                messagebox.showerror("Error", "Failed to create student")
                
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")
    
    def start_quiz_for_state(self, state_name):
        """Start a quiz for the selected state."""
        if not self.current_student:
            return
        
        try:
            data = {
                "student_id": self.current_student,
                "state": state_name
            }
            
            response = requests.post(f"{self.api_base_url}/quiz/start", json=data)
            
            if response.status_code == 200:
                quiz_data = response.json()
                self.current_question = quiz_data['question']
                self.session_start_time = quiz_data['session_data']['start_time']
                
                # Display question
                self.display_question(quiz_data['question'])
                self.status_var.set(f"Quiz started for {state_name}")
                
            else:
                messagebox.showerror("Error", f"Failed to start quiz: {response.json().get('error', 'Unknown error')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")
    
    def display_question(self, question):
        """Display the question and options."""
        # Clear previous question
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"State: {question['state']}\n")
        self.question_text.insert(tk.END, f"Difficulty: {question['difficulty']}\n\n")
        self.question_text.insert(tk.END, question['question'])
        
        # Set options
        for i, option in enumerate(question['options']):
            self.option_vars[i].set(f"{i+1}. {option}")
            self.option_buttons[i].config(state="normal")
        
        # Enable submit button
        self.submit_btn.config(state="normal")
        self.selected_answer = None
    
    def select_answer(self, option_index):
        """Select an answer option."""
        self.selected_answer = option_index
        
        # Highlight selected option
        for i, btn in enumerate(self.option_buttons):
            if i == option_index:
                btn.config(style="Accent.TButton")
            else:
                btn.config(style="TButton")
    
    def submit_answer(self):
        """Submit the selected answer."""
        if self.selected_answer is None:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        if not self.current_question or not self.session_start_time:
            return
        
        try:
            data = {
                "student_id": self.current_student,
                "question_id": self.current_question['id'],
                "answer": self.selected_answer,
                "start_time": self.session_start_time,
                "attempts": 1,
                "state": self.current_question['state'],
                "difficulty": self.current_question['difficulty']
            }
            
            response = requests.post(f"{self.api_base_url}/quiz/answer", json=data)
            
            if response.status_code == 200:
                result = response.json()
                
                # Show result
                if result['is_correct']:
                    messagebox.showinfo("Correct!", f"✅ {result['feedback']}")
                else:
                    messagebox.showinfo("Incorrect", f"❌ {result['feedback']}")
                
                # Update progress
                self.load_student_progress()
                
                # Clear question
                self.clear_question()
                
                # Ask if continue
                if messagebox.askyesno("Continue", "Would you like another question from this state?"):
                    self.start_quiz_for_state(self.current_question['state'])
                
            else:
                messagebox.showerror("Error", "Failed to submit answer")
                
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")
    
    def clear_question(self):
        """Clear the current question display."""
        self.question_text.delete(1.0, tk.END)
        for var in self.option_vars:
            var.set("")
        for btn in self.option_buttons:
            btn.config(state="disabled", style="TButton")
        self.submit_btn.config(state="disabled")
        self.current_question = None
        self.selected_answer = None
    
    def load_student_progress(self):
        """Load and display student progress."""
        if not self.current_student:
            return
        
        try:
            response = requests.get(f"{self.api_base_url}/student/progress", 
                                 params={"student_id": self.current_student})
            
            if response.status_code == 200:
                progress = response.json()
                
                progress_text = f"""
Student: {progress['name']} | Grade: {progress['grade']} | Favorite State: {progress['favorite_state']}
Total Questions: {progress['total_questions']} | Correct: {progress['correct_answers']} | Accuracy: {progress['accuracy']:.1%}
Current Difficulty: {progress['current_difficulty']:.1} | Streak: {progress['streak_days']} days
States Visited: {len(progress['states_visited'])} | Last Quiz: {progress['last_quiz_date']}
                """
                
                self.progress_text.delete(1.0, tk.END)
                self.progress_text.insert(1.0, progress_text.strip())
                
        except Exception as e:
            self.progress_text.delete(1.0, tk.END)
            self.progress_text.insert(1.0, f"Error loading progress: {e}")

def main():
    """Main function to run the interface."""
    root = tk.Tk()
    app = IndianMapInterface(root)
    
    # Set up custom styles
    style = ttk.Style()
    style.configure("Accent.TButton", background="lightblue")
    
    root.mainloop()

if __name__ == "__main__":
    main()
