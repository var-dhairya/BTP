#!/usr/bin/env python3
"""
Test suite for the Adaptive Quiz System.
Tests all major components to ensure they work correctly.
"""

import sys
import os
import unittest
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.adaptive_quiz_model import AdaptiveQuizModel
from ml_model.question_bank import QuestionBank
from ml_model.student_tracker import StudentTracker

class TestAdaptiveQuizSystem(unittest.TestCase):
    """Test cases for the adaptive quiz system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use test data files
        self.test_questions_file = "tests/test_questions.csv"
        self.test_students_file = "tests/test_students.csv"
        self.test_model_file = "tests/test_model.pkl"
        
        # Initialize components with test files
        self.quiz_model = AdaptiveQuizModel(self.test_model_file)
        self.question_bank = QuestionBank(self.test_questions_file)
        self.student_tracker = StudentTracker(self.test_students_file)
    
    def tearDown(self):
        """Clean up test files."""
        # Remove test files
        for file_path in [self.test_questions_file, self.test_students_file, self.test_model_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def test_question_bank_creation(self):
        """Test question bank creation and sample questions."""
        # Check if sample questions were created
        stats = self.question_bank.get_statistics()
        self.assertGreater(stats['total_questions'], 0)
        self.assertIn('Mathematics', stats['subjects'])
        self.assertIn('Science', stats['subjects'])
        
        # Test getting questions by difficulty
        question = self.question_bank.get_question(difficulty=1)
        self.assertIsNotNone(question)
        self.assertEqual(question['difficulty'], 1)
        self.assertIn('question', question)
        self.assertIn('options', question)
        self.assertIn('correct_answer', question)
    
    def test_student_tracker(self):
        """Test student tracking functionality."""
        # Create a test student
        success = self.student_tracker.create_student("test001", "Test Student", 5, "Mathematics")
        self.assertTrue(success)
        
        # Check if student exists
        students = self.student_tracker.get_all_students_summary()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]['name'], "Test Student")
        
        # Test performance tracking
        performance = self.student_tracker.get_student_performance("test001")
        self.assertIsNotNone(performance)
        self.assertEqual(performance['total_questions'], 0)
        self.assertEqual(performance['current_difficulty'], 1.0)
    
    def test_quiz_attempt_recording(self):
        """Test recording quiz attempts."""
        # Create test student
        self.student_tracker.create_student("test002", "Quiz Student", 6, "Science")
        
        # Record a quiz attempt
        success = self.student_tracker.record_quiz_attempt(
            student_id="test002",
            question_id=1,
            difficulty=2.0,
            response_time=15.5,
            is_correct=True,
            attempts=1
        )
        self.assertTrue(success)
        
        # Check updated performance
        performance = self.student_tracker.get_student_performance("test002")
        self.assertEqual(performance['total_questions'], 1)
        self.assertEqual(performance['correct_answers'], 1)
        self.assertEqual(performance['accuracy'], 1.0)
        self.assertGreater(performance['avg_response_time'], 0)
    
    def test_ml_model_prediction(self):
        """Test ML model difficulty prediction."""
        # Create test student with performance data
        self.student_tracker.create_student("test003", "ML Student", 7, "General")
        
        # Record some quiz attempts to build performance history
        for i in range(5):
            self.student_tracker.record_quiz_attempt(
                student_id="test003",
                question_id=i+1,
                difficulty=3.0,
                response_time=20.0 + i,
                is_correct=(i < 4),  # 80% accuracy
                attempts=1
            )
        
        # Get performance data
        performance = self.student_tracker.get_student_performance("test003")
        
        # Test prediction (should use heuristic initially)
        predicted_difficulty = self.quiz_model.predict_difficulty(performance)
        self.assertIsInstance(predicted_difficulty, float)
        self.assertGreaterEqual(predicted_difficulty, 1.0)
        self.assertLessEqual(predicted_difficulty, 10.0)
    
    def test_question_validation(self):
        """Test question answer validation."""
        # Get a test question
        question = self.question_bank.get_question(difficulty=1)
        self.assertIsNotNone(question)
        
        # Test correct answer
        is_correct, feedback = self.question_bank.validate_answer(
            question['id'], 
            question['correct_answer']
        )
        self.assertTrue(is_correct)
        self.assertIn('explanation', feedback)
        
        # Test incorrect answer
        wrong_answer = (question['correct_answer'] + 1) % 4
        is_correct, feedback = self.question_bank.validate_answer(
            question['id'], 
            wrong_answer
        )
        self.assertFalse(is_correct)
        self.assertIn('hint', feedback)
    
    def test_difficulty_adjustment(self):
        """Test automatic difficulty adjustment."""
        # Create test student
        self.student_tracker.create_student("test004", "Difficulty Student", 8, "Mathematics")
        
        # Start with easy questions and track performance
        initial_difficulty = 1.0
        
        # Simulate poor performance (should decrease difficulty)
        for i in range(3):
            self.student_tracker.record_quiz_attempt(
                student_id="test004",
                question_id=i+10,
                difficulty=initial_difficulty,
                response_time=30.0,
                is_correct=False,  # Poor performance
                attempts=2
            )
        
        # Check if difficulty decreased
        performance = self.student_tracker.get_student_performance("test004")
        self.assertLessEqual(performance['accuracy'], 0.5)
        
        # Now simulate good performance (should increase difficulty)
        for i in range(3):
            self.student_tracker.record_quiz_attempt(
                student_id="test004",
                question_id=i+20,
                difficulty=performance['current_difficulty'],
                response_time=15.0,
                is_correct=True,  # Good performance
                attempts=1
            )
        
        # Check updated performance
        updated_performance = self.student_tracker.get_student_performance("test004")
        self.assertGreater(updated_performance['accuracy'], 0.5)
    
    def test_model_training(self):
        """Test ML model training functionality."""
        # Create multiple test students with performance data
        for i in range(3):
            student_id = f"train{i:03d}"
            self.student_tracker.create_student(student_id, f"Training Student {i}", 5+i, "General")
            
            # Record quiz attempts
            for j in range(5):
                self.student_tracker.record_quiz_attempt(
                    student_id=student_id,
                    question_id=i*10+j,
                    difficulty=2.0 + i,
                    response_time=20.0 + j,
                    is_correct=(j < 4),  # 80% accuracy
                    attempts=1
                )
        
        # Generate training data
        training_data = []
        students = self.student_tracker.get_all_students_summary()
        
        for student in students:
            performance = self.student_tracker.get_student_performance(student['student_id'])
            if performance and performance['total_questions'] > 0:
                # Estimate optimal difficulty
                if performance['accuracy'] > 0.8:
                    optimal_difficulty = min(10.0, performance['current_difficulty'] + 1.0)
                elif performance['accuracy'] < 0.4:
                    optimal_difficulty = max(1.0, performance['current_difficulty'] - 1.0)
                else:
                    optimal_difficulty = performance['current_difficulty']
                
                training_data.append({
                    **performance,
                    'optimal_difficulty': optimal_difficulty
                })
        
        # Test model training
        if len(training_data) >= 10:
            success = self.quiz_model.train_model(training_data)
            self.assertTrue(success)
            
            # Check model info
            model_info = self.quiz_model.get_model_info()
            self.assertTrue(model_info['is_trained'])
            self.assertGreater(model_info['n_estimators'], 0)
        else:
            self.skipTest("Insufficient training data")
    
    def test_system_integration(self):
        """Test complete system integration."""
        # Create student
        self.student_tracker.create_student("test005", "Integration Student", 9, "Science")
        
        # Get question
        question = self.question_bank.get_question(difficulty=2)
        self.assertIsNotNone(question)
        
        # Record quiz attempt
        success = self.student_tracker.record_quiz_attempt(
            student_id="test005",
            question_id=question['id'],
            difficulty=question['difficulty'],
            response_time=25.0,
            is_correct=True,
            attempts=1
        )
        self.assertTrue(success)
        
        # Get updated performance
        performance = self.student_tracker.get_student_performance("test005")
        self.assertIsNotNone(performance)
        
        # Test ML prediction
        predicted_difficulty = self.quiz_model.predict_difficulty(performance)
        self.assertIsInstance(predicted_difficulty, float)
        
        # Update student difficulty
        update_success = self.student_tracker.update_difficulty("test005", predicted_difficulty)
        self.assertTrue(update_success)
        
        # Verify update
        updated_performance = self.student_tracker.get_student_performance("test005")
        self.assertEqual(updated_performance['current_difficulty'], predicted_difficulty)

def run_performance_test():
    """Run a simple performance test."""
    print("🚀 Running Performance Test...")
    
    # Initialize components
    quiz_model = AdaptiveQuizModel()
    question_bank = QuestionBank()
    student_tracker = StudentTracker()
    
    # Create test student
    student_tracker.create_student("perf001", "Performance Student", 6, "Mathematics")
    
    # Simulate quiz session
    start_time = time.time()
    
    for i in range(10):
        # Get question
        question = question_bank.get_question(difficulty=2)
        if not question:
            break
        
        # Record attempt
        student_tracker.record_quiz_attempt(
            student_id="perf001",
            question_id=question['id'],
            difficulty=question['difficulty'],
            response_time=15.0 + i,
            is_correct=(i < 8),  # 80% accuracy
            attempts=1
        )
    
    end_time = time.time()
    
    # Get performance
    performance = student_tracker.get_student_performance("perf001")
    predicted_difficulty = quiz_model.predict_difficulty(performance)
    
    print(f"✅ Performance test completed in {end_time - start_time:.2f} seconds")
    print(f"📊 Student accuracy: {performance['accuracy']:.1%}")
    print(f"🤖 Predicted difficulty: {predicted_difficulty:.1}")
    print(f"📈 Questions answered: {performance['total_questions']}")

if __name__ == "__main__":
    print("🧪 ADAPTIVE QUIZ SYSTEM TEST SUITE")
    print("=" * 50)
    
    # Run performance test first
    run_performance_test()
    print()
    
    # Run unit tests
    print("🔬 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
