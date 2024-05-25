# coolsms api
coolsms_api_key = "NCSEN7AT6LZUCWS5"
coolsms_api_secret = "8EGIQNUUSSEX0UGQPSIMLNDKUWT5DQYY"
send_number = "01074606675"
kakao_pfid = 'KA01PF240512130148067WJMMGFPOkKG',
kakao_templateid = 'KA01TP240521102417824tbILzmFvqYF'

# discord invite link
discord_invite = "https://discord.gg/4X4nGN8y5f"

# email html contents, email address
email_address = "codestone7@naver.com"
email_name = "CodeStone"
email_password = "qwe123!A"
email_smtp = "smtp.naver.com"
verification_code = 0
email_html = f"""\
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>CodeStone Email Verify</title>
                <style>
                    body {{ background-color: #333; color: #fff; font-family: Arial, sans-serif; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
                    .outer-box {{ background-color: #333; max-width: 2400px; padding: 160px; border: 1px solid #777; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); }}
                    .verification-box {{ background-color: #555; color: #fff; border: 2px solid #777; padding: 20px; text-align: center; max-width: 500px; margin: auto; border-radius: 30px; }}
                    .verification-code {{ font-size: 24px; letter-spacing: 5px; font-weight: bold; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="outer-box">
                    <div class="verification-box">
                        <h2>이메일 인증</h2>
                        <p>다음 인증 코드를 인증 필드에 입력해주세요.</p>
                        <div class="verification-code">{verification_code}</div> <!-- 인증 코드를 여기에 삽입 -->
                        <p>인증을 요청하지 않았다면, 이 메일을 무시해주세요.</p>
                        <h5>CodeStone 고객지원 +82 10-7460-6675</h5>
                    </div>
                </div>
            </body>
        </html>
        """

# bank_api
bank_api_token = "9INAtVVtp2WcTSvI0wGG"