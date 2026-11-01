from playwright.sync_api import sync_playwright, Response
import json

def intercept_compensation_data():
    intercepted_data = []

    def handle_response(response: Response):
        if "api/compensation/get_district_claims" in response.url and response.status == 200:
            print(f"📡 Intercepted hidden API payload from: {response.url}")
            try:
                raw_json = response.json()
                intercepted_data.append(raw_json)
            except Exception as e:
                print(f"Failed to parse JSON: {e}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.on("response", handle_response)

        print("Navigating to State Forest Compensation Portal...")
        page.goto("https://keralaforest.gov.in/compensation_portal_example", wait_until="networkidle")

        try:
            print("Selecting District: Wayanad...")
            page.select_option('select#district_dropdown', value='WAYANAD')
            page.click('button#fetch_records')
            
            page.wait_for_response(lambda r: "api/compensation" in r.url)
            
        except Exception as e:
            print(f"UI Interaction failed, portal might be down: {e}")

        browser.close()

    if intercepted_data:
        print("\n✅ Successfully extracted backend data without parsing HTML!")
        print(json.dumps(intercepted_data[0][:2], indent=2))
    else:
        print("\n❌ Failed to intercept data.")

if __name__ == "__main__":
    intercept_compensation_data()