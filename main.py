from bs4 import BeautifulSoup
import smtplib
import requests

email = 'INSERT EMAIL'
password = 'INSERT PASSWORD'
provider = 'INSERT PROVIDER'
tracked_items = {
    "https://www.amazon.ca/Logitech-G935-Wireless-DTS-LIGHTSYNC/dp/B07MP4HT95": 190,
    'https://www.amazon.ca/Unbroken-World-Survival-Resilience-Redemption/dp/0812974492': 12,
    'https://www.amazon.ca/1984-George-Orwell/dp/0451524934': 9.18,
}

header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/104.0.5112.102 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.8',
}

for item_link, max_price in tracked_items.items():
    response = requests.get(item_link, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    current_price = soup.find(name="span", class_="a-offscreen")
    product_name = soup.find("span", attrs={"id": 'productTitle'}).get_text().strip()
    current_price = float(current_price.get_text().replace('$', ''))
    if max_price >= current_price:
        with smtplib.SMTP(provider, 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email,
                                msg=f'Subject:{product_name} Available for ${current_price}\n\n'
                                    f'The price of {product_name} has reached the minimum recorded threshold of '
                                    f'${max_price} and is currently only ${current_price}. Buy Now!')
