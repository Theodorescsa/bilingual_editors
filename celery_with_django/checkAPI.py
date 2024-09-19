import requests
import aiohttp


class apiFunction:
    def __init__(self):
        self.url = ""
        
    def get_data():
        try:
            url = 'https://admin.metalearn.vn/VideoBilingualEditor/GetListVideo'
            
            # Gửi yêu cầu GET tới API
            response = requests.post(url)
            
            # Kiểm tra mã trạng thái phản hồi
            if response.status_code == 200:
                # Chuyển phản hồi từ JSON thành dictionary Python
                data = response.json()
                return data
            else:
                print(f"Failed to get data: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            print(f"Error at get_data api: {e}")
            return None
    def postSession(data):
        try:
            url = 'https://admin.metalearn.vn/VideoBilingualEditor/InsertVideo'

            # The object to post
            data = data

            # Make the POST request
            response = requests.post(url, json=data)
            print("Post success")
            return True
        except Exception as e:
            print(f"Error at post api: {e} ")
            return False

    def putSession(data):
        try:
            url = 'https://admin.metalearn.vn/VideoBilingualEditor/InsertVideo'

            # The object to post
            data = data

            # Make the POST request
            response = requests.put(url, json=data)
            print("Put success")
            return True
           
        except Exception as e:
            print(f"Error at put api: {e} ")
            return False
    
    def deleteSession(code):
        try:
            url = f'https://admin.metalearn.vn/VideoBilingualEditor/DeleteVideo?VideoCode={code}'

            response = requests.post(url)
            print("Delete success")
            return True
        
        except Exception as e:
            print(f"Error at delete api: {e} ")
            return False
    
    async def postSession2(data):
        print("go post 22")

        try:
            async with aiohttp.ClientSession() as session:
                # Adjust parameter names and use form-encoded data
                data = data
                async with session.post('https://os.3i.com.vn/MobileMrp/InsertOperatingVideoTrack', data=data) as response:
                        if response.status == 200:
                            print("success")

        except Exception as e:
            print(f"Error during request: {e}")
            
model = apiFunction
data = model.get_data()
print(data)