from services.config.workout_config import PROMPT

class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue=None):
        prompt = f"Event: {event}"
        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        # List of models to try in order of priority
        candidate_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]

        for model_name in candidate_models:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.4
                )
                text = response.choices[0].message.content.strip()
                self.history.append({"role": "assistant", "content": text})
                return text
            except Exception:
                # If a model returns 404 or fails, try the next model silently
                continue

        # Safe fallback response if all Groq models fail or API key is invalid
        return "Keep going! Focus on controlled reps and steady breathing."