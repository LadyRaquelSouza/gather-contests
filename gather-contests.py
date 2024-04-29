import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import re

url = "https://concursos-literarios.blogspot.com/p/inscricoes-abertas.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", href=lambda href: href and "concursos-literarios.blogspot.com" in href)

cal = Calendar()
cal.add('prodid', '-//My calendar//example.com//')
cal.add('version', '2.0')

date_regex = r'\b(\d{2}\.\d{2}\.\d{4})\b'

for link in links:
    link_text = link.text.strip()
    link_url = link['href']

    if re.search(date_regex, link_text):
        match = re.search(date_regex, link_text)
        date = match.group(1)
        title = link_text.replace(match.group(0), "").strip()

        date_obj = datetime.strptime(date, "%d.%m.%Y")

        event = Event()
        event.add('summary', title)
        event.add('dtstart', date_obj)
        event.add('dtend', date_obj)  # Evento de um dia
        cal.add_component(event)

with open('concursos_literarios.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Calendário gerado com sucesso!")
