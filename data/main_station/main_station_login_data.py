# -*- coding: utf-8 -*-

# 测试登录的账号
login_data = {
    "success_phone_data": [[("phone", "15889501911", "123456")], "手机账号密码正确"],
    "success_email_data": [[("email", "623260178@qq.com", "123456")], "邮箱账号密码正确"],
    "fail_data_phone_error": [[("phone", "19983271000", "457888")], "手机号不存在"],
    "fail_data_password_error": [[("phone", "19983271081", "457999")], "手机号正确，密码错误"]
}
