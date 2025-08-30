from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import time
from datetime import datetime

# Add parent directory to path to import ML modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.adaptive_quiz_model import AdaptiveQuizModel
from ml_model.question_bank import QuestionBank
from ml_model.student_tracker import StudentTracker

app = Flask(__name__)
CORS(app)

# Initialize components
quiz_model = AdaptiveQuizModel()
question_bank = QuestionBank()
student_tracker = StudentTracker()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_status': quiz_model.get_model_info()
    })

@app.route('/student/create', methods=['POST'])
def create_student():
    """Create a new student profile."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        name = data.get('name')
        grade = data.get('grade')
        favorite_state = data.get('favorite_state', 'General')
        
        if not all([student_id, name, grade]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = student_tracker.create_student(student_id, name, grade, favorite_state)
        
        if success:
            return jsonify({
                'message': 'Student created successfully',
                'student_id': student_id
            }), 201
        else:
            return jsonify({'error': 'Student already exists'}), 409
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Start a new quiz session for a student on a specific state."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        state = data.get('state')
        
        if not student_id:
            return jsonify({'error': 'Student ID required'}), 400
        
        if not state:
            return jsonify({'error': 'State required'}), 400
        
        # Get student performance data
        performance = student_tracker.get_student_performance(student_id)
        if not performance:
            return jsonify({'error': 'Student not found'}), 404
        
        # Predict optimal difficulty
        predicted_difficulty = quiz_model.predict_difficulty(performance)
        
        # Get appropriate question for the specific state
        question = question_bank.get_question(
            difficulty=int(predicted_difficulty),
            state=state
        )
        
        if not question:
            # Fallback to any available question for the state
            question = question_bank.get_questions_by_state(state, count=1)
            if question:
                question = question[0]
        
        if not question:
            return jsonify({'error': f'No questions available for {state}'}), 404
        
        # Start timer for response time tracking
        session_data = {
            'student_id': student_id,
            'question_id': question['id'],
            'start_time': time.time(),
            'state': state,
            'difficulty': question['difficulty']
        }
        
        return jsonify({
            'message': 'Quiz started',
            'question': {
                'id': question['id'],
                'question': question['question'],
                'options': question['options'],
                'difficulty': question['difficulty'],
                'state': question['state']
            },
            'session_data': session_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/answer', methods=['POST'])
def submit_answer():
    """Submit an answer and get feedback."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        start_time = data.get('start_time')
        attempts = data.get('attempts', 1)
        state = data.get('state')
        
        if not all([student_id, question_id, answer, start_time]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Validate answer
        is_correct, feedback = question_bank.validate_answer(question_id, answer)
        
        # Record the attempt
        student_tracker.record_quiz_attempt(
            student_id=student_id,
            question_id=question_id,
            difficulty=data.get('difficulty', 1.0),
            response_time=response_time,
            is_correct=is_correct,
            attempts=attempts,
            state=state
        )
        
        # Get updated performance data
        performance = student_tracker.get_student_performance(student_id)
        
        # Predict next difficulty
        next_difficulty = quiz_model.predict_difficulty(performance)
        
        # Update student's current difficulty
        student_tracker.update_difficulty(student_id, next_difficulty)
        
        return jsonify({
            'message': 'Answer submitted',
            'is_correct': is_correct,
            'feedback': feedback,
            'response_time': round(response_time, 2),
            'next_difficulty': round(next_difficulty, 1),
            'performance': {
                'accuracy': round(performance['accuracy'], 3),
                'current_difficulty': round(performance['current_difficulty'], 1),
                'total_questions': performance['total_questions'],
                'states_visited_count': performance['states_visited_count']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/next', methods=['GET'])
def get_next_question():
    """Get the next question for a student on a specific state."""
    try:
        student_id = request.args.get('student_id')
        state = request.args.get('state')
        
        if not student_id:
            return jsonify({'error': 'Student ID required'}), 400
        
        if not state:
            return jsonify({'error': 'State required'}), 400
        
        # Get student performance
        performance = student_tracker.get_student_performance(student_id)
        if not performance:
            return jsonify({'error': 'Student not found'}), 404
        
        # Predict difficulty
        predicted_difficulty = quiz_model.predict_difficulty(performance)
        
        # Get question for the specific state
        question = question_bank.get_question(
            difficulty=int(predicted_difficulty),
            state=state
        )
        
        if not question:
            # Fallback
            question = question_bank.get_questions_by_state(state, count=1)
            if question:
                question = question[0]
        
        if not question:
            return jsonify({'error': f'No questions available for {state}'}), 404
        
        return jsonify({
            'question': {
                'id': question['id'],
                'question': question['question'],
                'options': question['options'],
                'difficulty': question['difficulty'],
                'state': question['state']
            },
            'predicted_difficulty': round(predicted_difficulty, 1)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/states/list', methods=['GET'])
def get_states_list():
    """Get list of all Indian states and union territories."""
    try:
        return jsonify({
            'states': question_bank.states,
            'union_territories': question_bank.union_territories,
            'all_regions': question_bank.all_regions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/states/<state_name>/questions', methods=['GET'])
def get_state_questions(state_name: str):
    """Get questions for a specific state."""
    try:
        difficulty = request.args.get('difficulty', type=int)
        count = request.args.get('count', 5, type=int)
        
        questions = question_bank.get_questions_by_state(state_name, difficulty, count)
        
        if not questions:
            return jsonify({'error': f'No questions found for {state_name}'}), 404
        
        return jsonify({
            'state': state_name,
            'questions': questions,
            'total_available': len(questions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/student/progress', methods=['GET'])
def get_student_progress():
    """Get detailed progress for a student."""
    try:
        student_id = request.args.get('student_id')
        
        if not student_id:
            return jsonify({'error': 'Student ID required'}), 400
        
        progress = student_tracker.get_student_progress(student_id)
        if not progress:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify(progress), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/student/<student_id>/state/<state_name>/progress', methods=['GET'])
def get_student_state_progress(student_id: str, state_name: str):
    """Get student's progress for a specific state."""
    try:
        state_progress = student_tracker.get_state_performance(student_id, state_name)
        
        if not state_progress:
            return jsonify({'error': f'No progress data found for {state_name}'}), 404
        
        return jsonify(state_progress), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/student/update', methods=['POST'])
def update_student():
    """Update student information."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        updates = data.get('updates', {})
        
        if not student_id:
            return jsonify({'error': 'Student ID required'}), 400
        
        # Update student data
        if 'current_difficulty' in updates:
            student_tracker.update_difficulty(student_id, updates['current_difficulty'])
        
        return jsonify({'message': 'Student updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/summary', methods=['GET'])
def get_students_summary():
    """Get summary of all students."""
    try:
        summary = student_tracker.get_all_students_summary()
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/questions/stats', methods=['GET'])
def get_questions_stats():
    """Get statistics about the question bank."""
    try:
        stats = question_bank.get_statistics()
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model/train', methods=['POST'])
def train_model():
    """Train the ML model with sample data."""
    try:
        # Generate sample training data
        training_data = []
        
        # Get all students' performance data
        students = student_tracker.get_all_students_summary()
        
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
        
        if len(training_data) < 10:
            return jsonify({
                'error': 'Insufficient training data',
                'available_samples': len(training_data),
                'required_samples': 10
            }), 400
        
        # Train the model
        success = quiz_model.train_model(training_data)
        
        if success:
            return jsonify({
                'message': 'Model trained successfully',
                'training_samples': len(training_data),
                'model_info': quiz_model.get_model_info()
            }), 200
        else:
            return jsonify({'error': 'Model training failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def get_model_info():
    """Get information about the ML model."""
    try:
        info = quiz_model.get_model_info()
        return jsonify(info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Indian States Geography Quiz API Server...")
    print(f"Model Status: {quiz_model.get_model_info()}")
    print(f"Question Bank Stats: {question_bank.get_statistics()}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
