#!/usr/bin/env python3
"""
Demo script for the Adaptive Quiz System.
This demonstrates the core functionality in a simple way.
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_model.adaptive_quiz_model import AdaptiveQuizModel
from ml_model.question_bank import QuestionBank
from ml_model.student_tracker import StudentTracker

def run_demo():
    """Run the adaptive quiz system demo."""
    print("🎓 ADAPTIVE QUIZ SYSTEM DEMO")
    print("=" * 50)
    print("This demo shows how the system adapts question difficulty")
    print("based on student performance using machine learning.")
    print()
    
    # Initialize components
    print("🔄 Initializing system...")
    quiz_model = AdaptiveQuizModel()
    question_bank = QuestionBank()
    student_tracker = StudentTracker()
    print("✅ System ready!")
    print()
    
    # Create demo student
    print("👤 Creating demo student...")
    student_tracker.create_student("demo001", "Alice", 5, "Mathematics")
    print("✅ Student 'Alice' created!")
    print()
    
    # Show initial state
    print("📊 INITIAL STATE:")
    performance = student_tracker.get_student_performance("demo001")
    print(f"Student: {performance['student_id']}")
    print(f"Current Difficulty: {performance['current_difficulty']}")
    print(f"Total Questions: {performance['total_questions']}")
    print(f"Accuracy: {performance['accuracy']:.1%}")
    print()
    
    # Demo quiz session
    print("❓ STARTING DEMO QUIZ SESSION")
    print("=" * 50)
    
    questions_answered = 0
    correct_answers = 0
    
    for round_num in range(1, 6):  # 5 questions
        print(f"\n🔄 ROUND {round_num}")
        print("-" * 30)
        
        # Get current performance
        current_performance = student_tracker.get_student_performance("demo001")
        
        # Predict difficulty using ML
        predicted_difficulty = quiz_model.predict_difficulty(current_performance)
        print(f"🤖 ML Predicted Difficulty: {predicted_difficulty:.1}")
        
        # Get question
        question = question_bank.get_question(difficulty=int(predicted_difficulty))
        if not question:
            print("❌ No questions available at this difficulty level.")
            break
        
        print(f"📚 Subject: {question['subject']}")
        print(f"🎯 Question Difficulty: {question['difficulty']}")
        print(f"❓ Question: {question['question']}")
        print()
        
        # Display options
        for i, option in enumerate(question['options']):
            print(f"{i}. {option}")
        print()
        
        # Simulate student answer (for demo, we'll use a simple pattern)
        # In real usage, this would be user input
        if round_num <= 2:
            # First two questions: correct answers (good performance)
            answer = question['correct_answer']
            is_correct = True
            response_time = 15.0  # Fast response
            attempts = 1
        else:
            # Later questions: mix of correct/incorrect (challenging)
            if round_num == 3:
                answer = (question['correct_answer'] + 1) % 4  # Wrong answer
                is_correct = False
                response_time = 45.0  # Slower response
                attempts = 2
            else:
                answer = question['correct_answer']  # Correct answer
                is_correct = True
                response_time = 25.0  # Medium response
                attempts = 1
        
        print(f"🎯 Simulated Answer: {answer} ({question['options'][answer]})")
        
        # Validate answer
        validation_result, feedback = question_bank.validate_answer(question['id'], answer)
        print(f"✅ Correct Answer: {question['correct_answer']} ({question['options'][question['correct_answer']]})")
        
        if is_correct:
            correct_answers += 1
            print(f"🎉 Result: Correct! {feedback}")
        else:
            print(f"❌ Result: Incorrect. {feedback}")
        
        print(f"⏱️ Response Time: {response_time:.1f}s")
        print(f"🔄 Attempts: {attempts}")
        
        # Record the attempt
        student_tracker.record_quiz_attempt(
            student_id="demo001",
            question_id=question['id'],
            difficulty=question['difficulty'],
            response_time=response_time,
            is_correct=is_correct,
            attempts=attempts
        )
        
        # Update difficulty based on performance
        updated_performance = student_tracker.get_student_performance("demo001")
        new_difficulty = quiz_model.predict_difficulty(updated_performance)
        student_tracker.update_difficulty("demo001", new_difficulty)
        
        print(f"📈 New Difficulty Level: {new_difficulty:.1}")
        
        questions_answered += 1
        
        # Show progress
        current_accuracy = correct_answers / questions_answered
        print(f"📊 Progress: {correct_answers}/{questions_answered} correct ({current_accuracy:.1%})")
        
        time.sleep(1)  # Brief pause for readability
    
    # Final results
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETED!")
    print("=" * 50)
    
    final_performance = student_tracker.get_student_progress("demo001")
    
    print(f"👤 Student: {final_performance['name']}")
    print(f"📚 Subject: {final_performance['subject']}")
    print(f"📊 Final Results:")
    print(f"   Questions Answered: {final_performance['total_questions']}")
    print(f"   Correct Answers: {final_performance['correct_answers']}")
    print(f"   Final Accuracy: {final_performance['accuracy']:.1%}")
    print(f"   Final Difficulty: {final_performance['current_difficulty']:.1}")
    print(f"   Average Response Time: {final_performance['avg_response_time']:.1f}s")
    print(f"   Streak: {final_performance['streak_days']} days")
    
    print("\n🤖 ML MODEL ANALYSIS:")
    print("The system learned from Alice's performance patterns:")
    
    if final_performance['accuracy'] > 0.7:
        print("   ✅ High accuracy → Difficulty increased")
    elif final_performance['accuracy'] < 0.4:
        print("   ❌ Low accuracy → Difficulty decreased")
    else:
        print("   ⚖️ Medium accuracy → Difficulty maintained")
    
    print(f"\n📈 Difficulty Progression:")
    for i, record in enumerate(final_performance['difficulty_progression'][-5:], 1):
        print(f"   Question {i}: Level {record['difficulty']:.1} ({'✅' if record['correct'] else '❌'})")
    
    print("\n💡 KEY FEATURES DEMONSTRATED:")
    print("✅ Adaptive difficulty adjustment")
    print("✅ Performance tracking and analysis")
    print("✅ ML-powered question selection")
    print("✅ Real-time feedback and hints")
    print("✅ Progress monitoring and analytics")
    
    print("\n🚀 This system is ready for Arduino/ESP32 deployment!")
    print("The lightweight design ensures efficient operation on embedded hardware.")

def show_system_info():
    """Show detailed system information."""
    print("\n🔧 SYSTEM INFORMATION:")
    print("=" * 50)
    
    # Initialize components
    quiz_model = AdaptiveQuizModel()
    question_bank = QuestionBank()
    student_tracker = StudentTracker()
    
    # ML Model info
    print("🤖 MACHINE LEARNING MODEL:")
    model_info = quiz_model.get_model_info()
    print(f"   Status: {'✅ Trained' if model_info['is_trained'] else '❌ Not Trained'}")
    print(f"   Type: {model_info['model_type']}")
    print(f"   Features: {model_info['feature_count']}")
    print(f"   Estimators: {model_info['n_estimators']}")
    
    # Question Bank info
    print("\n📚 QUESTION BANK:")
    qb_stats = question_bank.get_statistics()
    print(f"   Total Questions: {qb_stats['total_questions']}")
    print(f"   Subjects: {', '.join(qb_stats['subjects'])}")
    print(f"   Difficulty Levels: {len(qb_stats['difficulty_levels'])}")
    
    # Student Tracker info
    print("\n👨‍🎓 STUDENT TRACKER:")
    students = student_tracker.get_all_students_summary()
    print(f"   Total Students: {len(students)}")
    if students:
        active_students = sum(1 for s in students if s['total_questions'] > 0)
        print(f"   Active Students: {active_students}")
        print(f"   Total Questions Answered: {sum(s['total_questions'] for s in students)}")
    
    print("\n💾 STORAGE:")
    print("   Data stored in CSV files for portability")
    print("   ML model saved as pickle file")
    print("   Lightweight design for embedded systems")

if __name__ == "__main__":
    print("🎓 ADAPTIVE QUIZ SYSTEM - INTERACTIVE DEMO")
    print("=" * 60)
    
    while True:
        print("\n📚 DEMO MENU:")
        print("1. 🚀 Run Full Demo")
        print("2. 🔧 Show System Info")
        print("3. ❌ Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            run_demo()
        elif choice == '2':
            show_system_info()
        elif choice == '3':
            print("\n👋 Thank you for exploring the Adaptive Quiz System!")
            print("Goodbye! 🎓")
            break
        else:
            print("❌ Invalid option. Please select 1-3.")
        
        if choice != '3':
            input("\nPress Enter to continue...")
