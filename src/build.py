#!/usr/bin/env python3
"""
Java Learning Platform — Master Build Script
Assembles curriculum data + templates into a single self-contained index.html.

Usage: python3 build.py

Directory structure:
  src/templates/head.html  — HTML/CSS up to the curriculum data insertion point
  src/templates/tail.html  — JavaScript application code + closing tags
  src/curriculum/          — Phase data files (phase1.py, phase2.py, ...)
  dist/index.html          — Build output
"""

import json, os, sys, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SRC = SCRIPT_DIR  # build.py lives in src/
OUTPUT = os.path.join(PROJECT_ROOT, 'dist', 'index.html')

# ===== PHASE METADATA =====
PHASES = {
    "Programming Fundamentals": {"icon": "☕", "colorClass": "java", "cssClass": "ph-java", "color": "#f89820"},
    "Developer Tools": {"icon": "🔧", "colorClass": "tools", "cssClass": "ph-tools", "color": "#c084fc"},
    "Data Structures & Algorithms": {"icon": "📊", "colorClass": "dsa", "cssClass": "ph-dsa", "color": "#f472b6"},
    "Database Fundamentals": {"icon": "🗄️", "colorClass": "db", "cssClass": "ph-db", "color": "#60a5fa"},
    "Web Fundamentals": {"icon": "🌐", "colorClass": "web", "cssClass": "ph-web", "color": "#38bdf8"},
    "Spring Boot": {"icon": "🍃", "colorClass": "spring", "cssClass": "ph-spring", "color": "#6db33f"},
}


def load_topics():
    """Load all curriculum topics from phase files."""
    topics = []
    curriculum_dir = os.path.join(SRC, 'curriculum')
    
    if os.path.isdir(curriculum_dir):
        for fname in sorted(os.listdir(curriculum_dir)):
            if fname.endswith('.py') and fname != '__init__.py':
                filepath = os.path.join(curriculum_dir, fname)
                # Execute the phase file to get its TOPICS list
                namespace = {}
                with open(filepath) as f:
                    exec(f.read(), namespace)
                if 'TOPICS' in namespace:
                    topics.extend(namespace['TOPICS'])
                    print(f"  Loaded {len(namespace['TOPICS'])} topics from {fname}")
    
    if not topics:
        print("ERROR: No topics loaded. Create phase files in src/curriculum/.")
        print("Run: python3 -c \"from curriculum.phase1 import TOPICS\" to verify.")
        sys.exit(1)

    return topics


def validate_topics(topics):
    """Validate curriculum data integrity."""
    errors = []
    ids = set()
    for t in topics:
        # Required fields
        for field in ['id', 'phase', 'title', 'hours', 'complexity', 'importance', 
                       'textbook', 'summary', 'lesson', 'quiz', 'codingExercise']:
            if field not in t:
                errors.append(f"Topic {t.get('id', '?')}: missing field '{field}'")
        
        # Duplicate ID check
        tid = t.get('id')
        if tid in ids:
            errors.append(f"Topic {tid}: duplicate ID")
        ids.add(tid)
        
        # Quiz validation
        quiz = t.get('quiz', [])
        if not isinstance(quiz, list):
            errors.append(f"Topic {tid}: quiz is not a list")
        else:
            for qi, q in enumerate(quiz):
                if 'correct' in q:
                    correct = q['correct']
                    options = q.get('options', [])
                    if not (0 <= correct < len(options)):
                        errors.append(f"Topic {tid}, quiz Q{qi+1}: correct={correct} out of range (0-{len(options)-1})")
        
        # Complexity/Importance values
        for field, valid in [('complexity', ['beginner', 'intermediate', 'advanced']),
                              ('importance', ['critical', 'important', 'nice'])]:
            if t.get(field) not in valid:
                errors.append(f"Topic {tid}: {field}='{t.get(field)}' not in {valid}")
    
    if errors:
        print("\n⚠ VALIDATION ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return False
    
    print(f"  ✓ All {len(topics)} topics validated successfully")
    return True


def build():
    """Main build function."""
    print("Building Java Learning Platform...")
    
    # Load topics
    topics = load_topics()
    if not topics:
        print("ERROR: No topics loaded. Create phase files in src/curriculum/ or ensure build.py exists.")
        sys.exit(1)
    
    # Validate
    if not validate_topics(topics):
        print("WARNING: Validation failed. Build may produce broken output.")
    
    # Load templates
    head_path = os.path.join(SRC, 'templates', 'head.html')
    tail_path = os.path.join(SRC, 'templates', 'tail.html')
    
    if not os.path.exists(head_path) or not os.path.exists(tail_path):
        print("ERROR: Template files not found. Run extract_templates.py first.")
        sys.exit(1)
    
    with open(head_path) as f:
        head = f.read()
    with open(tail_path) as f:
        tail = f.read()
    
    # Serialize data
    curriculum_json = json.dumps(topics, ensure_ascii=False, indent=2)
    phases_json = json.dumps(PHASES, ensure_ascii=False, indent=2)
    
    # Assemble
    middle = (f'const CURRICULUM = {curriculum_json};\n\n'
              f'// ===== PHASE METADATA =====\n'
              f'const PHASES = {phases_json};\n\n')
    
    output = head + middle + tail
    
    # Write
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(output)
    
    # Stats
    word_count = sum(len(re.sub(r'<[^>]+>', ' ', t['lesson']).split()) for t in topics)
    total_hours = sum(t['hours'] for t in topics)
    print(f"\n✓ Build complete: {OUTPUT}")
    print(f"  {len(topics)} topics, {word_count:,} lesson words, ~{total_hours}h")
    print(f"  Output: {len(output):,} chars")


if __name__ == '__main__':
    build()
