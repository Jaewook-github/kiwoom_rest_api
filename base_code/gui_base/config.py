is_paper_trading = True  # 모의투자 여부: False 또는 True
api_key = "VMbARSlQb4f4AyKjoEkbettQlBWW3dPkzyrp1-DMsGY"  # API KEY
api_secret_key = "djEpkavpWJ3G4pSTrQ19JT2dPQFDtsG8uo2T-H90A0Y"  # API SECRET KEY

host = "https://mockapi.kiwoom.com" if is_paper_trading else "https://api.kiwoom.com"
websocket_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket" if is_paper_trading else "wss://api.kiwoom.com:10000/api/dostk/websocket"