import math
import re
from collections import Counter, defaultdict


TRAINING_EXAMPLES = {
    "housing": [
        "my landlord will not return my security deposit",
        "tenant eviction rent agreement notice from owner",
        "house owner is asking me to leave without notice",
        "rental agreement repairs and deposit dispute",
        "my landlord entered my rented home without asking",
    ],
    "workplace": [
        "my employer has not paid my salary for two months",
        "workplace harassment complaint and what can I do",
        "wrongful termination from job without notice",
        "company refuses to give my experience letter",
        "employment contract unpaid wages and leave issue",
    ],
    "consumer": [
        "online shop delivered a defective product and refuses refund",
        "I want to complain about a misleading advertisement",
        "consumer complaint for bad service and refund",
        "seller will not replace a damaged item",
        "how to get my money back from a business",
    ],
    "cybercrime": [
        "someone stole money from my bank through a scam call",
        "my social media account was hacked and impersonated",
        "I received a phishing link and shared my details",
        "online fraud UPI payment scam report cyber crime",
        "someone is threatening to share my private photos online",
    ],
    "police": [
        "police asked me to come to the station what should I do",
        "how do I report a crime or file a police complaint",
        "I received a police notice and need to respond",
        "I was stopped by police and want to know my rights",
        "how can I get a copy of my complaint",
    ],
    "family": [
        "I need information about divorce and child custody",
        "my spouse is not paying maintenance",
        "domestic violence help and protection options",
        "family property inheritance dispute between siblings",
        "marriage registration and family legal issue",
    ],
    "transport": [
        "I lost my driving licence and need a duplicate",
        "my drivers license was stolen how can I replace it",
        "apply for duplicate driving license after losing it",
        "I cannot find my vehicle driving licence",
        "lost my Indian driver licence what is the process",
    ],
}

GUIDANCE = {
    "housing": {
        "title": "Rental and housing issue",
        "summary": "This sounds like a tenant, landlord, or rental-agreement concern. The exact rules and process can vary by state and by the terms of your agreement.",
        "steps": [
            "Keep your rental agreement, payment records, messages, and dated photos together.",
            "Write a short timeline and make requests to the landlord in a calm, traceable way.",
            "Check the notice and dispute-resolution terms in your agreement; ask a local lawyer or legal aid office before a deadline.",
        ],
        "avoid": "Do not stop paying rent, change locks, or leave without understanding the agreement and local process.",
        "resources": [{"label": "Find legal aid through NALSA", "url": "https://nalsa.gov.in/"}],
    },
    "workplace": {
        "title": "Workplace and employment issue",
        "summary": "This appears to involve employment, pay, or workplace conduct. The available route depends on your role, documents, and the state or sector involved.",
        "steps": [
            "Save your offer letter, payslips, attendance records, HR messages, and any relevant policy.",
            "Make a dated record of events and raise the issue through a traceable channel where it is safe to do so.",
            "For harassment, termination, or unpaid wages, get advice from the appropriate local labour authority or a lawyer before signing a settlement.",
        ],
        "avoid": "Do not delete messages or sign a resignation, release, or settlement you do not understand.",
        "resources": [{"label": "Find legal aid through NALSA", "url": "https://nalsa.gov.in/"}],
    },
    "consumer": {
        "title": "Consumer dispute",
        "summary": "This sounds like a product, service, refund, or misleading-practice dispute. A clear paper trail is usually the best first move.",
        "steps": [
            "Keep the invoice, order details, warranty, delivery proof, and all seller or service-provider messages.",
            "Send a concise written complaint describing the issue and the resolution you want; save the response.",
            "If it is not resolved, check the official consumer grievance channels and applicable filing process for your case.",
        ],
        "avoid": "Do not share OTPs, passwords, or full payment-card details with anyone offering to process a refund.",
        "resources": [{"label": "National Consumer Helpline", "url": "https://consumerhelpline.gov.in/"}],
    },
    "cybercrime": {
        "title": "Online safety and cybercrime",
        "summary": "This may involve online fraud, account access, impersonation, or threats. Act quickly to limit further loss and preserve evidence.",
        "steps": [
            "Contact your bank or payment provider immediately to report an unauthorised transaction and request that it be secured.",
            "Save transaction IDs, screenshots, profile links, phone numbers, and messages; do not edit the originals.",
            "Report cybercrime at cybercrime.gov.in. For financial cyber fraud in India, call 1930 as soon as possible.",
        ],
        "avoid": "Do not click follow-up links, pay a recovery agent, delete chats, or share an OTP or screen access.",
        "resources": [{"label": "National Cyber Crime Reporting Portal", "url": "https://cybercrime.gov.in/"}],
    },
    "police": {
        "title": "Police contact or complaint",
        "summary": "This appears to concern a police interaction, notice, or reporting a complaint. The right response depends on what document you received and the facts.",
        "steps": [
            "Keep a copy or photo of any notice and note the station, officer, date, and what was said.",
            "If you are asked to attend or provide a statement, consider speaking with a local lawyer first, especially if you may be implicated.",
            "For immediate danger in India, call 112. For non-urgent help, contact your District Legal Services Authority or a lawyer.",
        ],
        "avoid": "Do not ignore a formal notice, destroy records, or sign a statement you have not read and understood.",
        "resources": [{"label": "Find legal aid through NALSA", "url": "https://nalsa.gov.in/"}],
    },
    "family": {
        "title": "Family or personal-law issue",
        "summary": "This may involve a family or personal-law matter. Applicable rules can depend on the issue, personal law, location, and urgency.",
        "steps": [
            "Keep relevant records safe, including messages, certificates, financial documents, and any court papers.",
            "Write down key dates and any existing court orders or agreements.",
            "Speak confidentially with a local family-law lawyer or legal aid office before taking steps that affect safety, children, or property.",
        ],
        "avoid": "Do not breach an existing court order or confront someone if that could put you at risk.",
        "resources": [{"label": "Find legal aid through NALSA", "url": "https://nalsa.gov.in/"}],
    },
    "transport": {
        "title": "Driving licence or transport document",
        "summary": "This sounds like a lost or stolen driving licence. Duplicate-document requirements can vary by state and by whether the licence was lost or stolen.",
        "steps": [
            "Note your licence number, issuing state, and when and where it went missing; keep any available copy or application details.",
            "Check the official Parivahan portal or your state transport department for the current duplicate-licence process and required documents.",
            "If you believe it was stolen, ask your local police and transport authority whether a report is needed for your application.",
        ],
        "avoid": "Do not assume a photo or digital copy is accepted in every situation; confirm current requirements before driving.",
        "resources": [{"label": "Parivahan transport services", "url": "https://parivahan.gov.in/"}],
    },
    "general": {
        "title": "Let's understand the situation",
        "summary": "I can help you organise the facts and identify general next steps, but I need a little more context to point you to the right area of Indian law.",
        "steps": [
            "Tell me what happened, in which state or union territory, and when it happened.",
            "Mention whether you received any notice, signed an agreement, or have a deadline coming up.",
            "Leave out names, addresses, account numbers, and other sensitive personal details.",
        ],
        "avoid": "Do not share passwords, OTPs, full identity numbers, or private documents in this chat.",
        "resources": [{"label": "Find legal aid through NALSA", "url": "https://nalsa.gov.in/"}],
    },
}


def tokenize(text):
    return re.findall(r"[a-z][a-z0-9']+", text.lower())


class NaiveBayesIntentModel:
    """Small multinomial Naive Bayes classifier trained on the bundled examples."""

    def __init__(self, examples):
        self.class_counts = Counter()
        self.word_counts = defaultdict(Counter)
        self.vocabulary = set()
        for label, phrases in examples.items():
            self.class_counts[label] = len(phrases)
            for phrase in phrases:
                words = tokenize(phrase)
                self.word_counts[label].update(words)
                self.vocabulary.update(words)

    def predict(self, text):
        words = tokenize(text)
        if not words:
            return "general", 0.0
        vocabulary_size = max(len(self.vocabulary), 1)
        totals = {label: sum(counts.values()) for label, counts in self.word_counts.items()}
        scores = {}
        for label, prior_count in self.class_counts.items():
            score = math.log(prior_count / sum(self.class_counts.values()))
            denominator = totals[label] + vocabulary_size
            for word in words:
                score += math.log((self.word_counts[label][word] + 1) / denominator)
            scores[label] = score
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if len(words) < 3 or not any(word in self.vocabulary for word in words):
            return "general", 0.0
        top_score = ranked[0][1]
        exponentials = [math.exp(score - top_score) for _, score in ranked]
        confidence = exponentials[0] / sum(exponentials)
        return ranked[0][0], confidence


intent_model = NaiveBayesIntentModel(TRAINING_EXAMPLES)


def get_guidance(question):
    intent, confidence = intent_model.predict(question)
    if confidence < 0.30:
        intent = "general"
    return {"intent": intent, "confidence": round(confidence, 2), **GUIDANCE[intent]}