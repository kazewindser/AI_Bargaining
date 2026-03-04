
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









