#!/usr/bin/env python3
"""ONE-SHOT GENERATOR: Builds complete index.html with all 65 topics. All JS escaping via json.dumps()."""
import json, os

OUTPUT = os.path.join(os.path.dirname(__file__), 'index.html')

# ===== CURRICULUM DATA ====="
topics = []
def t(id, phase, pc, pclass, title, hrs, comp, imp, textbook, summary, lesson, quiz, ex=None):
    topics.append(dict(id=id, phase=phase, phaseColor=pc, phaseClass=pclass, title=title,
        hours=hrs, complexity=comp, importance=imp, textbook=textbook, summary=summary,
        lesson=lesson, quiz=quiz, codingExercise=ex))
def q(question, options, correct, explanation):
    return dict(question=question, options=options, correct=correct, explanation=explanation)
def e(instruction, hint, keywords):
    return dict(instruction=instruction, hint=hint, checkKeywords=keywords)
P1='Programming Fundamentals';P2='Developer Tools';P3='Data Structures & Algorithms'
P4='Database Fundamentals';P5='Web Fundamentals';P6='Spring Boot'
J='java';T='tools';D='dsa';DB='db';W='web';S='spring'
