def main():

  from scripts.international_conference_alerts import scrape
  from scripts.dev_events import scrape
  from scripts.hackathon import scrape
  from scripts.e27 import get_events
  from scripts.event_brite import scrape
  from scripts.ten_times import scrape
  data = scrape()

  # Save the body content to a text file
  # with open("html_content.txt", "w", encoding='utf-8') as file:
  #   file.write(str(body_content))

  # print("Body content saved to html_content.txt")


if __name__ == "__main__":
  main()