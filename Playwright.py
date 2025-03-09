from playwright.sync_api import sync_playwright
import csv



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # firefox webkit chromium | True = no GUI اجرای مرورگر به‌صورت گرافیکی
    page = browser.new_page()
    page.goto("https://arbabacamp.com/register/", timeout=100000, wait_until='load') # load ,domcontentloaded ,networkidle

    #page.reload() تعامل با آدرس
    #page.go_back()
    #page.go_forward()


    # مراحل ثبت و نام در سایت
    name = input("Enter your name: ")
    page.fill("input[name='name']",name)
    page.press("button[type='button']", "Enter")

    number = input("Enter phone number:")
    page.fill("input[name='number']", number)
    password = input("Enter password:")
    page.fill("input[name='password']", password)
    page.press("input[type='submit']", "Enter")

    #گرفتن داده از صفحه اصلی سایت
    text = page.inner_text("h1")

    # ریختن آن در یک فایل CSV
    with open("data2.csv", mode="w", newline="", encoding="utf-8") as file:
         writer = csv.writer(file)
         file.write(text)

    # گرفتن عکس از صفحه سایت
    page.screenshot(path="screenshot.png")  # گرفتن اسکرین‌شات از صفحه

    # منتظر ماندن برای دیدن نتایج و بعد خروج
    page.wait_for_timeout(2000)
    browser.close()