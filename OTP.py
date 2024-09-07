from flask import Flask, request, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key_here'  # Set a secret key for the session

# Replace with your own phone number
my_phone_number = '+1234567890'

def generate_otp(length: int = 6) -> str:
    otp = ''.join([str(random.randint(0, 9)) for i in range(length)])
    return otp

def send_otp(phone_number: str, otp: str) -> bool:
    if phone_number == my_phone_number:
        print(f'OTP đã được gửi đến {phone_number}: {otp}')
        return True
    else:
        print('Số điện thoại không hợp lệ')
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number_input = request.form['phoneNumber']
        otp = generate_otp()
        if send_otp(phone_number_input, otp):
            session['otp'] = otp
            session['phoneNumber'] = phone_number_input  # Store the phone number in the session
            return '''
                <form action="/verify" method="post">
                    <label for="otp">Nhập mã OTP bạn nhận được:</label><br>
                    <input type="number" id="otp" name="otp"><br>
                    <input type="submit" value="Verify OTP">
                </form>
            '''
        else:
            return 'Không thể gửi OTP vì số điện thoại không hợp lệ.'
    return '''
        <form action="" method="post">
            <label for="phoneNumber">Nhập số điện thoại của bạn:</label><br>
            <input type="tel" id="phoneNumber" name="phoneNumber"><br>
            <input type="submit" value="Send OTP">
        </form>
    '''

@app.route('/verify', methods=['POST'])
def verify_otp():
    otp_input = request.form['otp']
    if 'otp' in session and otp_input == session['otp']:
        print('Xác thực OTP thành công.')
        return 'Xác thực OTP thành công.'
    else:
        print('Mã OTP không hợp lệ, xác thực thất bại.')
        return 'Mã OTP không hợp lệ, xác thực thất bại.'

if __name__ == '__main__':
    app.run(debug=True)