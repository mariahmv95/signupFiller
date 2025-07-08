import os
import sys
from playwright.sync_api import sync_playwright
import csv

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Navigate to the signup page for each user
            page.goto("https://demo.guru99.com/test/newtours/register.php")

            # username as email
            username = row['email'].split('@')[0]
            if username[-1].isdigit():
                username = username[:-1]


            # Fill out the signup page
            page.locator('input[name="firstName"]').type(row['first_name'], delay=100)
            page.locator('input[name="lastName"]').type(row['last_name'], delay=100)
            page.locator('input[name="phone"]').type(row['phone'], delay=100)
            page.locator('input[name="userName"]').type(row['email'], delay=100)
            page.locator('input[name="address1"]').type(row['address'], delay=100)
            page.locator('input[name="city"]').type(row['city'], delay=100)
            page.locator('input[name="state"]').type(row['state'],delay=100)
            page.locator('input[name="postalCode"]').type("12345", delay=100)
            page.select_option('select[name="country"]', 'UNITED STATES')

            page.locator('input[name="email"]').type(username, delay=100)
            page.locator('input[name="password"]').type(row['password'], delay=100)
            page.locator('input[name="confirmPassword"]').type(row['password'], delay=100)

            # check for checkbox
            accept_checkbox = page.locator('input[name="acceptTerms"]')
            if accept_checkbox.is_visible():
                accept_checkbox.check()
            else:
                print("Checkbox not found")

            # Submit the form
            page.locator('input[name="submit"]').click()



            # check for successful execution
            success_locator = page.locator(f"text=/Note: Your user name is {username}/")
            if success_locator.is_visible():
                print(f"Successfully registered {username}")
            else:
                print(f"Failed to register {username}")

            page.wait_for_timeout(2000) # Wait for 2 seconds to see the result

    # Close browser
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
