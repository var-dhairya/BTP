#!/usr/bin/env python3
"""
Main application for the Indian States Geography Quiz System with Machine Learning.
This demonstrates the core functionality of the system.
"""

import time
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_model.adaptive_quiz_model import AdaptiveQuizModel
from ml_model.question_bank import QuestionBank
from ml_model.student_tracker import StudentTracker

def print_banner():
    """Print a welcome banner."""
    print("=" * 70)
    print("🇮🇳 INDIAN STATES GEOGRAPHY QUIZ SYSTEM WITH MACHINE LEARNING 🇮🇳")
    print("=" * 70)
    print("An intelligent quiz system that personalizes questions about Indian states")
    print("based on student performance using ML algorithms")
    print("=" * 70)
    print()

def print_menu():
    """Print the main menu options."""
    print("📚 MAIN MENU:")
    print("1. 🧠 Train ML Model")
    print("2. 👨‍🎓 Manage Students")
    print("3. 🗺️ Take State Geography Quiz")
    print("4. 📊 View Analytics")
    print("5. 🔧 System Status")
    print("6. 🚀 Start API Server")
    print("7. 🖥️ Launch Interactive Map Interface")
    print("8. ❌ Exit")
    print()

def train_ml_model(quiz_model, student_tracker):
    """Train the machine learning model."""
    print("🧠 Training ML Model...")
    print("This will analyze student performance data to improve question difficulty prediction.")
    print()
    
    # Check if we have enough data
    students = student_tracker.get_all_students_summary()
    if len(students) < 2:
        print("❌ Need at least 2 students with quiz history to train the model.")
        print("Please create some students and take quizzes first.")
        return
    
    # Generate training data
    training_data = []
    for student in students:
        performance = student_tracker.get_student_performance(student['student_id'])
        if performance and performance['total_questions'] > 0:
            # Estimate optimal difficulty based on performance
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
    
    print(f"📊 Generated {len(training_data)} training samples")
    
    if len(training_data) < 10:
        print("❌ Need at least 10 samples to train effectively.")
        print("Continue taking quizzes to gather more data.")
        return
    
    # Train the model
    print("🔄 Training in progress...")
    success = quiz_model.train_model(training_data)
    
    if success:
        print("✅ Model trained successfully!")
        model_info = quiz_model.get_model_info()
        print(f"📈 Model Type: {model_info['model_type']}")
        print(f"🔢 Estimators: {model_info['n_estimators']}")
        print(f"🎯 Features: {model_info['feature_count']}")
    else:
        print("❌ Model training failed. Check error logs.")

def manage_students(student_tracker):
    """Manage student profiles."""
    while True:
        print("\n👨‍🎓 STUDENT MANAGEMENT:")
        print("1. 👤 Create New Student")
        print("2. 📋 List All Students")
        print("3. 📊 View Student Progress")
        print("4. 🗺️ View State-wise Progress")
        print("5. 🔙 Back to Main Menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            print("\n👤 CREATE NEW STUDENT:")
            student_id = input("Student ID: ").strip()
            name = input("Name: ").strip()
            grade = input("Grade (1-12): ").strip()
            favorite_state = input("Favorite State (default: Maharashtra): ").strip() or "Maharashtra"
            
            try:
                grade = int(grade)
                if grade < 1 or grade > 12:
                    print("❌ Grade must be between 1 and 12")
                    continue
                
                success = student_tracker.create_student(student_id, name, grade, favorite_state)
                if success:
                    print(f"✅ Student {name} created successfully!")
                else:
                    print("❌ Student creation failed")
            except ValueError:
                print("❌ Invalid grade format")
        
        elif choice == '2':
            print("\n📋 ALL STUDENTS:")
            students = student_tracker.get_all_students_summary()
            if not students:
                print("No students found.")
            else:
                for student in students:
                    print(f"ID: {student['student_id']}")
                    print(f"Name: {student['name']}")
                    print(f"Grade: {student['grade']}")
                    print(f"Favorite State: {student['favorite_state']}")
                    print(f"Questions: {student['total_questions']}")
                    print(f"Accuracy: {student['accuracy']:.1%}")
                    print(f"Current Difficulty: {student['current_difficulty']:.1}")
                    print(f"Streak: {student['streak_days']} days")
                    print(f"States Visited: {student['states_visited_count']}")
                    print("-" * 30)
        
        elif choice == '3':
            print("\n📊 VIEW STUDENT PROGRESS:")
            student_id = input("Enter Student ID: ").strip()
            progress = student_tracker.get_student_progress(student_id)
            if progress:
                print(f"\n📈 PROGRESS FOR {progress['name']}:")
                print(f"Grade: {progress['grade']}")
                print(f"Favorite State: {progress['favorite_state']}")
                print(f"Total Questions: {progress['total_questions']}")
                print(f"Correct Answers: {progress['correct_answers']}")
                print(f"Accuracy: {progress['accuracy']:.1%}")
                print(f"Current Difficulty: {progress['current_difficulty']:.1}")
                print(f"Average Response Time: {progress['avg_response_time']:.1f}s")
                print(f"Streak: {progress['streak_days']} days")
                print(f"Last Quiz: {progress['last_quiz_date']}")
                print(f"States Visited: {len(progress['states_visited'])}")
            else:
                print("❌ Student not found")
        
        elif choice == '4':
            print("\n🗺️ VIEW STATE-WISE PROGRESS:")
            student_id = input("Enter Student ID: ").strip()
            states_progress = student_tracker.get_states_progress(student_id)
            if states_progress:
                print(f"\n📊 STATE-WISE PROGRESS FOR STUDENT {student_id}:")
                for state, progress in states_progress.items():
                    print(f"\n🏛️ {state}:")
                    print(f"   Questions: {progress['total_questions']}")
                    print(f"   Correct: {progress['correct_answers']}")
                    print(f"   Accuracy: {progress['accuracy']:.1%}")
                    print(f"   Avg Response Time: {progress['avg_response_time']:.1f}s")
            else:
                print("❌ No state progress data found")
        
        elif choice == '5':
            break
        
        else:
            print("❌ Invalid option")

def take_quiz(quiz_model, question_bank, student_tracker):
    """Take an Indian states geography quiz."""
    print("\n🗺️ TAKE INDIAN STATES GEOGRAPHY QUIZ:")
    
    # Select student
    students = student_tracker.get_all_students_summary()
    if not students:
        print("❌ No students found. Please create a student first.")
        return
    
    print("\nAvailable Students:")
    for i, student in enumerate(students, 1):
        print(f"{i}. {student['name']} (ID: {student['student_id']})")
    
    try:
        choice = int(input(f"\nSelect student (1-{len(students)}): ")) - 1
        if choice < 0 or choice >= len(students):
            print("❌ Invalid selection")
            return
        
        selected_student = students[choice]
        student_id = selected_student['student_id']
        
        print(f"\n🎯 Quiz for {selected_student['name']}")
        print(f"Current Difficulty: {selected_student['current_difficulty']:.1}")
        print(f"Overall Accuracy: {selected_student['accuracy']:.1%}")
        print(f"States Visited: {selected_student['states_visited_count']}")
        
        # Get performance data for ML prediction
        performance = student_tracker.get_student_performance(student_id)
        predicted_difficulty = quiz_model.predict_difficulty(performance)
        
        print(f"🤖 ML Predicted Difficulty: {predicted_difficulty:.1}")
        print()
        
        # Select state
        print("Available States:")
        states = question_bank.get_states_with_questions()
        for i, state in enumerate(states, 1):
            print(f"{i}. {state}")
        
        state_choice = int(input(f"\nSelect state (1-{len(states)}): ")) - 1
        if state_choice < 0 or state_choice >= len(states):
            print("❌ Invalid state selection")
            return
        
        selected_state = states[state_choice]
        print(f"\n🗺️ Selected State: {selected_state}")
        
        # Start quiz
        question_count = 0
        correct_count = 0
        
        while True:
            # Get question for the selected state
            question = question_bank.get_question(
                difficulty=int(predicted_difficulty),
                state=selected_state,
                exclude_ids=[q['id'] for q in question_bank.questions.get(int(predicted_difficulty), {}).get(selected_state, [])[:question_count]]
            )
            
            if not question:
                print(f"❌ No more questions available for {selected_state} at this difficulty level.")
                break
            
            question_count += 1
            print(f"Question {question_count}:")
            print(f"🏛️ State: {question['state']}")
            print(f"🎯 Difficulty: {question['difficulty']}")
            print(f"❓ {question['question']}")
            print()
            
            # Display options
            for i, option in enumerate(question['options']):
                print(f"{i}. {option}")
            print()
            
            # Get answer
            start_time = time.time()
            attempts = 0
            
            while True:
                try:
                    answer = int(input("Your answer (0-3): "))
                    if 0 <= answer <= 3:
                        break
                    else:
                        print("❌ Please enter a number between 0 and 3")
                        attempts += 1
                except ValueError:
                    print("❌ Please enter a valid number")
                    attempts += 1
            
            response_time = time.time() - start_time
            attempts += 1
            
            # Validate answer
            is_correct, feedback = question_bank.validate_answer(question['id'], answer)
            
            if is_correct:
                correct_count += 1
                print(f"✅ Correct! {feedback}")
            else:
                print(f"❌ Incorrect. {feedback}")
            
            print(f"⏱️ Response time: {response_time:.1f}s")
            print(f"🔄 Attempts: {attempts}")
            print()
            
            # Record attempt
            student_tracker.record_quiz_attempt(
                student_id=student_id,
                question_id=question['id'],
                difficulty=question['difficulty'],
                response_time=response_time,
                is_correct=is_correct,
                attempts=attempts,
                state=selected_state
            )
            
            # Update difficulty for next question
            updated_performance = student_tracker.get_student_performance(student_id)
            predicted_difficulty = quiz_model.predict_difficulty(updated_performance)
            student_tracker.update_difficulty(student_id, predicted_difficulty)
            
            print(f"🤖 Next question difficulty: {predicted_difficulty:.1}")
            print("-" * 50)
            
            # Ask if continue
            continue_quiz = input("Continue quiz? (y/n): ").strip().lower()
            if continue_quiz != 'y':
                break
        
        # Quiz summary
        accuracy = correct_count / question_count if question_count > 0 else 0
        print(f"\n🎉 QUIZ COMPLETED!")
        print(f"State: {selected_state}")
        print(f"Questions answered: {question_count}")
        print(f"Correct answers: {correct_count}")
        print(f"Accuracy: {accuracy:.1%}")
        
        # Update final performance
        final_performance = student_tracker.get_student_performance(student_id)
        print(f"Final difficulty level: {final_performance['current_difficulty']:.1}")
        
    except (ValueError, IndexError) as e:
        print(f"❌ Error: {e}")

def view_analytics(student_tracker, question_bank):
    """View system analytics."""
    print("\n📊 SYSTEM ANALYTICS:")
    
    # Question bank stats
    print("📚 QUESTION BANK STATISTICS:")
    qb_stats = question_bank.get_statistics()
    print(f"Total Questions: {qb_stats['total_questions']}")
    print(f"States: {len(qb_stats['states'])}")
    print(f"Union Territories: {len(qb_stats['union_territories'])}")
    print("Questions by Difficulty:")
    for diff, count in qb_stats['questions_by_difficulty'].items():
        level_name = qb_stats['difficulty_levels'][diff]
        print(f"  Level {diff} ({level_name}): {count}")
    
    print("\n📊 STUDENT PERFORMANCE SUMMARY:")
    students = student_tracker.get_all_students_summary()
    if not students:
        print("No students found.")
    else:
        total_questions = sum(s['total_questions'] for s in students)
        avg_accuracy = sum(s['accuracy'] for s in students) / len(students)
        avg_difficulty = sum(s['current_difficulty'] for s in students) / len(students)
        total_states_visited = sum(s['states_visited_count'] for s in students)
        
        print(f"Total Students: {len(students)}")
        print(f"Total Questions Answered: {total_questions}")
        print(f"Average Accuracy: {avg_accuracy:.1%}")
        print(f"Average Difficulty: {avg_difficulty:.1}")
        print(f"Total States Visited: {total_states_visited}")
        
        print("\nTop Performers:")
        top_students = sorted(students, key=lambda x: x['accuracy'], reverse=True)[:3]
        for i, student in enumerate(top_students, 1):
            print(f"{i}. {student['name']} - {student['accuracy']:.1%} accuracy")

def system_status(quiz_model, question_bank, student_tracker):
    """Show system status."""
    print("\n🔧 SYSTEM STATUS:")
    
    # ML Model status
    print("🤖 MACHINE LEARNING MODEL:")
    model_info = quiz_model.get_model_info()
    print(f"Status: {'✅ Trained' if model_info['is_trained'] else '❌ Not Trained'}")
    print(f"Type: {model_info['model_type']}")
    if model_info['is_trained']:
        print(f"Estimators: {model_info['n_estimators']}")
        print(f"Features: {model_info['feature_count']}")
    
    # Question Bank status
    print("\n📚 QUESTION BANK:")
    qb_stats = question_bank.get_statistics()
    print(f"Total Questions: {qb_stats['total_questions']}")
    print(f"States: {len(qb_stats['states'])}")
    print(f"Union Territories: {len(qb_stats['union_territories'])}")
    
    # Student Tracker status
    print("\n👨‍🎓 STUDENT TRACKER:")
    students = student_tracker.get_all_students_summary()
    print(f"Total Students: {len(students)}")
    if students:
        active_students = sum(1 for s in students if s['total_questions'] > 0)
        print(f"Active Students: {active_students}")
        print(f"Total Questions Answered: {sum(s['total_questions'] for s in students)}")
        print(f"Total States Visited: {sum(s['states_visited_count'] for s in students)}")

def start_api_server():
    """Start the Flask API server."""
    print("\n🚀 STARTING API SERVER...")
    print("The API server will be available at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Import and run the Flask app
        from api.app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 API server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def launch_map_interface():
    """Launch the interactive map interface."""
    print("\n🖥️ LAUNCHING INTERACTIVE MAP INTERFACE...")
    print("This will open a graphical interface where you can click on states to get questions.")
    print()
    
    try:
        # Check if tkinter is available
        import tkinter
        print("✅ Tkinter is available. Launching interface...")
        
        # Import and run the map interface
        from indian_map_interface import main as map_main
        map_main()
        
    except ImportError:
        print("❌ Tkinter is not available. Please install tkinter to use the graphical interface.")
        print("You can still use the console-based quiz system.")
    except Exception as e:
        print(f"❌ Error launching map interface: {e}")

def main():
    """Main application loop."""
    print_banner()
    
    # Initialize components
    print("🔄 Initializing system components...")
    quiz_model = AdaptiveQuizModel()
    question_bank = QuestionBank()
    student_tracker = StudentTracker()
    print("✅ System initialized successfully!")
    print()
    
    # Create sample data if none exists
    if not student_tracker.students:
        print("📝 Creating sample student for demonstration...")
        student_tracker.create_student("demo001", "Demo Student", 5, "Maharashtra")
        print("✅ Sample student created!")
        print()
    
    while True:
        print_menu()
        
        try:
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                train_ml_model(quiz_model, student_tracker)
            
            elif choice == '2':
                manage_students(student_tracker)
            
            elif choice == '3':
                take_quiz(quiz_model, question_bank, student_tracker)
            
            elif choice == '4':
                view_analytics(student_tracker, question_bank)
            
            elif choice == '5':
                system_status(quiz_model, question_bank, student_tracker)
            
            elif choice == '6':
                start_api_server()
            
            elif choice == '7':
                launch_map_interface()
            
            elif choice == '8':
                print("\n👋 Thank you for using the Indian States Geography Quiz System!")
                print("Goodbye! 🇮🇳")
                break
            
            else:
                print("❌ Invalid option. Please select 1-8.")
            
            if choice not in ['6', '7']:  # Don't pause after starting API server or launching interface
                input("\nPress Enter to continue...")
                print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! 🇮🇳")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
