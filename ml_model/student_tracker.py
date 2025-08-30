import csv
import time
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta

class StudentTracker:
    """
    Tracks and analyzes student performance for Indian states geography quiz system.
    Designed to be lightweight and efficient for embedded systems.
    """
    
    def __init__(self, students_file: str = "data/students.csv"):
        self.students_file = students_file
        self.students = {}
        self.performance_history = {}
        
        # Load existing student data
        self.load_students()
    
    def load_students(self) -> bool:
        """Load student data from CSV file."""
        try:
            if not os.path.exists(self.students_file):
                return False
            
            with open(self.students_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student_id = row['student_id']
                    self.students[student_id] = {
                        'name': row['name'],
                        'grade': int(row['grade']),
                        'favorite_state': row['favorite_state'],
                        'current_difficulty': float(row['current_difficulty']),
                        'total_questions': int(row['total_questions']),
                        'correct_answers': int(row['correct_answers']),
                        'total_attempts': int(row['total_attempts']),
                        'avg_response_time': float(row['avg_response_time']),
                        'last_quiz_date': row['last_quiz_date'],
                        'streak_days': int(row['streak_days']),
                        'states_visited': row['states_visited'].split('|') if row['states_visited'] else []
                    }
                    
                    # Initialize performance history
                    if student_id not in self.performance_history:
                        self.performance_history[student_id] = []
            
            return True
            
        except Exception as e:
            print(f"Error loading students: {e}")
            return False
    
    def save_students(self) -> bool:
        """Save student data to CSV file."""
        try:
            os.makedirs(os.path.dirname(self.students_file), exist_ok=True)
            
            with open(self.students_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['student_id', 'name', 'grade', 'favorite_state', 'current_difficulty',
                            'total_questions', 'correct_answers', 'total_attempts',
                            'avg_response_time', 'last_quiz_date', 'streak_days', 'states_visited']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for student_id, data in self.students.items():
                    writer.writerow({
                        'student_id': student_id,
                        'name': data['name'],
                        'grade': data['grade'],
                        'favorite_state': data['favorite_state'],
                        'current_difficulty': data['current_difficulty'],
                        'total_questions': data['total_questions'],
                        'correct_answers': data['correct_answers'],
                        'total_attempts': data['total_attempts'],
                        'avg_response_time': data['avg_response_time'],
                        'last_quiz_date': data['last_quiz_date'],
                        'streak_days': data['streak_days'],
                        'states_visited': '|'.join(data['states_visited'])
                    })
            
            return True
            
        except Exception as e:
            print(f"Error saving students: {e}")
            return False
    
    def create_student(self, student_id: str, name: str, grade: int, 
                      favorite_state: str = "General") -> bool:
        """Create a new student profile."""
        if student_id in self.students:
            print(f"Student {student_id} already exists")
            return False
        
        self.students[student_id] = {
            'name': name,
            'grade': grade,
            'favorite_state': favorite_state,
            'current_difficulty': 1.0,  # Start with easiest difficulty
            'total_questions': 0,
            'correct_answers': 0,
            'total_attempts': 0,
            'avg_response_time': 0.0,
            'last_quiz_date': datetime.now().strftime('%Y-%m-%d'),
            'streak_days': 0,
            'states_visited': []
        }
        
        self.performance_history[student_id] = []
        self.save_students()
        return True
    
    def record_quiz_attempt(self, student_id: str, question_id: int, 
                           difficulty: float, response_time: float, 
                           is_correct: bool, attempts: int = 1, state: str = None) -> bool:
        """
        Record a quiz attempt for a student.
        Updates performance metrics and history.
        """
        if student_id not in self.students:
            print(f"Student {student_id} not found")
            return False
        
        try:
            student = self.students[student_id]
            
            # Update basic metrics
            student['total_questions'] += 1
            student['total_attempts'] += attempts
            
            if is_correct:
                student['correct_answers'] += 1
            
            # Update average response time
            if student['total_questions'] == 1:
                student['avg_response_time'] = response_time
            else:
                # Weighted average (more weight to recent attempts)
                weight = 0.3
                student['avg_response_time'] = (
                    (1 - weight) * student['avg_response_time'] + 
                    weight * response_time
                )
            
            # Update streak
            today = datetime.now().strftime('%Y-%m-%d')
            if student['last_quiz_date'] == today:
                # Already quizzed today, don't update streak
                pass
            elif student['last_quiz_date'] == (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'):
                # Consecutive day
                student['streak_days'] += 1
            else:
                # Break in streak
                student['streak_days'] = 1
            
            student['last_quiz_date'] = today
            
            # Track states visited
            if state and state not in student['states_visited']:
                student['states_visited'].append(state)
            
            # Record performance history
            performance_record = {
                'timestamp': datetime.now().isoformat(),
                'question_id': question_id,
                'difficulty': difficulty,
                'response_time': response_time,
                'is_correct': is_correct,
                'attempts': attempts,
                'state': state
            }
            
            if student_id not in self.performance_history:
                self.performance_history[student_id] = []
            
            self.performance_history[student_id].append(performance_record)
            
            # Keep only last 100 records to save memory
            if len(self.performance_history[student_id]) > 100:
                self.performance_history[student_id] = self.performance_history[student_id][-100:]
            
            self.save_students()
            return True
            
        except Exception as e:
            print(f"Error recording quiz attempt: {e}")
            return False
    
    def get_student_performance(self, student_id: str) -> Optional[Dict]:
        """
        Get comprehensive performance data for a student.
        Returns data formatted for ML model input.
        """
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        history = self.performance_history.get(student_id, [])
        
        if not history:
            # No history, return basic info
            return {
                'student_id': student_id,
                'current_difficulty': student['current_difficulty'],
                'accuracy': 0.5,  # Default
                'avg_response_time': student['avg_response_time'],
                'avg_attempts': 1.0,
                'recent_accuracy': 0.5,
                'total_questions': student['total_questions'],
                'states_visited_count': len(student['states_visited'])
            }
        
        # Calculate recent performance (last 10 questions)
        recent_history = history[-10:] if len(history) >= 10 else history
        recent_correct = sum(1 for record in recent_history if record['is_correct'])
        recent_accuracy = recent_correct / len(recent_history)
        
        # Calculate average attempts
        avg_attempts = sum(record['attempts'] for record in history) / len(history)
        
        # Calculate overall accuracy
        overall_accuracy = student['correct_answers'] / max(student['total_questions'], 1)
        
        return {
            'student_id': student_id,
            'current_difficulty': student['current_difficulty'],
            'accuracy': overall_accuracy,
            'avg_response_time': student['avg_response_time'],
            'avg_attempts': avg_attempts,
            'recent_accuracy': recent_accuracy,
            'total_questions': student['total_questions'],
            'streak_days': student['streak_days'],
            'grade': student['grade'],
            'favorite_state': student['favorite_state'],
            'states_visited_count': len(student['states_visited'])
        }
    
    def get_state_performance(self, student_id: str, state: str) -> Optional[Dict]:
        """Get performance data for a specific state."""
        if student_id not in self.performance_history:
            return None
        
        state_history = [
            record for record in self.performance_history[student_id]
            if record.get('state') == state
        ]
        
        if not state_history:
            return None
        
        total_questions = len(state_history)
        correct_answers = sum(1 for record in state_history if record['is_correct'])
        accuracy = correct_answers / total_questions
        avg_response_time = sum(record['response_time'] for record in state_history) / total_questions
        avg_attempts = sum(record['attempts'] for record in state_history) / total_questions
        
        return {
            'state': state,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': accuracy,
            'avg_response_time': avg_response_time,
            'avg_attempts': avg_attempts
        }
    
    def get_states_progress(self, student_id: str) -> Dict[str, Dict]:
        """Get progress for all states visited by the student."""
        if student_id not in self.students:
            return {}
        
        student = self.students[student_id]
        states_progress = {}
        
        for state in student['states_visited']:
            state_perf = self.get_state_performance(student_id, state)
            if state_perf:
                states_progress[state] = state_perf
        
        return states_progress
    
    def update_difficulty(self, student_id: str, new_difficulty: float) -> bool:
        """Update the current difficulty level for a student."""
        if student_id not in self.students:
            return False
        
        self.students[student_id]['current_difficulty'] = new_difficulty
        self.save_students()
        return True
    
    def get_student_progress(self, student_id: str) -> Optional[Dict]:
        """Get detailed progress information for a student."""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        history = self.performance_history.get(student_id, [])
        
        # Calculate state-wise performance
        states_progress = self.get_states_progress(student_id)
        
        # Calculate difficulty progression
        difficulty_progression = []
        for record in history:
            difficulty_progression.append({
                'date': record['timestamp'][:10],
                'difficulty': record['difficulty'],
                'correct': record['is_correct'],
                'state': record.get('state', 'Unknown')
            })
        
        return {
            'student_id': student_id,
            'name': student['name'],
            'grade': student['grade'],
            'favorite_state': student['favorite_state'],
            'current_difficulty': student['current_difficulty'],
            'total_questions': student['total_questions'],
            'correct_answers': student['correct_answers'],
            'accuracy': student['correct_answers'] / max(student['total_questions'], 1),
            'avg_response_time': student['avg_response_time'],
            'streak_days': student['streak_days'],
            'last_quiz_date': student['last_quiz_date'],
            'difficulty_progression': difficulty_progression[-20:],  # Last 20 questions
            'total_attempts': student['total_attempts'],
            'states_visited': student['states_visited'],
            'states_progress': states_progress
        }
    
    def get_all_students_summary(self) -> List[Dict]:
        """Get summary of all students' performance."""
        summary = []
        
        for student_id, student in self.students.items():
            performance = self.get_student_performance(student_id)
            if performance:
                summary.append({
                    'student_id': student_id,
                    'name': student['name'],
                    'grade': student['grade'],
                    'favorite_state': student['favorite_state'],
                    'current_difficulty': student['current_difficulty'],
                    'total_questions': student['total_questions'],
                    'accuracy': performance['accuracy'],
                    'streak_days': student['streak_days'],
                    'states_visited_count': len(student['states_visited'])
                })
        
        return summary
    
    def get_performance_analytics(self, student_id: str, days: int = 30) -> Dict:
        """Get performance analytics for a specific time period."""
        if student_id not in self.performance_history:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_history = [
            record for record in self.performance_history[student_id]
            if datetime.fromisoformat(record['timestamp']) > cutoff_date
        ]
        
        if not recent_history:
            return {}
        
        # Calculate analytics
        total_questions = len(recent_history)
        correct_answers = sum(1 for record in recent_history if record['is_correct'])
        accuracy = correct_answers / total_questions
        
        avg_response_time = sum(record['response_time'] for record in recent_history) / total_questions
        avg_difficulty = sum(record['difficulty'] for record in recent_history) / total_questions
        
        # State-wise analytics
        states_visited = set(record.get('state') for record in recent_history if record.get('state'))
        
        # Difficulty trend
        difficulties = [record['difficulty'] for record in recent_history]
        difficulty_trend = 'increasing' if difficulties[-1] > difficulties[0] else 'decreasing' if difficulties[-1] < difficulties[0] else 'stable'
        
        return {
            'period_days': days,
            'total_questions': total_questions,
            'accuracy': accuracy,
            'avg_response_time': avg_response_time,
            'avg_difficulty': avg_difficulty,
            'difficulty_trend': difficulty_trend,
            'questions_per_day': total_questions / days,
            'states_visited': list(states_visited),
            'unique_states_count': len(states_visited)
        }
