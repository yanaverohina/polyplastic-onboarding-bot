import sys
sys.stdout.reconfigure(line_buffering=True)
import time
from typing import List, Dict, Any, Optional

import db
from max_client import client, BASE_URL, send_message

def get_hr_keyboard() -> List[List[Dict[str, str]]]:
    return [
        [{"type": "callback", "text": "👥 Список новичков (Сводка)", "payload": "btn_hr_employees"}],
        [{"type": "callback", "text": "📥 Обращения к HR", "payload": "btn_hr_tickets"}]
    ]

def get_hr_contact_keyboard() -> List[List[Dict[str, str]]]:
    return [
        [{"type": "callback", "text": "Связаться с рекрутером", "payload": "contact_hr_now"}]
    ]

def handle_message(chat_id: str, user_id: int, text: str, sender_name: str) -> None:
    user = db.get_or_create_user(user_id, sender_name)
    role = user.get('role', 'employee')
    text_lower = text.lower().strip()
    
    if text_lower in ['/start', 'привет', 'меню', 'старт']:
        if role == 'hr':
            send_message(chat_id, f"Привет, {sender_name}! Я Корсик. Панель HR активна.", get_hr_keyboard())
        else:
            send_message(chat_id, "Добро пожаловать в нашу команду!\nПривет-привет-привет! 🐾 Меня зовут Корсик, ваш персональный гид по миру Группы ПОЛИПЛАСТИК! 🤗")
            time.sleep(1)
            send_message(chat_id, "Рад знакомству и обещаю сделать вашу адаптацию веселой, легкой и комфортной! 💃 Вместе мы изучим компанию и найдем друзей среди лучших специалистов отрасли. 🌟")
            time.sleep(1)
            # ЖДЕМ ОТВЕТА (кнопки)
            send_message(chat_id, "Как мы будем общаться?", [
                [{"type": "callback", "text": "На ТЫ", "payload": "tone_informal"}],
                [{"type": "callback", "text": "На ВЫ", "payload": "tone_formal"}]
            ])
            
    elif text_lower == '/demo_minus1':
        send_message(chat_id, "Привет! Уже завтра наступит твой первый рабочий день. Ты готов?", [
            [{"type": "callback", "text": "Да, жду не дождусь!", "payload": "ready_yes"}],
            [{"type": "callback", "text": "Готов/Готова", "payload": "ready_ok"}],
            [{"type": "callback", "text": "Да, но немного волнуюсь", "payload": "ready_nervous"}]
        ])

    elif text_lower == '/demo_day1':
        send_message(chat_id, "Поздравляю с первым рабочим днем! 🥳\n\nУверен, что ты будешь отлично справляться со своими задачами, вносить свой вклад в наше общее дело и делиться идеями. Мы всегда готовы поддержать тебя и создать комфортные условия для работы.")
        time.sleep(1)
        send_message(chat_id, "Наш офис довольно большой, но я помогу тебе в нем разобраться! Хочешь я покажу тебе подробную карту?", [
            [{"type": "callback", "text": "Показать карту", "payload": "map_yes"}],
            [{"type": "callback", "text": "Я уже ориентируюсь", "payload": "map_no"}]
        ])

    elif text_lower == '/demo_day3':
        send_message(chat_id, "Привет! Надеюсь, что ты уже чуть лучше понимаешь нашу компанию, наши ценности и правила. Чтобы полностью влиться в команду, твой руководитель подготовил для тебя адаптационный план.")
        time.sleep(1)
        send_message(chat_id, "Первые пару дней на новом месте могут быть немного сложными, поэтому мы предлагаем пройти тебе опрос, чтобы поделиться с нами своими впечатлениями!\n\nВопрос 1: Были ли вопросы при оформлении?", [
            [{"type": "callback", "text": "Все отлично!", "payload": "poll_d3_q1_a"}],
            [{"type": "callback", "text": "Остались вопросы", "payload": "poll_d3_q1_b"}],
            [{"type": "callback", "text": "Трудности с документами", "payload": "poll_d3_q1_c"}]
        ])

    elif text_lower == '/demo_month2':
        send_message(chat_id, "Привет! Поздравляю тебя с успешным завершением месяца работы! Так держать!")
        time.sleep(1)
        send_message(chat_id, "Мы придаём большое значение успешной адаптации новых сотрудников. Подскажи, как идет работа по адаптационному плану?", [
            [{"type": "callback", "text": "Все хорошо! Продвигаюсь по плану", "payload": "poll_m2_a"}],
            [{"type": "callback", "text": "Все ок! Немного отстаю от графика", "payload": "poll_m2_b"}],
            [{"type": "callback", "text": "Я отстаю от графика.", "payload": "poll_m2_c"}]
        ])

    elif text_lower == '/demo_final':
        send_message(chat_id, "Дорогой друг,\nЭти 3 месяца пролетели так быстро! Ты только начинаешь познавать нашу компанию и вот, уже завершился твой адаптационный период...\n\nПока эмоции все еще свежи, поделишься с нами своими впечатлениями от прохождения испытательного срока?")
        time.sleep(1)
        send_message(chat_id, "Вопрос 1: Что было самым сложным в период адаптации?", [
            [{"type": "callback", "text": "Со всем справился", "payload": "poll_fin_q1_a"}],
            [{"type": "callback", "text": "Коммуникации с другими отделами", "payload": "poll_fin_q1_b"}],
            [{"type": "callback", "text": "Нечеткие задачи", "payload": "poll_fin_q1_c"}]
        ])

    elif text_lower == '/hr':
        send_message(chat_id, "Переключаю в режим HR-панели...", get_hr_keyboard())
    else:
        msg = f"Корсик: Я передам твой вопрос коллегам из подбора персонала и вернусь с ответом! Либо ты можешь связаться с ними напрямую."
        send_message(chat_id, msg, get_hr_contact_keyboard())

def handle_callback(chat_id: str, user_id: int, payload_data: str, query_id: str) -> None:
    db.get_or_create_user(user_id, "Unknown")
    
    # === День -3 ===
    if payload_data in ["tone_informal", "tone_formal"]:
        tone = "informal" if payload_data == "tone_informal" else "formal"
        db.update_user_tone(user_id, tone)
        format_text = "на ТЫ" if tone == "informal" else "на ВЫ"
        
        send_message(chat_id, f"Договорились! Очень приятно познакомиться, будем общаться {format_text}.")
        time.sleep(1)
        send_message(chat_id, "Для того, чтобы ты пришел подготовленный в свой первый рабочий день, ознакомься со списком необходимых для оформления документов и подготовь их к своему выходу на работу:\n1. Трудовая книжка и сведения о трудовой деятельности\n2. Паспорт\n3. СНИЛС\n4. ИНН\n5. Документ об образовании\n6. Свидетельство о браке/разводе\n7. Свидетельство о рождении ребенка\n8. Документы воинского учета\n9. Фотографии 3*4 в количестве 2шт")
        time.sleep(1)
        send_message(chat_id, "Чтобы дорога до офиса была комфортнее, у нас есть корпоративный транспорт! Рассказать о маршрутах и расписании?", [
            [{"type": "callback", "text": "Да, расскажи", "payload": "transport_yes"}],
            [{"type": "callback", "text": "Нет, спасибо", "payload": "transport_no"}]
        ])
        # Ждем следующего клика
        
    elif payload_data in ["transport_yes", "transport_no"]:
        if payload_data == "transport_yes":
            send_message(chat_id, "Отлично! Вот расписание корпоративного транспорта: [PDF_ПРИКРЕПЛЕН]")
        else:
            send_message(chat_id, "Понял! Если передумаешь, маршруты всегда можно найти на корпоративном портале.")
            
        time.sleep(1)
        send_message(chat_id, "Я готов поделиться самыми интересными фактами о своей организации.\n\n🧑🏼‍🔧 Факт №1: Я горжусь тем, что работаю в компании, которая делает мир лучше каждый день! Наши инновационные трубы помогают обеспечивать чистой водой миллионы людей по всей стране...")
        time.sleep(1)
        send_message(chat_id, "Очень скоро мы начнем полноценное погружение в компанию, а пока отдыхай. Я напишу тебе за день до выхода на работу \n\nДо встречи! 👋🏻")
        # Конец этапа -3 дня
        
    # === День -1 ===
    elif payload_data in ["ready_yes", "ready_ok", "ready_nervous"]:
        if payload_data in ["ready_yes", "ready_ok"]:
            send_message(chat_id, "Супер! Мне нравится твой настрой ✨")
        else:
            send_message(chat_id, "Это нормально - немного волноваться в первый рабочий день. Поверь мне, я сам через это проходил, когда меня создавали 😓")
            
        time.sleep(1)
        send_message(chat_id, "Для того, чтобы ты пришел подготовленный в свой первый рабочий день, напоминаю про список необходимых для оформления документов, подготовь их к своему выходу на работу.")
        # Конец этапа -1 день
        
    # === День 1 ===
    elif payload_data in ["map_yes", "map_no"]:
        if payload_data == "map_yes":
            send_message(chat_id, "Держи подробную карту территории/офиса: [КАРТА_ПРИКРЕПЛЕНА]")
        else:
            send_message(chat_id, "Хорошо! Если заблудишься, всегда можешь спросить меня.")
            
        time.sleep(1)
        send_message(chat_id, "Тебе предстоит многое узнать о нашей компании. Но сначала решим пару организационных вопросов.\n\nНа твоем рабочем месте тебя будет ждать необходимая техника. Для тебя уже заведена учетная запись и доступы IT. Есть ли у тебя все необходимые доступы и материалы?", [
            [{"type": "callback", "text": "Да, все есть", "payload": "access_yes"}],
            [{"type": "callback", "text": "Нет", "payload": "access_no"}]
        ])
        
    elif payload_data in ["access_yes", "access_no"]:
        if payload_data == "access_yes":
            send_message(chat_id, "Замечательно! Тогда пока осваивайся, а я напишу тебе чуть позже.")
        else:
            send_message(chat_id, "Ничего страшного! В таком случае лучше всего уточнить у твоего руководителя, когда будут заведены доступы и предоставлены необходимые материалы.")
            
        time.sleep(1)
        send_message(chat_id, "Хочешь, подскажу, где пообедать?", [
            [{"type": "callback", "text": "Да!", "payload": "lunch_yes"}],
            [{"type": "callback", "text": "Нет, спасибо!", "payload": "lunch_no"}]
        ])
        
    elif payload_data in ["lunch_yes", "lunch_no"]:
        if payload_data == "lunch_yes":
            send_message(chat_id, "Приятного аппетита! Вот список лучших мест: [МЕНЮ_ПРИКРЕПЛЕНО]")
        else:
            send_message(chat_id, "Я тебя понял! Если ты передумаешь, ты всегда можешь набрать /Food и я подскажу тебе где пообедать.")
            
        time.sleep(1)
        send_message(chat_id, "Первый рабочий день позади!\n\nЭто очень важный момент, первые шаги в новой работе всегда особенные. Я уверен, что ты успешно справился со своими первыми задачами.")
        
    # === Опрос День 3 ===
    elif payload_data in ["poll_d3_q1_a", "poll_d3_q1_b", "poll_d3_q1_c"]:
        if payload_data == "poll_d3_q1_b":
            send_message(chat_id, "Хорошо, я тебя понял! Помни, что ты всегда можешь связаться с рекрутером, описать проблему или задать интересующие тебя вопросы.", get_hr_contact_keyboard())
        elif payload_data == "poll_d3_q1_c":
            send_message(chat_id, "Очень важно иметь возможность полноценно изучить подписываемые документы. Свяжись с HR, чтобы решить вопрос.", get_hr_contact_keyboard())
            
        time.sleep(1)
        send_message(chat_id, "Вопрос 2: Как тебя встретили новые коллеги?", [
            [{"type": "callback", "text": "Отлично!", "payload": "poll_d3_q2_a"}],
            [{"type": "callback", "text": "Пока присматриваюсь", "payload": "poll_d3_q2_b"}],
            [{"type": "callback", "text": "Никак, все заняты", "payload": "poll_d3_q2_c"}]
        ])
        
    elif payload_data in ["poll_d3_q2_a", "poll_d3_q2_b", "poll_d3_q2_c"]:
        if payload_data == "poll_d3_q2_c":
            send_message(chat_id, "Жалко, что не удалось познакомиться с новыми коллегами. Если нужна помощь — пиши HR.", get_hr_contact_keyboard())
            
        time.sleep(1)
        send_message(chat_id, "Вопрос 3: Понятны ли тебе задачи на испытательный срок?", [
            [{"type": "callback", "text": "Да, все понятно!", "payload": "poll_d3_q3_a"}],
            [{"type": "callback", "text": "Жду разъяснений", "payload": "poll_d3_q3_b"}],
            [{"type": "callback", "text": "Пока ничего не понял", "payload": "poll_d3_q3_c"}]
        ])
        
    elif payload_data.startswith("poll_d3_q3_"):
        if payload_data == "poll_d3_q3_a":
            send_message(chat_id, "Отлично 💪🏻 Спасибо за обратную связь! Увидимся завтра 👋🏻")
        else:
            send_message(chat_id, "Понимание своих задач - ключевой элемент. Обязательно обсуди это с руководителем или HR.", get_hr_contact_keyboard())

    # === Месяц 2 ===
    elif payload_data in ["poll_m2_a", "poll_m2_b", "poll_m2_c"]:
        if payload_data in ["poll_m2_a", "poll_m2_b"]:
            send_message(chat_id, "Прекрасно! Тогда, продолжай в том же духе 💪🏻")
        else:
            send_message(chat_id, "Спасибо за обратную связь! Ты можешь связаться с HR-специалистом, описав трудности, с которыми ты столкнулся.", get_hr_contact_keyboard())

    # === Окончание ИС ===
    elif payload_data in ["poll_fin_q1_a", "poll_fin_q1_b", "poll_fin_q1_c"]:
        send_message(chat_id, "Принято! Спасибо за ответ.")
        time.sleep(1)
        send_message(chat_id, "Вопрос 2: Планируешь ли ты продолжить работу по итогам испытательного срока?", [
            [{"type": "callback", "text": "Да, однозначно!", "payload": "poll_fin_q2_a"}],
            [{"type": "callback", "text": "Не уверен", "payload": "poll_fin_q2_b"}],
            [{"type": "callback", "text": "Нет, задумываюсь об уходе", "payload": "poll_fin_q2_c"}]
        ])
        
    elif payload_data in ["poll_fin_q2_a", "poll_fin_q2_b", "poll_fin_q2_c"]:
        if payload_data == "poll_fin_q2_a":
            send_message(chat_id, "Мы рады видеть тебя в нашей команде и надеемся, что ты останешься с нами на долгое время! 🎉\n\nКажется, все вопросы заданы, а материалы переданы. Пришло время нам с тобой попрощаться. До встречи! 👋🏻")
        else:
            send_message(chat_id, "Очень жаль, что ты сомневаешься в дальнейшем сотрудничестве с нами. Могу ли я поинтересоваться, что на это повлияло? Готов обсудить это с рекрутером?", get_hr_contact_keyboard())

    elif payload_data == "contact_hr_now":
        send_message(chat_id, "Уведомление отправлено твоему куратору/рекрутеру! Он свяжется с тобой в ближайшее время.")

    # Отправляем подтверждение (ack) серверу
    try:
        client.post(f"{BASE_URL}/answers", params={"callback_id": query_id}, json={"message": "ОК"})
    except:
        pass

def main() -> None:
    print("[INFO] Бот Корсик запущен (Строгий интерактивный режим).")
    db.init_db()
    marker: Optional[str] = None
    
    while True:
        params: Dict[str, Any] = {"timeout": 10}
        if marker: 
            params["marker"] = marker
        try:
            resp = client.get(f"{BASE_URL}/updates", params=params)
            if resp.status_code == 200:
                data = resp.json()
                marker = data.get("marker")
                for upd in data.get("updates", []):
                    update_type = upd.get("update_type")
                    if update_type == "message_created":
                        msg = upd.get("message", {})
                        body = msg.get("body", {})
                        text = body.get("text", "")
                        sender_name = msg.get("sender", {}).get("name", "Unknown")
                        user_id = msg.get("sender", {}).get("user_id")
                        chat_id = msg.get("recipient", {}).get("chat_id")
                        
                        if text and chat_id and user_id:
                            handle_message(chat_id, user_id, text, sender_name)
                            
                    elif update_type == "message_callback":
                        cb = upd.get("callback", {})
                        query_id = cb.get("callback_id")
                        payload_data = cb.get("payload")
                        user_id = cb.get("user", {}).get("user_id")
                        chat_id = upd.get("message", {}).get("recipient", {}).get("chat_id")
                        
                        if payload_data and user_id and chat_id:
                            handle_callback(chat_id, user_id, payload_data, query_id)
        except Exception as e:
            import traceback
            print(f"[ERROR] Внешняя ошибка поллинга: {e}")
            traceback.print_exc()
            time.sleep(2)


if __name__ == '__main__':
    main()
