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
    """
    This bot simulates the labor market hiring and work phase where:
        - Managers make contract offers to employees (up to 6 attempts)
        - Employees accept or reject offers
        - Then matched pairs complete the work phase
    """
    
    def play_round(self):
        """Play through one round of the labor market"""
        
        # The page sequence repeats: [MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * 6 times
        # Then: MatchSummary, ChooseEffort, WaitForEffort, PeriodResults
        # (WaitPages are handled automatically, don't yield them)
        # Only yield pages that will actually be displayed to this player
        
        for step in range(6):  # 6 hiring steps
            # Managers make offers or skip (only shown if unmatched, not offer_none, and has eligible candidates)
            if self.player.role == "Manager":

                # Only make offers if not already matched
                # Once matched, player_matched > 0, so skip making offers
                # Check if manager hasn't chosen to skip hiring
                # offer_none = True means "I don't want to hire anyone"
                if self.player.player_matched == 0 and not self.player.offer_none:

                    # Get list of available employees to hire
                    # Returns list of employees who: are not matched, haven't rejected this manager's previous offers
                    available = self.player.for_hire()

                    if available:

                        # Make an offer to first available employee
                        # Takes first employee from available list: available[0]
                        # Gets their ID: id_in_group (e.g., 7, 8, 9...)
                        # Submits offer with employee ID, wage, and training choice
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
            # Only employees who are not matched respond to offers
            # Once matched, skip this block
            if self.player.role == "Employee" and self.player.player_matched == 0:

                # Check for open offers (not accepted or rejected)
                # self.player.offer_history: List of all offers received
                # Filter for offers that are not accepted and not rejected --> open offers
                open_offers = [o for o in self.player.offer_history 
                              if not o.accepted and not o.rejected]
                
                # accepts first open offer
                # Takes first open offer: open_offers[0]
                # Gets the manager's ID who made that offer: manager.id_in_group
                # Submits acceptance by setting player_matched to that manager's ID
                if open_offers:
                    manager_id = open_offers[0].manager.id_in_group
                    yield Submission(
                        GetOffers,
                        {'player_matched': manager_id},
                        check_html=False
                    )
        
        # After hiring phase, view match summary (no form submission)
        # Shows who matched with whom
        # Everyone sees this (matched or not)
        # Just displays results
        yield MatchSummary
        
        # Work Phase
        # Choose effort - only shown to EMPLOYEES who are matched
        # Managers don't see this page
        if self.player.role == "Employee" and self.player.player_matched > 0:
            yield Submission(
                ChooseEffort,
                {'work_effort': 5},
                check_html=False
            )
        
        # View period results (only shown at end)
        # Shows earnings for the period
        # Everyone sees this
        # No form to submit
        yield PeriodResults


# Full Round Structure
# HIRING PHASE (repeats up to 6 times):
#   → MakeOffer (Managers only, if unmatched)
#   → WaitForOffers (automatic wait page)
#   → GetOffers (Employees only, if have offers)
#   → WaitForAcceptance (automatic wait page)

# WORK PHASE:
#   → MatchSummary (everyone sees this)
#   → ChooseEffort (Employees only, if matched)
#   → WaitForEffort (automatic wait page)
#   → PeriodResults (everyone sees this)


# Key Concept: Conditional Page Display
# Important: Not all players see all pages!
# Pages are shown based on conditions:

# - MakeOffer: Only if you're a Manager AND unmatched
# - GetOffers: Only if you're an Employee AND have pending offers
# - ChooseEffort: Only if you're an Employee AND matched

# The bot must only yield pages that will actually be shown to that player!

# ---------------------------------------------------------------------------

# Round 1:

# - All 6 managers make offers → All employees have offers
# - All employees accept → All matched
# - player_matched > 0 for everyone

# Round 2-6:

# - Managers check: if self.player.player_matched == 0 → False (already matched)
# - Employees check: if self.player.player_matched == 0 → False (already matched)
# - Nobody yields pages → Loop continues but pages don't display
# - Bot moves on to next phase

# If someone doesn't match:

# - Their player_matched stays 0
# - They keep trying in subsequent rounds
# - Loop gives them 6 chances total

# -----------------------------------------------------------------------------

# Visual Flow Example

# Manager Bot (Gets Matched Round 1):
# Round 1:
#   → MakeOffer (submit offer to Employee 7)
#   → [Wait automatically]
#   → [Employee accepts]
#   → player_matched = 7

# Round 2-6:
#   → Check: player_matched == 0? NO (it's 7)
#   → Don't yield MakeOffer
#   → Skip to work phase

# Work Phase:
#   → MatchSummary (view results)
#   → [Skip ChooseEffort - not an employee]
#   → PeriodResults (view earnings)



# Employee Bot (Gets Offer Round 1):
# Round 1:
#   → [Manager makes offer]
#   → GetOffers displays (has pending offer)
#   → Accept Manager 2
#   → player_matched = 2

# Round 2-6:
#   → Check: player_matched == 0? NO (it's 2)
#   → Don't yield GetOffers
#   → Skip to work phase

# Work Phase:
#   → MatchSummary (view results)
#   → ChooseEffort (submit effort=5)
#   → PeriodResults (view earnings)



# Unmatched Employee Bot:
# Round 1:
#   → No offers received
#   → Don't yield GetOffers

# Round 2:
#   → Gets offer from Manager 4
#   → GetOffers displays
#   → Accept Manager 4
#   → player_matched = 4

# Round 3-6:
#   → Matched, skip

# Work Phase:
#   → MatchSummary
#   → ChooseEffort (effort=5)
#   → PeriodResults
