import telegram   #텔레그램 모듈을 가져옵니다.

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.

bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

arr = []
for u in updates:   # 내역중 메세지를 출력합니다.
    arr.append(u.message['chat']['id'])

    print(u.message['chat']['id'])

arr = list(set(arr))
print(arr)

chat_id = '1028099025'
bot.sendMessage(chat_id=chat_id, text="안녕하세요, 무비 봇입니다.")

