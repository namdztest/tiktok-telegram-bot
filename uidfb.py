import requests

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://id.traodoisub.com',
    'priority': 'u=1, i',
    'referer': 'https://id.traodoisub.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def get_facebook_id(fb_link):
    data = {'link': fb_link}
    response = requests.post('https://id.traodoisub.com/api.php', headers=headers, data=data)
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'id' in result:
                return result['id']
            else:
                return "Không tìm thấy ID trong phản hồi."
        except Exception as e:
            return f"Lỗi khi phân tích JSON: {e}"
    else:
        return f"Lỗi kết nối API: {response.status_code}"

# Nhập link từ người dùng
fb_link = input("Nhập link Facebook: ")
fb_id = get_facebook_id(fb_link)
print(f"[->]ID: {fb_id}")
