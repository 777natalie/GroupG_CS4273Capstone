"""
Grading endpoints for transcript analysis
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from api.services.rule_grader import RuleBasedGrader
from api.services.ai_grader import AIGraderService
from api.services.question_loader import QuestionLoader

grading_bp = Blueprint('grading', __name__)

# Initialize loaders and graders
question_loader = QuestionLoader()  # Loads questions from EMSQA.csv
rule_grader = RuleBasedGrader()     # Kept for backward compatibility

@grading_bp.route('/grade', methods=['POST'])
def grade_transcript():
    """
    Grade a transcript using AI grading (default)
    
    Request body (JSON):
        Group B's transcript format:
        {
            "language": "en",
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Norman 911, what is the address?",
                    "speaker": "SPEAKER_01",
                    ...
                }
            ]
        }
    
    Optional query params:
        ?show_evidence=true  - Include evidence in response (not used by AI)
    
    Returns:
        JSON response with AI grading results
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        transcript_data = request.get_json()
        
        # Validate required fields
        if 'segments' not in transcript_data:
            return jsonify({
                'error': 'Missing required field: segments'
            }), 400
        
        # Check if evidence should be included (not used by AI, but kept for API compatibility)
        show_evidence = request.args.get('show_evidence', 'false').lower() == 'true'
        
        # Load Case Entry questions from EMSQA.csv
        questions = question_loader.load_case_entry_questions()
        
        # Initialize AI grader with loaded questions
        ai_grader = AIGraderService(questions=questions)
        
        # Grade the transcript using AI
        grades = ai_grader.grade_transcript(transcript_data, show_evidence=show_evidence)
        
        # Calculate percentage score
        percentage = ai_grader.calculate_percentage(grades)
        
        # Count questions
        total_questions = len(grades)
        questions_asked_correctly = sum(
            1 for g in grades.values() if g.get('code') in ['1', '6']
        )
        questions_missed = total_questions - questions_asked_correctly
        
        # Build response
        response = {
            'grader_type': 'ai',
            'grade_percentage': percentage,
            'total_questions': total_questions,
            'questions_asked_correctly': questions_asked_correctly,
            'questions_missed': questions_missed,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'grades': grades,
            'metadata': {
                'language': transcript_data.get('language', 'unknown'),
                'segment_count': len(transcript_data.get('segments', [])),
                'grader_version': '1.0.0',
                'model': 'llama3.1:8b',
                'questions_source': 'EMSQA.csv (Case Entry)'
            }
        }
        
        return jsonify(response), 200
    
    except ConnectionError as e:
        return jsonify({
            'error': 'Ollama connection failed',
            'message': 'Please ensure Ollama is installed and running (ollama serve)',
            'details': str(e)
        }), 503
    
    except ValueError as e:
        return jsonify({
            'error': 'Invalid transcript data',
            'message': str(e)
        }), 400
    
    except RuntimeError as e:
        return jsonify({
            'error': 'AI grading failed',
            'message': str(e),
            'suggestion': 'Check if llama3.1:8b model is downloaded (ollama pull llama3.1:8b)'
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': f'Grading failed: {str(e)}'
        }), 500


@grading_bp.route('/grade/rule', methods=['POST'])
def grade_rule_only():
    """
    Explicit rule-based grading endpoint
    (Uses Kevin's original pattern-matching grader)
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        transcript_data = request.get_json()
        
        # Validate required fields
        if 'segments' not in transcript_data:
            return jsonify({
                'error': 'Missing required field: segments'
            }), 400
        
        # Check if evidence should be included
        show_evidence = request.args.get('show_evidence', 'false').lower() == 'true'
        
        # Grade the transcript using rule-based grader
        grades = rule_grader.grade_transcript(transcript_data, show_evidence=show_evidence)
        
        # Build response
        response = {
            'grader_type': 'rule_based',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'grades': grades,
            'metadata': {
                'language': transcript_data.get('language', 'unknown'),
                'segment_count': len(transcript_data.get('segments', [])),
                'grader_version': '1.0.0'
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Rule-based grading failed: {str(e)}'
        }), 500


@grading_bp.route('/grade/ai', methods=['POST'])
def grade_ai():
    """
    AI-based grading endpoint (alias for /grade)
    Uses Ollama with llama3.1:8b model
    """
    return grade_transcript()  # Use the main AI grading endpoint


@grading_bp.route('/grade/all', methods=['POST'])
def grade_all():
    """
    Run both rule-based and AI grading, return comparison
    
    TODO: Implement once AI grader is ready
    """
    return jsonify({
        'error': 'Combined grading not yet implemented',
        'message': 'Use /api/grade/rule for rule-based grading',
        'status': 'coming_soon'
    }), 501

