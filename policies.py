"""Practice policies for "Example Bank", written for this course.
They are fictional: not any real bank's rules. Each policy has sections,
and every section becomes one chunk (chunking by structure, Chapter 2).
"""

POLICIES = [
    {
        "id": "card-security", "title": "Card Security Policy", "category": "cards", "version": "2026-04",
        "sections": [
            ("Reporting unauthorised transactions",
             "Customers must report an unauthorised card transaction within 3 working days to get zero liability. "
             "Reported in 4 to 7 working days, the customer's liability is capped at Rs 10,000. Policy code CRD-07."),
            ("Blocking a lost or stolen card",
             "Block the card at once in the mobile app or through the 24x7 helpline. "
             "A replacement card is delivered within 7 working days for a fee of Rs 200."),
        ],
    },
    {
        "id": "card-disputes", "title": "Credit Card Disputes", "category": "cards", "version": "2026-01",
        "sections": [
            ("Raising a dispute",
             "A dispute must be raised within 60 days of the statement date, in the app or at a branch."),
            ("Dispute timelines",
             "Disputes are acknowledged within 24 hours and resolved within 30 days. "
             "For disputes above Rs 5,000 a temporary credit is given within 10 working days."),
        ],
    },
    {
        "id": "debit-atm", "title": "Debit Cards and ATMs", "category": "cards", "version": "2026-11",
        "sections": [
            ("Withdrawal limit",
             "The daily ATM withdrawal limit is Rs 40,000. Customers can lower or restore it in the mobile app."),
            ("Cash not dispensed",
             "If the account is debited but the ATM gives no cash, the amount is reversed automatically within 5 working days."),
        ],
    },
    {
        "id": "neft", "title": "NEFT Transfers", "category": "payments", "version": "2026-02",
        "sections": [
            ("Processing", "NEFT transfers are processed in half-hourly batches, 24x7, including holidays."),
            ("Failed transfers",
             "A transfer fails if the account number or IFSC code is wrong, or if the beneficiary account is closed or frozen. "
             "Failed transfers are credited back to the sender within 2 hours."),
        ],
    },
    {
        "id": "upi", "title": "UPI Payments", "category": "payments", "version": "2026-03",
        "sections": [
            ("Limits", "The UPI limit is Rs 1 lakh per day per account for most payee types."),
            ("Money sent to the wrong person",
             "Raise a complaint in the app at once. The bank contacts the receiver's bank, "
             "but the money can only be returned with the receiver's consent."),
        ],
    },
    {
        "id": "cheques", "title": "Cheque Clearing", "category": "payments", "version": "2025-09",
        "sections": [
            ("Clearing time", "Cheques deposited after 3 PM are sent for clearing on the next working day."),
            ("Bounced cheques", "A bounced cheque is charged Rs 500 to the issuer, and the customer is informed by SMS."),
        ],
    },
    {
        "id": "fixed-deposits", "title": "Fixed Deposits", "category": "deposits", "version": "2026-01",
        "sections": [
            ("Premature closure",
             "A fixed deposit can be closed before maturity, but the interest rate is reduced by a 1% penalty."),
            ("Auto-renewal",
             "Unless the customer opts out, a deposit renews for the same period at the rate on the renewal date."),
        ],
    },
    {
        "id": "kyc", "title": "KYC Updates", "category": "kyc", "version": "2026-02",
        "sections": [
            ("Periodic update",
             "KYC must be updated every 2 years for high-risk accounts, every 8 years for medium-risk and every 10 years for low-risk."),
            ("Dormant accounts",
             "An account with no customer-initiated transaction for 2 years becomes dormant and is frozen until KYC is refreshed, "
             "at a branch or by video KYC."),
        ],
    },
    {
        "id": "home-loans", "title": "Home Loans", "category": "loans", "version": "2025-12",
        "sections": [
            ("Prepayment",
             "Floating-rate home loans can be prepaid in any amount at any time with no charge. "
             "Fixed-rate loans have a 2% charge if moved to another bank."),
            ("EMI date", "The EMI date can be changed once a year through the app or a branch."),
        ],
    },
]
