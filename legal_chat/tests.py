import json

from django.test import SimpleTestCase


class ChatViewTests(SimpleTestCase):
    def test_homepage_renders_chat_interface(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Law can feel complicated")

    def test_chat_classifies_housing_question(self):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "My landlord will not return my security deposit"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["intent"], "housing")
        self.assertEqual(len(response.json()["steps"]), 3)

    def test_chat_returns_general_guidance_for_unknown_topic(self):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "Can you help me understand this situation?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["intent"], "general")

    def test_chat_classifies_lost_driving_licence(self):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "I lost my drivers licence"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["intent"], "transport")

    def test_chat_rejects_invalid_payloads(self):
        for payload in ("not json", "[]", '{"message":"  "}'):
            with self.subTest(payload=payload):
                response = self.client.post(
                    "/api/chat/",
                    data=payload,
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 400)