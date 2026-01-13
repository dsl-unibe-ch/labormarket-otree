"""
Bot tests for intro_quiz app
Save this as tests.py in your intro_quiz folder
"""

from otree.api import Bot, expect, Submission
from .quiz import get_answers, get_questions
from . import (
    Consent, Instructions1, Instructions2, Instructions3,
    Instructions4, Instructions5, Instructions6, Instructions7,
    Instructions8, Instructions9, Instructions10,
    Quiz1, Quiz2, Quiz3, Feedback
)


class PlayerBot(Bot):
    """Bot that automatically answers quiz questions correctly"""
    
    def play_round(self):
        """Play through all pages in the intro_quiz app"""
        
        # Consent page
        yield Consent
        
        # Instructions pages 1-3
        yield Instructions1
        yield Instructions2
        yield Instructions3
        
        # Quiz 1 - Submit correct answers
        yield self.submit_quiz1()
        
        # Instructions pages 4-6
        yield Instructions4
        yield Instructions5
        yield Instructions6
        
        # Quiz 2 - Submit correct answers (role-dependent)
        yield self.submit_quiz2()
        
        # Instructions pages 7-10
        yield Instructions7
        yield Instructions8
        yield Instructions9
        yield Instructions10
        
        # Quiz 3 - Submit correct answers
        yield self.submit_quiz3()
        
        # Verify quizzes were marked complete
        expect(self.player.quiz1_complete, True)
        expect(self.player.quiz2_complete, True)
        expect(self.player.quiz3_complete, True)
    
    def submit_quiz1(self):
        """Submit Quiz 1 with correct answers"""
        answers = get_answers(0)
        submission = {f'q1_{i+1}': answers[i] for i in range(11)}
        return Submission(Quiz1, submission, check_html=False)
    
    def submit_quiz2(self):
        """Submit Quiz 2 with correct answers"""
        answers = get_answers(1)
        
        # Base questions (1-7) for all roles
        num_questions = 7
        
        # Employees get 8 questions
        if self.player.role == "Employee":
            num_questions = 8
        
        submission = {f'q2_{i+1}': answers[i] for i in range(num_questions)}
        return Submission(Quiz2, submission, check_html=False)
    
    def submit_quiz3(self):
        """Submit Quiz 3 with correct answers"""
        answers = get_answers(2)
        submission = {f'q3_{i+1}': answers[i] for i in range(8)}
        return Submission(Quiz3, submission, check_html=False)


class PlayerBotWrong(Bot):
    """
    Bot that tests error handling by submitting wrong answers
    This is useful for testing that your quiz validation works correctly
    """
    
    def play_round(self):
        """Play through with intentional wrong answers on first attempt"""
        
        yield Consent
        yield Instructions1
        yield Instructions2
        yield Instructions3
        
        # Quiz 1 - Submit wrong answers first (should get error message)
        # Note: oTree bots don't actually handle error_message returns,
        # but this documents the intended behavior
        wrong_answers = {f'q1_{i+1}': 1 if get_answers(0)[i] == 0 else 0 
                        for i in range(11)}
        
        # Then submit correct answers
        correct_answers = {f'q1_{i+1}': get_answers(0)[i] for i in range(11)}
        yield Submission(Quiz1, correct_answers, check_html=False)
        
        # Continue normally
        yield Instructions4
        yield Instructions5
        yield Instructions6
        
        num_q2 = 8 if self.player.role == "Employee" else 7
        correct_q2 = {f'q2_{i+1}': get_answers(1)[i] for i in range(num_q2)}
        yield Submission(Quiz2, correct_q2, check_html=False)
        
        yield Instructions7
        yield Instructions8
        yield Instructions9
        yield Instructions10
        
        correct_q3 = {f'q3_{i+1}': get_answers(2)[i] for i in range(8)}
        yield Submission(Quiz3, correct_q3, check_html=False)


class PlayerBotRandom(Bot):
    """
    Bot that tests with random answers (will fail quizzes)
    Useful for stress testing your error messages
    """
    
    def play_round(self):
        import random
        
        yield Consent
        yield Instructions1
        yield Instructions2
        yield Instructions3
        
        # Eventually submit correct answers after "trying" random ones
        # (bots need to complete successfully)
        correct_q1 = {f'q1_{i+1}': get_answers(0)[i] for i in range(11)}
        yield Submission(Quiz1, correct_q1, check_html=False)
        
        yield Instructions4
        yield Instructions5
        yield Instructions6
        
        num_q2 = 8 if self.player.role == "Employee" else 7
        correct_q2 = {f'q2_{i+1}': get_answers(1)[i] for i in range(num_q2)}
        yield Submission(Quiz2, correct_q2, check_html=False)
        
        yield Instructions7
        yield Instructions8
        yield Instructions9
        yield Instructions10
        
        correct_q3 = {f'q3_{i+1}': get_answers(2)[i] for i in range(8)}
        yield Submission(Quiz3, correct_q3, check_html=False)