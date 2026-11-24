"""Chapter 3, step 4: measure retrieval before you trust answers.
Fast, because no chat model is needed.  Run:  python rag_eval.py
"""
from rag_retrieve import hybrid_search, keyword_search, semantic_search

# (question, the policy that must be in the top 3). Add your own in Lab 4.
EVAL = [
    ("Someone used my card without asking me. How long do I have to tell you?", "card-security"),
    ("I lost my debit card on the train", "card-security"),
    ("The ATM took money from my account but no notes came out", "debit-atm"),
    ("My NEFT did not reach my brother. When do I get it back?", "neft"),
    ("I paid the wrong person on UPI by mistake", "upi"),
    ("Can I break my FD early?", "fixed-deposits"),
    ("My account is frozen because I didn't use it", "kyc"),
    ("Will I pay extra if I repay my home loan early?", "home-loans"),
    ("My bank card was used by someone else without permission", "card-security"),
("I misplaced my ATM card. How can I stop someone using it?", "card-security"),
("What is the CRD-07 card security rule?", "card-security"),
("What is the Rs 50,000 ATM withdrawal limit?", "debit-atm"),
]


def hit_rate(search, k: int = 3) -> tuple[int, list[str]]:
    hits, misses = 0, []
    for question, doc_id in EVAL:
        found = [chunk_id.split("#")[0] for chunk_id in search(question, k)]
        if doc_id in found:
            hits += 1
        else:
            misses.append(f"{question!r} -> {found}")
    return hits, misses


if __name__ == "__main__":
    for name, search in [("keyword", keyword_search), ("semantic", semantic_search), ("hybrid", hybrid_search)]:
        hits, misses = hit_rate(search)
        print(f"{name:8} hit@3 = {hits}/{len(EVAL)}")
        for miss in misses:
            print(f"    missed: {miss}")
