from selenium import webdriver
import json
import csv

class BaseScraper(object):

  def __init__(self, config_file, store_file='scrape.csv'):
    with open(config_file) as f:
      self.config = json.load(f)

    self.url = self.config['url']
    # TODO: specify browser in config
    self.driver = webdriver.Chrome()
    self.driver.get(self.url)
    self.scrape_data = []
    self.store_file = store_file

  def navigate(self):
    # contains steps for getting to page with data on it
    for step in self.config.get('navigate', []):
      self.do_action(step)

  def scrape(self):
    selector = self.config['scrape']['selector']
    links = self.driver.find_elements_by_css_selector(selector)
    field_mappings = self.config['scrape']['field_mappings']
    self.scrape_data += [
      {
        key: link.get_property(value)
        for key, value in field_mappings.items()
      }
      for link in links
    ]
  def store(self):
    csv_columns = self.config['scrape']['field_mappings'].keys()
    with open(self.store_file, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for data in self.scrape_data:
        writer.writerow(data)
  
  def do_action(self, action):
    el = self.driver.find_element_by_css_selector(action['selector'])
    if action['command'] == 'click':
      el.click()
    elif action['command'] == 'type':
      el.send_keys(action['text'])

  def next_page(self):
    for action in self.config.get('next_page', []):
      self.do_action(action)
    
