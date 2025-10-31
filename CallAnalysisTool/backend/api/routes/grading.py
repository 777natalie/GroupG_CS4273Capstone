"""
Grading endpoints for transcript analysis
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from api.services.rule_grader import RuleBasedGrader

grading_bp = Blueprint('grading', __name__)

# Initialize grader (loads rubric.json and synonyms.json)
grader = RuleBasedGrader()

@grading_bp.route('/grade', methods=['POST'])
def grade_transcript():
    """
    Grade a transcript using rule-based grading
    
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
        ?show_evidence=true  - Include evidence in response
    
    Returns:
        JSON response with grading results
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
        
        # Grade the transcript
        grades = grader.grade_transcript(transcript_data, show_evidence=show_evidence)
        
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
            'error': f'Grading failed: {str(e)}'
        }), 500


@grading_bp.route('/grade/rule', methods=['POST'])
def grade_rule_only():
    """
    Explicit rule-based grading endpoint
    (Alias for /grade for compatibility with future AI endpoints)
    """
    return grade_transcript()


@grading_bp.route('/grade/ai', methods=['POST'])
def grade_ai():
    """
    AI-based grading endpoint (placeholder)
    
    TODO: Integrate Jaiden's AI grader here
    """
    return jsonify({
        'error': 'AI grading not yet implemented',
        'message': 'Use /api/grade or /api/grade/rule for rule-based grading',
        'status': 'coming_soon'
    }), 501


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

