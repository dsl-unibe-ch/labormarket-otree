"""
Bot tests for outro_quiz app
"""

from otree.api import Bot, Submission
from . import PEQ, DemographicQuiz, Conclusion


class PlayerBot(Bot):
    """Bot that completes the post-experiment questionnaire"""
    
    def play_round(self):
        """Play through the outro quiz"""
        
        # PEQ (Post-Experiment Questionnaire) - 17 questions per role
        # Different scales are used for different questions:
        # - Most questions use DISAGREE_AGREE (1-7)
        # - Questions 12, 14, 15 use LOWER_HIGHER (-3 to 3)
        # - Question 16 uses WORSE_BETTER (-3 to 3) only for managers
        
        if self.player.role == "Employee":
            peq_fields = {
                f"e_peq_quiz{i}": 4 for i in range(1, 13)  # 1-12: DISAGREE_AGREE (1-7)
            }
            peq_fields["e_peq_quiz13"] = 0  # LOWER_HIGHER (-3 to 3)
            peq_fields["e_peq_quiz14"] = 0  # LOWER_HIGHER (-3 to 3)
            peq_fields.update({f"e_peq_quiz{i}": 4 for i in range(15, 18)})  # 15-17: DISAGREE_AGREE (1-7)
        else:  # Manager
            peq_fields = {
                f"m_peq_quiz{i}": 4 for i in range(1, 12)  # 1-11: DISAGREE_AGREE (1-7)
            }
            peq_fields["m_peq_quiz12"] = 0  # LOWER_HIGHER (-3 to 3)
            peq_fields["m_peq_quiz13"] = 4  # DISAGREE_AGREE (1-7)
            peq_fields["m_peq_quiz14"] = 4  # DISAGREE_AGREE (1-7)
            peq_fields["m_peq_quiz15"] = 0  # LOWER_HIGHER (-3 to 3)
            peq_fields["m_peq_quiz16"] = 0  # WORSE_BETTER (-3 to 3)
            peq_fields["m_peq_quiz17"] = 4  # DISAGREE_AGREE (1-7)
        
        yield Submission(PEQ, peq_fields, check_html=False)
        
        # Demographic Quiz - 8 questions
        demographic_fields = {
            "demographic_quiz1": "Male",
            "demographic_quiz2": 25,
            "demographic_quiz3": "Junior",
            "demographic_quiz4": "Computer Science",
            "demographic_quiz5": 3.5,
            "demographic_quiz6": 5,
            "demographic_quiz7": 5,
            "demographic_quiz8": "No additional comments",
        }
        yield Submission(DemographicQuiz, demographic_fields, check_html=False)
