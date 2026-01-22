import re

regex = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

emails = ["Asilbek2706@gmail.com", "test@mail.ru", "user.name@gmail.com", "info@yandex.uz"]

for email in emails:
    if re.match(regex, email):
        print(f"✅ {email} - To'g'ri")
    else:
        print(f"❌ {email} - Noto'g'ri")