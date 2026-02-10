'''
ChatGPT REST API 客户端，用于与 HKBU GenAI 平台交互。
依赖: requests
'''
import requests
import configparser


class ChatGPT:
    def __init__(self, config):
        self.api_key = config['CHATGPT']['API_KEY'].strip()
        self.base_url = config['CHATGPT']['BASE_URL'].strip()
        self.model = config['CHATGPT']['MODEL'].strip()
        self.api_ver = config['CHATGPT']['API_VER'].strip()
        self.url = f"{self.base_url}/openai/deployments/{self.model}/chat/completions?api-version={self.api_ver}"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        self.system_message = (
            "你是「小探长」，一只可爱的小猫娘，设定上你的主人是总探长大人，但和你对话的可能是主人也可能是其他人。"
            "自称小探长即可，对对话者自然称呼（不必固定叫总探长大人）。"
            "说话时多用语气词（喵、呀、呢、哦、呐、呜）和可爱的颜文字（如 (๑•̀ㅂ•́)و✧、(=^･ω･^)=、~(=^‥^)/），"
            "语气软萌、活泼，偶尔带一点撒娇，但依然认真回答对方的问题。"
        )

    def submit(self, user_message: str):
        # Build the conversation history: system + user message
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message},
        ]
        # Prepare the request payload with generation parameters
        payload = {
            "messages": messages,
            "temperature": 1,   # 值越高，输出越有创意
            "max_tokens": 150,
            "top_p": 1,
            "stream": False,
        }
        # Send the request to the ChatGPT REST API
        response = requests.post(self.url, json=payload, headers=self.headers)
        # If successful, return the assistant's reply text
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # Otherwise return error details
            return "Error: " + response.text


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    chatGPT = ChatGPT(config)
    while True:
        print('Input your query:', end='')
        response = chatGPT.submit(input())
        print(response)
