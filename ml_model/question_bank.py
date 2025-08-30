import csv
import random
from typing import Dict, List, Optional, Tuple
import os

class QuestionBank:
    """
    Manages a database of questions about Indian states and union territories.
    Designed to be lightweight and efficient for embedded systems.
    """
    
    def __init__(self, questions_file: str = "data/questions.csv"):
        self.questions_file = questions_file
        self.questions = {}
        self.difficulty_levels = {
            1: "Very Easy",
            2: "Easy", 
            3: "Easy-Medium",
            4: "Medium",
            5: "Medium-Hard",
            6: "Hard",
            7: "Hard-Advanced",
            8: "Advanced",
            9: "Very Advanced",
            10: "Expert"
        }
        
        # Indian States and Union Territories
        self.states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
            "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
            "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
            "Uttar Pradesh", "Uttarakhand", "West Bengal"
        ]
        
        self.union_territories = [
            "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
            "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
        ]
        
        self.all_regions = self.states + self.union_territories
        
        # Load questions from file
        self.load_questions()
        
        # If no questions exist, create sample questions
        if not self.questions:
            self.create_sample_questions()
    
    def load_questions(self) -> bool:
        """Load questions from CSV file."""
        try:
            if not os.path.exists(self.questions_file):
                return False
            
            with open(self.questions_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    question_id = int(row['id'])
                    difficulty = int(row['difficulty'])
                    state = row['state']
                    
                    if difficulty not in self.questions:
                        self.questions[difficulty] = {}
                    
                    if state not in self.questions[difficulty]:
                        self.questions[difficulty][state] = []
                    
                    question_data = {
                        'id': question_id,
                        'question': row['question'],
                        'options': row['options'].split('|'),
                        'correct_answer': int(row['correct_answer']),
                        'explanation': row['explanation'],
                        'hint': row['hint'],
                        'difficulty': difficulty,
                        'state': state
                    }
                    
                    self.questions[difficulty][state].append(question_data)
            
            return True
            
        except Exception as e:
            print(f"Error loading questions: {e}")
            return False
    
    def save_questions(self) -> bool:
        """Save questions to CSV file."""
        try:
            os.makedirs(os.path.dirname(self.questions_file), exist_ok=True)
            
            with open(self.questions_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'question', 'options', 'correct_answer', 
                            'explanation', 'hint', 'difficulty', 'state']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for difficulty in self.questions:
                    for state in self.questions[difficulty]:
                        for question in self.questions[difficulty][state]:
                            writer.writerow({
                                'id': question['id'],
                                'question': question['question'],
                                'options': '|'.join(question['options']),
                                'correct_answer': question['correct_answer'],
                                'explanation': question['explanation'],
                                'hint': question['hint'],
                                'difficulty': question['difficulty'],
                                'state': question['state']
                            })
            
            return True
            
        except Exception as e:
            print(f"Error saving questions: {e}")
            return False
    
    def create_sample_questions(self) -> None:
        """Create sample questions about Indian states for demonstration."""
        sample_questions = [
            # Maharashtra - Easy
            {
                'id': 1, 'question': 'What is the capital of Maharashtra?', 
                'options': ['Mumbai', 'Pune', 'Nagpur', 'Thane'],
                'correct_answer': 0, 'explanation': 'Mumbai is the capital and financial capital of India', 
                'hint': 'Think of the city with the Gateway of India',
                'difficulty': 1, 'state': 'Maharashtra'
            },
            {
                'id': 2, 'question': 'Which famous monument is located in Maharashtra?', 
                'options': ['Taj Mahal', 'Gateway of India', 'Red Fort', 'Qutub Minar'],
                'correct_answer': 1, 'explanation': 'Gateway of India is located in Mumbai, Maharashtra', 
                'hint': 'It\'s a famous arch in Mumbai',
                'difficulty': 2, 'state': 'Maharashtra'
            },
            
            # Karnataka - Easy
            {
                'id': 3, 'question': 'What is the capital of Karnataka?', 
                'options': ['Bangalore', 'Mysore', 'Mangalore', 'Hubli'],
                'correct_answer': 0, 'explanation': 'Bangalore (Bengaluru) is the capital of Karnataka', 
                'hint': 'Known as the Silicon Valley of India',
                'difficulty': 1, 'state': 'Karnataka'
            },
            
            # Tamil Nadu - Easy
            {
                'id': 4, 'question': 'Which temple city is famous in Tamil Nadu?', 
                'options': ['Varanasi', 'Madurai', 'Amritsar', 'Puri'],
                'correct_answer': 1, 'explanation': 'Madurai is famous for the Meenakshi Temple', 
                'hint': 'Famous for its temple with thousands of pillars',
                'difficulty': 2, 'state': 'Tamil Nadu'
            },
            
            # Kerala - Easy
            {
                'id': 5, 'question': 'What is Kerala famous for?', 
                'options': ['Deserts', 'Backwaters', 'Mountains', 'Plains'],
                'correct_answer': 1, 'explanation': 'Kerala is famous for its beautiful backwaters and houseboats', 
                'hint': 'Think of water-based tourism',
                'difficulty': 2, 'state': 'Kerala'
            },
            
            # Rajasthan - Easy
            {
                'id': 6, 'question': 'What is the capital of Rajasthan?', 
                'options': ['Jaipur', 'Jodhpur', 'Udaipur', 'Bikaner'],
                'correct_answer': 0, 'explanation': 'Jaipur is the capital of Rajasthan, known as the Pink City', 
                'hint': 'Known as the Pink City',
                'difficulty': 1, 'state': 'Rajasthan'
            },
            
            # Gujarat - Easy
            {
                'id': 7, 'question': 'Which is the largest city in Gujarat?', 
                'options': ['Surat', 'Ahmedabad', 'Vadodara', 'Rajkot'],
                'correct_answer': 1, 'explanation': 'Ahmedabad is the largest city in Gujarat', 
                'hint': 'Famous for its textile industry',
                'difficulty': 2, 'state': 'Gujarat'
            },
            
            # Uttar Pradesh - Easy
            {
                'id': 8, 'question': 'Which famous monument is in Uttar Pradesh?', 
                'options': ['Taj Mahal', 'Gateway of India', 'India Gate', 'Charminar'],
                'correct_answer': 0, 'explanation': 'Taj Mahal is located in Agra, Uttar Pradesh', 
                'hint': 'One of the Seven Wonders of the World',
                'difficulty': 1, 'state': 'Uttar Pradesh'
            },
            
            # West Bengal - Easy
            {
                'id': 9, 'question': 'What is the capital of West Bengal?', 
                'options': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol'],
                'correct_answer': 0, 'explanation': 'Kolkata is the capital of West Bengal', 
                'hint': 'Formerly known as Calcutta',
                'difficulty': 1, 'state': 'West Bengal'
            },
            
            # Delhi - Easy
            {
                'id': 10, 'question': 'What is the Red Fort famous for?', 
                'options': ['Independence Day celebrations', 'Republic Day parade', 'Both', 'Neither'],
                'correct_answer': 2, 'explanation': 'Red Fort is famous for both Independence Day and Republic Day celebrations', 
                'hint': 'Prime Minister hoists the flag here on Independence Day',
                'difficulty': 2, 'state': 'Delhi'
            },
            
            # Maharashtra - Medium
            {
                'id': 11, 'question': 'Which hill station is known as the Queen of the Deccan?', 
                'options': ['Mahabaleshwar', 'Lonavala', 'Khandala', 'Matheran'],
                'correct_answer': 0, 'explanation': 'Mahabaleshwar is known as the Queen of the Deccan', 
                'hint': 'Famous for strawberries and scenic beauty',
                'difficulty': 4, 'state': 'Maharashtra'
            },
            
            # Karnataka - Medium
            {
                'id': 12, 'question': 'Which ancient empire had its capital in Karnataka?', 
                'options': ['Maurya', 'Gupta', 'Vijayanagara', 'Chola'],
                'correct_answer': 2, 'explanation': 'Vijayanagara Empire had its capital in Hampi, Karnataka', 
                'hint': 'Famous for the ruins at Hampi',
                'difficulty': 4, 'state': 'Karnataka'
            },
            
            # Tamil Nadu - Medium
            {
                'id': 13, 'question': 'Which dance form originated in Tamil Nadu?', 
                'options': ['Kathak', 'Bharatanatyam', 'Kuchipudi', 'Odissi'],
                'correct_answer': 1, 'explanation': 'Bharatanatyam originated in Tamil Nadu', 
                'hint': 'One of the oldest classical dance forms',
                'difficulty': 4, 'state': 'Tamil Nadu'
            },
            
            # Kerala - Medium
            {
                'id': 14, 'question': 'What is the traditional martial art of Kerala?', 
                'options': ['Kalaripayattu', 'Silambam', 'Gatka', 'Thang-ta'],
                'correct_answer': 0, 'explanation': 'Kalaripayattu is the traditional martial art of Kerala', 
                'hint': 'One of the oldest martial arts in the world',
                'difficulty': 4, 'state': 'Kerala'
            },
            
            # Rajasthan - Medium
            {
                'id': 15, 'question': 'Which fort is known as the Golden Fort?', 
                'options': ['Amber Fort', 'Jaisalmer Fort', 'Chittorgarh Fort', 'Ranthambore Fort'],
                'correct_answer': 1, 'explanation': 'Jaisalmer Fort is known as the Golden Fort due to its yellow sandstone', 
                'hint': 'Located in the Thar Desert',
                'difficulty': 4, 'state': 'Rajasthan'
            }
        ]
        
        # Add questions to the bank
        for question_data in sample_questions:
            difficulty = question_data['difficulty']
            state = question_data['state']
            
            if difficulty not in self.questions:
                self.questions[difficulty] = {}
            
            if state not in self.questions[difficulty]:
                self.questions[difficulty][state] = []
            
            self.questions[difficulty][state].append(question_data)
        
        # Save to file
        self.save_questions()
    
    def get_question(self, difficulty: int, state: str = None, 
                    exclude_ids: List[int] = None) -> Optional[Dict]:
        """
        Get a random question of specified difficulty and state.
        Excludes previously asked questions.
        """
        if difficulty not in self.questions:
            return None
        
        if state and state not in self.questions[difficulty]:
            return None
        
        available_questions = []
        
        if state:
            # Get questions from specific state
            available_questions = self.questions[difficulty][state]
        else:
            # Get questions from all states at this difficulty
            for st in self.questions[difficulty]:
                available_questions.extend(self.questions[difficulty][st])
        
        if not available_questions:
            return None
        
        # Filter out previously asked questions
        if exclude_ids:
            available_questions = [q for q in available_questions if q['id'] not in exclude_ids]
        
        if not available_questions:
            return None
        
        # Return random question
        return random.choice(available_questions)
    
    def get_questions_by_difficulty_range(self, min_difficulty: int, max_difficulty: int,
                                        state: str = None, count: int = 1) -> List[Dict]:
        """Get multiple questions within a difficulty range."""
        questions = []
        
        for difficulty in range(min_difficulty, max_difficulty + 1):
            if difficulty in self.questions:
                if state:
                    if state in self.questions[difficulty]:
                        questions.extend(self.questions[difficulty][state])
                else:
                    for st in self.questions[difficulty]:
                        questions.extend(self.questions[difficulty][st])
        
        # Shuffle and return requested count
        random.shuffle(questions)
        return questions[:count]
    
    def get_questions_by_state(self, state: str, difficulty: int = None, count: int = 1) -> List[Dict]:
        """Get questions for a specific state."""
        questions = []
        
        if difficulty:
            # Get questions of specific difficulty for the state
            if difficulty in self.questions and state in self.questions[difficulty]:
                questions = self.questions[difficulty][state]
        else:
            # Get questions of all difficulties for the state
            for diff in self.questions:
                if state in self.questions[diff]:
                    questions.extend(self.questions[diff][state])
        
        # Shuffle and return requested count
        random.shuffle(questions)
        return questions[:count]
    
    def add_question(self, question_data: Dict) -> bool:
        """Add a new question to the bank."""
        try:
            difficulty = question_data['difficulty']
            state = question_data['state']
            
            if difficulty not in self.questions:
                self.questions[difficulty] = {}
            
            if state not in self.questions[difficulty]:
                self.questions[difficulty][state] = []
            
            # Generate new ID
            max_id = 0
            for diff in self.questions.values():
                for st in diff.values():
                    for q in st:
                        max_id = max(max_id, q['id'])
            
            question_data['id'] = max_id + 1
            
            self.questions[difficulty][state].append(question_data)
            self.save_questions()
            return True
            
        except Exception as e:
            print(f"Error adding question: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get statistics about the question bank."""
        stats = {
            'total_questions': 0,
            'questions_by_difficulty': {},
            'questions_by_state': {},
            'difficulty_levels': self.difficulty_levels,
            'states': self.states,
            'union_territories': self.union_territories,
            'all_regions': self.all_regions
        }
        
        for difficulty in self.questions:
            stats['questions_by_difficulty'][difficulty] = 0
            for state in self.questions[difficulty]:
                count = len(self.questions[difficulty][state])
                stats['questions_by_difficulty'][difficulty] += count
                stats['total_questions'] += count
                
                if state not in stats['questions_by_state']:
                    stats['questions_by_state'][state] = 0
                stats['questions_by_state'][state] += count
        
        return stats
    
    def validate_answer(self, question_id: int, student_answer: int) -> Tuple[bool, str]:
        """Validate a student's answer and return feedback."""
        # Find the question
        question = None
        for difficulty in self.questions.values():
            for state in difficulty.values():
                for q in state:
                    if q['id'] == question_id:
                        question = q
                        break
                if question:
                    break
            if question:
                break
        
        if not question:
            return False, "Question not found"
        
        is_correct = (student_answer == question['correct_answer'])
        feedback = question['explanation'] if is_correct else question['hint']
        
        return is_correct, feedback
    
    def get_states_with_questions(self) -> List[str]:
        """Get list of states that have questions."""
        states_with_questions = set()
        for difficulty in self.questions.values():
            states_with_questions.update(difficulty.keys())
        return list(states_with_questions)
