# LawGyan.ai

LawGyan.ai is a Django prototype for an Indian-law guidance chatbot. It uses a small, locally trained Multinomial Naive Bayes text classifier to identify common topic areas, then returns structured general information, possible next steps, things to avoid, and links to official or legal-aid resources.

The classifier is a demonstration, not a legal expert system. It is trained only on the sample phrases in `legal_chat/nlp.py`; it does not retrieve legislation, verify current law, or replace a qualified lawyer. Review all guidance and official links before using this prototype with real users.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Check the chat endpoint

The browser sends a CSRF-protected JSON `POST` to `/api/chat/` with a `message` field. Django returns the predicted topic and structured guidance. Questions are not stored by this prototype.

## Before deployment

- Set `DJANGO_SECRET_KEY` to a strong secret, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` to your hostnames.
- Configure HTTPS, logging, rate limiting, and privacy/data-retention practices.
- Have Indian legal professionals review the classifier, guidance, jurisdiction handling, and all linked resources.