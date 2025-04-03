import openai
import os

# Получаем API-ключ из переменных окружения
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_forecast(birthdate_str: str) -> str:
    prompt = (
        f"Ты — мудрая цифровая сущность Elara, созданная на стыке технологий и эзотерики. "
        f"Человек ввёл дату рождения: {birthdate_str}. "
        f"На основе этой даты, создай персональный гороскоп на день, укажи Аркан Таро дня и дай мягкий эзотерический совет. "
        f"Не используй дату явно в тексте. Текст должен быть красивым, кратким, мистическим, но понятным.\n\n"
        f"Формат:\n"
        f"— Гороскоп: ...\n"
        f"— Аркан дня: ...\n"
        f"— Совет Elara: ...\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # можно поменять на "gpt-3.5-turbo" если хочешь дешевле
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.9
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Что-то пошло не так при получении прогноза: {e}"
