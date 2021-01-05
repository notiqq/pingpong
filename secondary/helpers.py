import base64

class Helper:
    
    @staticmethod
    def encode_base64(value):
        message_bytes = value.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    @staticmethod
    def decode_base64(value):
        base64_bytes = value.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
