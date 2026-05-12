"""Java Learning Platform — REST API Backend"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import query

app = Flask(__name__)
CORS(app)
DEFAULT_USER = 1


# ── Health ──────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'java-learning-platform'})


# ── Progress ────────────────────────────────────────────
@app.route('/api/progress', methods=['GET'])
def get_progress():
    rows = query(
        'SELECT topic_id FROM topic_progress WHERE user_id = %s',
        (DEFAULT_USER,)
    )
    return jsonify({'completedTopicIds': [r['topic_id'] for r in rows]})


@app.route('/api/progress/<int:topic_id>', methods=['POST'])
def mark_complete(topic_id):
    query(
        'INSERT IGNORE INTO topic_progress (user_id, topic_id) VALUES (%s, %s)',
        (DEFAULT_USER, topic_id),
        fetch=False
    )
    return jsonify({'status': 'ok', 'topicId': topic_id, 'completed': True})


@app.route('/api/progress/<int:topic_id>', methods=['DELETE'])
def unmark_complete(topic_id):
    query(
        'DELETE FROM topic_progress WHERE user_id = %s AND topic_id = %s',
        (DEFAULT_USER, topic_id),
        fetch=False
    )
    return jsonify({'status': 'ok', 'topicId': topic_id, 'completed': False})


# ── Quiz Answers ────────────────────────────────────────
@app.route('/api/quiz/<int:topic_id>', methods=['GET'])
def get_quiz_answers(topic_id):
    rows = query(
        'SELECT question_index, selected_option, is_correct FROM quiz_answers '
        'WHERE user_id = %s AND topic_id = %s',
        (DEFAULT_USER, topic_id)
    )
    answers = {}
    for r in rows:
        answers[r['question_index']] = {
            'selectedOption': r['selected_option'],
            'isCorrect': bool(r['is_correct'])
        }
    return jsonify({'topicId': topic_id, 'answers': answers})


@app.route('/api/quiz/<int:topic_id>', methods=['POST'])
def save_quiz_answers(topic_id):
    data = request.get_json()
    answers = data.get('answers', {})
    for qi_str, answer in answers.items():
        qi = int(qi_str)
        query(
            'REPLACE INTO quiz_answers (user_id, topic_id, question_index, selected_option, is_correct) '
            'VALUES (%s, %s, %s, %s, %s)',
            (DEFAULT_USER, topic_id, qi, answer['selectedOption'], answer['isCorrect']),
            fetch=False
        )
    return jsonify({'status': 'ok', 'topicId': topic_id, 'saved': len(answers)})


# ── Resources ───────────────────────────────────────────
@app.route('/api/resources/<int:topic_id>', methods=['GET'])
def get_resources(topic_id):
    rows = query(
        'SELECT id, resource_type, title, author, url, created_at FROM topic_resources '
        'WHERE user_id = %s AND topic_id = %s ORDER BY created_at DESC',
        (DEFAULT_USER, topic_id)
    )
    resources = []
    for r in rows:
        resources.append({
            'id': r['id'],
            'type': r['resource_type'],
            'title': r['title'],
            'author': r['author'] or '',
            'url': r['url'],
            'addedAt': r['created_at'].isoformat() if r['created_at'] else None
        })
    return jsonify({'topicId': topic_id, 'resources': resources})


@app.route('/api/resources/<int:topic_id>', methods=['POST'])
def add_resource(topic_id):
    data = request.get_json()
    rid = query(
        'INSERT INTO topic_resources (user_id, topic_id, resource_type, title, author, url) '
        'VALUES (%s, %s, %s, %s, %s, %s)',
        (DEFAULT_USER, topic_id, data['type'], data['title'], data.get('author', ''), data.get('url', '')),
        fetch=False
    )
    return jsonify({'status': 'ok', 'id': rid, 'topicId': topic_id})


@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    query(
        'DELETE FROM topic_resources WHERE id = %s AND user_id = %s',
        (resource_id, DEFAULT_USER),
        fetch=False
    )
    return jsonify({'status': 'ok', 'id': resource_id})


# ── Enhancements ────────────────────────────────────────
@app.route('/api/enhancements/<int:topic_id>', methods=['GET'])
def get_enhancements(topic_id):
    rows = query(
        'SELECT id, comment, status, created_at FROM topic_enhancements '
        'WHERE user_id = %s AND topic_id = %s ORDER BY created_at DESC',
        (DEFAULT_USER, topic_id)
    )
    enhancements = []
    for r in rows:
        enhancements.append({
            'id': r['id'],
            'comment': r['comment'],
            'status': r['status'],
            'submittedAt': r['created_at'].isoformat() if r['created_at'] else None
        })
    return jsonify({'topicId': topic_id, 'enhancements': enhancements})


@app.route('/api/enhancements/<int:topic_id>', methods=['POST'])
def add_enhancement(topic_id):
    data = request.get_json()
    eid = query(
        'INSERT INTO topic_enhancements (user_id, topic_id, comment) VALUES (%s, %s, %s)',
        (DEFAULT_USER, topic_id, data['comment']),
        fetch=False
    )
    return jsonify({'status': 'ok', 'id': eid, 'topicId': topic_id})


if __name__ == '__main__':
    print("Starting Java Learning Platform API on http://localhost:5000")
    app.run(debug=True, port=5000)
