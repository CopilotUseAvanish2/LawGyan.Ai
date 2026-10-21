import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .nlp import get_guidance


def home(request):
    return render(request, "legal_chat/home.html")


@require_POST
def chat(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Send your question as valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "Send your question as a JSON object."}, status=400)

    question = payload.get("message", "")
    if not isinstance(question, str) or not question.strip():
        return JsonResponse({"error": "Type a question to get started."}, status=400)
    if len(question) > 2000:
        return JsonResponse({"error": "Please keep your question under 2,000 characters."}, status=400)

    return JsonResponse(get_guidance(question.strip()))