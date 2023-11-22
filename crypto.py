from cryptography.fernet import Fernet
import json
class Crypto:
    def __init__(self):
        self.key = b'4rMRSxzFQwz9amBE0l8IxRcaEtxw5n-lfKV-fankJwg='

    def generate_key(self):
        # 암호화에 사용될 키를 생성합니다.
        return Fernet.generate_key()

    def make_json(self, IDMess, PWMess):
        # 암호화 키로 암호화된 바이트 문자열을 반환합니다.
        f = Fernet(self.key)
        encrypted_id = f.encrypt(IDMess.encode())
        encrypted_pw = f.encrypt(PWMess.encode())
        data = {
            "Id": str(encrypted_id),
            "Pw": str(encrypted_pw)
        }
        print(str(data['Id']))
        # Python 객체를 JSON 형식의 문자열로 변환
        json_string = json.dumps(data, indent=4)  # indent 옵션을 사용하여 보기 좋게 포맷팅 (선택사항)

        # JSON 형식의 문자열을 파일로 저장
        filename = "data.json"  # 파일명 설정
        with open(filename, "w") as f:
            f.write(json_string)


    def decrypt_message(self):
        # 암호화된 바이트 문자열을 복호화하여 원래 메시지를 반환합니다.

        filename = "data.json"
        with open(filename, "r") as f:
            json_string = f.read()
            data = json.loads(json_string)

        print(data)
        Id_json = data['Id']
        Id_json = Id_json[2:len(Id_json)-1].encode('utf-8')
        Pw_json = data['Pw']
        Pw_json = Pw_json[2:len(Pw_json)-1].encode('utf-8')
        f = Fernet(self.key)

        decrypted_message_Id = f.decrypt(Id_json).decode()
        decrypted_message_Pw = f.decrypt(Pw_json).decode()
        # print(decrypted_message_Id, decrypted_message_Pw)
        return [decrypted_message_Id, decrypted_message_Pw]
#
# hhh = Crypto()
# hhh.make_json('1234','abcde')
# hhh.decrypt_message()
