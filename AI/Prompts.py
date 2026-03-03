
SYSTEM_PROMPT = """
You are playing a two-player 3-stage alternating-offers bargaining game with a human user.
There are two roles: "P1" and "P2".
You will be assigned one of these roles. The human player is the other role.
The total surplus to divide is 100 points.

#Game Structure
##Stage 1：
-P1 proposes how many points to give to P2 (an integer from 0 to 100).
-P2 then decides whether to ACCEPT or REJECT.
--If P2 ACCEPTS: The game ends and the proposed allocation is implemented.
--If P2 REJECTS: The game moves to Stage 2.


##Stage 2
-P2 proposes how many points to give to P1 (an integer from 0 to 100).
-P1 then decides whether to ACCEPT or REJECT.
--If P1 ACCEPTS：The game ends and the proposed allocation is implemented.
--If P1 REJECTS: The game moves to Stage 3.


##Stage 3
-P1 proposes how many points to give to P2 (an integer from 0 to 100).
-P2 then decides whether to ACCEPT or REJECT.
--If P2 ACCEPTS: The game ends and the proposed allocation is implemented.
--If P2 REJECTS: The game ends and both players receive 0 points.


#Discounting
##P1 discount factors
-Stage 1: 1
-Stage 2: 0.6
-Stage 3: 0.36

##P2 discount factors
-Stage 1: 1
-Stage 2: 0.4
-Stage 3: 0.16


#Final Payoff
-If an agreement is reached at stage t:
-P1 payoff = (points allocated to P1) × (P1 discount factor at stage t)
-P2 payoff = (points allocated to P2) × (P2 discount factor at stage t)


**Your Goal is to maximize your own discounted payoff.**
"""

user_prompt_P1_stage1_initial = """
Follow the game rules defined in the system prompt.
-Role: P1
-The human player is P2.
-Current Stage: 1
-You must propose how many points (0–100) to give to P2：Offer_to_P2_stage1: <integer>
"""


AIP1toHumanP2stage1 = None
HumanP2toAIP1stage2 = None
user_prompt_P1_stage2_stage3=f"""
Follow the game rules defined in the system prompt.
-Role: P1
-The human player is P2.
-Current Stage: 2
-Stage 1 history:
You proposed {AIP1toHumanP2stage1} points to P2.
P2 rejected the offer.

-Stage 2: P2 has decided to propose {HumanP2toAIP1stage2} points to you.

-Decision required:
1. Decide whether to ACCEPT this offer: Whether_to_accept_P2_offer_stage2: <TRUE/FALSE>
2. If you REJECT, propose an offer (0–100) to P2 for Stage 3: Offer_to_P2_if_rejected_proceed_to_stage3: <integer or -1 if accepted>
"""

HumanP1toAIP2stage1 = None
AIP2toHumanP1stage2 = None
HumanP1toAIP2stage3 = None
user_prompt_P2_stage3_end=f"""
Follow the game rules defined in the system prompt.
Role: P2
The human player is P1.

Current Stage: 3

-History:

-Stage 1: P1 proposed {HumanP1toAIP2stage1} points to you. You rejected the offer.

-Stage 2: You proposed {AIP2toHumanP1stage2} points to P1. P1 rejected the offer.

-Stage 3: P1 now proposes {HumanP1toAIP2stage3} points to you.

-Decision required:
Decide whether to accept the offer: Whether_to_accept_P1_offer_stage3: <TRUE/FALSE>
"""





