from . import jalali
from django.utils import timezone
import http.client
import json

def persian_numbers_converter(string):
    numbers = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }

    for e, p in numbers.items():
        string = string.replace(e, p)
    
    return string


def jalali_converter(time):
    jmonths = [
        'فروردین',  'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند', 
    ]

    time = timezone.localtime(time)

    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}"
    return persian_numbers_converter(output)





def send_otp_code(mobile, code):

    conn = http.client.HTTPSConnection("api.sms.ir")
    payload = json.dumps({
    "mobile": f"0{mobile}",
    "templateId": 100000,
    "parameters": [
        {
        "name": "Code",
        "value": str(code)
        }
    ]
    })
    headers = {
    'x-api-key': 'zvhhzzfkmPYmLDqgkJLaU83KQR8aQj4ySe8lojdUq56b0ZJ2BnQwh43qNxFAmhXU',
    'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v1/send/verify", payload, headers)
        res = conn.getresponse()
        data = res.read()
    except:
        print("دوباره امتحان کنید. سرور پیامک پاسگو نمیباشد.")

   
    # print(data.decode("utf-8"))

