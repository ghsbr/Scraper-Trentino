import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import re
import json


@dataclass
class Centralina:
  name: str = ''
  biossido_di_azoto: float = 0.0
  ozono: float = 0.0
  polveri_sottili_pm10: float = 0.0
  polveri_sottili_pm2: float = 0.0


def parser(url):
  
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  table = soup.find(id = 'responsivequal')
  table_body = table.find('tbody')

  table_body_rows = table_body.find_all('tr')

  centraline = []

  for row in table_body_rows:

    temp_centralina = Centralina()

    temp_centralina.name = row.find('th').find('a').get_text()

    row_values = []
    row_values.clear()

    row_values_containers = row.find_all('td')

    for container in row_values_containers:

      raw_value = container.get_text()
      corrected_value = re.findall('\d+', raw_value)
      current_row_container_value = 0

      if len(corrected_value) != 0:
        current_row_container_value = float(corrected_value[0])
      else:
        current_row_container_value = 0
    
      row_values.append(current_row_container_value)

  
    temp_centralina.biossido_di_azoto = row_values[0]
    temp_centralina.ozono = row_values[1]
    temp_centralina.polveri_sottili_pm10 = row_values[2]
    temp_centralina.polveri_sottili_pm2 = row_values[3]
    centraline.append(temp_centralina)

  return centraline


def main():
  url ='https://service.prerender.io//https://ambiente.provincia.bz.it/aria/misurazione-attuale-aria.asp'
  data = parser(url)
  with open('data.json', 'w') as f:
    f.write(json.dumps(data ,default=lambda x: x.__dict__, indent=2))


if __name__ == '__main__':
  main()