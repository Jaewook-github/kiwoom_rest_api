is_paper_trading = True # 모의투자 여부 : False 또는 True
api_key = "CX2gQlmkWFmyWW3QKaUv7ePoZKbr3l8Vur8ki7q1-AI" # API KEY
api_secret_key = "TFny7ILgk6NHHjLhhP8rRRSGEvIrQP9R3JJuifleGYc" # API SECRET KEY

host = "https://mockapi.kiwoom.com" if is_paper_trading else "https://api.kiwoom.com"
websocket_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket" if is_paper_trading else "wss://api.kiwoom.com:10000/api/dostk/websocket"

