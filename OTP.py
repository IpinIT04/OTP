from flask import Flask, request, session, render_template_string
import pyotp
import random

app = Flask(__name__)
app.secret_key = 'secret_key_here'

my_phone_number = '1234567890'

def generate_otp() -> str:
    totp = pyotp.TOTP('base32secret3232')
    otp_code = totp.now()
    return otp_code

def send_otp(phone_number: str, otp: str) -> bool:
    if phone_number == my_phone_number:
        print(f'OTP đã được gửi đến {phone_number}: {otp}')
        return True
    else:
        print('Số điện thoại không hợp lệ')
        return False

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: rgb(15,250,114);
            background: linear-gradient(67deg, rgba(15,250,114,1) 0%, rgba(0,255,255,1) 77%);
        }
        .main {
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .box_main {
            height: 200px;
            width: 400px;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
        .inputPhoneNumber {
            padding-top: 10px;
            width: 100%;
            height: 40%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        input {
            width: 350px;
            height: 50px;
            border: none;
            border-bottom: 2px solid black;
            padding-bottom: 0px;
            line-height: 1px;
            font-size: 25px;
            text-align: center;
        }
        input:focus {
            border-bottom: 2px solid #007bff;
            outline: none;
            padding-bottom: 0px;
        }
        .box_bottom {
            width: 100%;
            height: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 35px; 
        }
        button {
            width: 300px;
            height: 50px;
            background: rgb(15,250,114);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 30px;
            font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            margin: 0 auto;
            display: block;
            text-align: center;
        }
        button:hover {
            background-color: aqua;
        }
    </style>
    <title>Document</title>
</head>
<body>
    <div class="main">
        <div class="box_main">
            <form action="/" method="post">
                <div class="inputPhoneNumber">
                    <input type="text" name="phoneNumber" value="" placeholder="Nhập số điện thoại của bạn">
                </div>
                <div class="box_bottom">
                    <div class="send">
                        <button type="submit">
                            SEND
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
'''

verify_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: rgb(15,250,114);
            background: linear-gradient(67deg, rgba(15,250,114,1) 0%, rgba(0,255,255,1) 77%);
        }
        .main {
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .box_main {
            height: 200px;
            width: 400px;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
        .inputPhoneNumber {
            padding-top: 10px;
            width: 100%;
            height: 40%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        input {
            width: 350px;
            height: 50px;
            border: none;
            border-bottom: 2px solid black;
            padding-bottom: 0px;
            line-height: 1px;
            font-size: 25px;
            text-align: center;
        }
        input:focus {
            border-bottom: 2px solid #007bff;
            outline: none;
            padding-bottom: 0px;
        }
        .box_bottom {
            width: 100%;
            height: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 35px; /* Điều chỉnh khoảng cách giữa input và nút VERIFY */
        }
        button {
            width: 300px;
            height: 50px;
            background: rgb(15,250,114);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 30px;
            font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            margin: 0 auto;
            display: block;
            text-align: center;
        }
        button:hover {
            background-color: aqua;
        }
    </style>
    <title>Verify OTP</title>
</head>
<body>
    <div class="main">
        <div class="box_main">
            <form action="/verify" method="post">
                <div class="inputPhoneNumber">
                    <input type="text" name="otp" value="" placeholder="Nhập mã OTP">
                </div>
                <div class="box_bottom">
                    <div class="send">
                        <button type="submit">
                            VERIFY
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number_input = request.form.get('phoneNumber')
        if phone_number_input != my_phone_number:
            return '''
                <div style="text-align: center; color: red; font-size: 24px">
                    <p>Số điện thoại không hợp lệ!</p>
                </div>
            '''
        otp = generate_otp()
        if send_otp(phone_number_input, otp):
            session['otp'] = otp
            session['phoneNumber'] = phone_number_input  # Store the phone number in the session
            return render_template_string(verify_template)
        else:
            return 'Không thể gửi OTP vì số điện thoại không hợp lệ.'
    return render_template_string(html_template)

@app.route('/verify', methods=['POST'])
def verify_otp():
    otp_input = request.form.get('otp')
    if 'otp' in session and otp_input == session['otp']:
        print('Xác thực OTP thành công.')
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .success {
                            color: #0f0;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <p class="success">Xác thực OTP thành công!</p>
                    </div>
                </body>
            </html>
        ''')
    else:
        print('Mã OTP không hợp lệ, xác thực thất bại.')
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .error {
                            color: #f00;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container"> 
                        <p class="error">Mã OTP không hợp lệ, xác thực thất bại!</p> 
                    </div
                    </div> 
                </body> 
            </html>
        ''')

if __name__ == '__main__':
    app.run(debug=True)
