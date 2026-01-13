"""
Bot tests for labor_market app
"""

from otree.api import Bot, Submission
from . import (
    MakeOffer, GetOffers,
    MatchSummary, ChooseEffort, PeriodResults
)


class PlayerBot(Bot):
    """Bot that plays through the labor market simulation"""
    
    def play_round(self):
        """Play through one round of the labor market"""
        
        # The page sequence repeats: [MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * 6 times
        # Then: MatchSummary, ChooseEffort, WaitForEffort, PeriodResults
        # (WaitPages are handled automatically, don't yield them)
        # Only yield pages that will actually be displayed to this player
        
        for step in range(6):  # 6 hiring steps
            # Managers make offers or skip (only shown if unmatched, not offer_none, and has eligible candidates)
            if self.player.role == "Manager":
                if self.player.player_matched == 0 and not self.player.offer_none:
                    available = self.player.for_hire()
                    if available:
                        # Make an offer to first available employee
                        employee_id = available[0].id_in_group
                        yield Submission(
                            MakeOffer,
                            {
                                'offer_employee': employee_id,
                                'offer_wage': 100,
                                'offer_training': False
                            },
                            check_html=False
                        )
                    else:
                        # No one to hire, submit no offer
                        yield Submission(
                            MakeOffer,
                            {'offer_employee': 0},
                            check_html=False
                        )
            
            # Employees accept offers if they have any (only shown if unmatched and has open offers)
            if self.player.role == "Employee" and self.player.player_matched == 0:
                open_offers = [o for o in self.player.offer_history 
                              if not o.accepted and not o.rejected]
                if open_offers:
                    manager_id = open_offers[0].manager.id_in_group
                    yield Submission(
                        GetOffers,
                        {'player_matched': manager_id},
                        check_html=False
                    )
        
        # After hiring phase, view match summary (no form submission)
        yield MatchSummary
        
        # Choose effort - only shown to EMPLOYEES who are matched
        if self.player.role == "Employee" and self.player.player_matched > 0:
            yield Submission(
                ChooseEffort,
                {'work_effort': 5},
                check_html=False
            )
        
        # View period results (only shown at end)
        yield PeriodResults
