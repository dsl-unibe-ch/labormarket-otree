"""
Bot tests for intro_quiz app
Save this as tests.py in your intro_quiz folder
"""

# Bot: Base class for creating bots
# expect: Function to verify/assert values (for testing)
# Submission: Wrapper for form submissions with extra options
# get_answers(): Your function that returns correct quiz answers
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
        """
        play_round() method: Defines what the bot does in one round
        yield statement: Tells the bot to visit a page
        """
        
        # Consent page
        # Bot visits the Consent page, 
        # Automatically clicks "Next" button
        # No form data to submit
        yield Consent
        
        # Instructions pages 1-3
        # Bot goes to these pages and clicks Next
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
        

        #expect(self.player.quiz1_complete, True):
        # Checks if player.quiz1_complete equals True
        # If not, test fails with an error message
        # Similar to assert in Python, but gives better error messages

        # Verify quizzes were marked complete
        expect(self.player.quiz1_complete, True)
        expect(self.player.quiz2_complete, True)
        expect(self.player.quiz3_complete, True)
    
    def submit_quiz1(self):
        """Submit Quiz 1 with correct answers"""
        answers = get_answers(0) # Get correct answers: [0, 0, 1, 1, ...] for Quiz1 from quiz.py
        submission = {f'q1_{i+1}': answers[i] for i in range(11)} # Build submission dictionary, 
                                                                  # Creates: {'q1_1': 0, 'q1_2': 0, 'q1_3': 1, ...}
        # Quiz1: The page to visit
        # submission: The form data to submit
        # check_html=False: Don't validate HTML structure (faster)
        return Submission(Quiz1, submission, check_html=False)
    
    def submit_quiz2(self):
        """Submit Quiz 2 with correct answers"""
        answers = get_answers(1)
        
        # Base questions (1-7) for all roles
        # Employees get 8 questions, Managers get 7
        num_questions = 7
        
        # Employees get 8 questions
        if self.player.role == "Employee":
            num_questions = 8
        
        # If Employee: create 8 answer fields (q2_1 through q2_8)
        # If Manager: create 7 answer fields (q2_1 through q2_7)
        submission = {f'q2_{i+1}': answers[i] for i in range(num_questions)}
        return Submission(Quiz2, submission, check_html=False)
    
    def submit_quiz3(self):
        """Submit Quiz 3 with correct answers"""
        answers = get_answers(2)
        submission = {f'q3_{i+1}': answers[i] for i in range(8)}
        return Submission(Quiz3, submission, check_html=False)
    


# When you run otree test intro_quiz:
# 1. oTree creates virtual players (12 players: 6 managers, 6 employees)

# 2. Each player runs play_round():
#   - Player 1 (Manager):   Consent → Instructions → Quiz1 → ...
#   - Player 2 (Manager):   Consent → Instructions → Quiz1 → ...
#   - Player 3 (Employee):  Consent → Instructions → Quiz1 → ...
#   - ... (all 12 players simultaneously)

# 3. Bots fill out forms automatically using the submission dictionaries

# 4. oTree checks for errors:
#   - Form validation errors
#   - Python exceptions
#   - Failed expect() assertions


