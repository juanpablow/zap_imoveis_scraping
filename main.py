from email_utils import send_email_with_csv
from format_columns import format_columns
from scraper import scrape_zap_state

states = ["sc", "rs"]
types = ["galpao-deposito-armazem"]
exit_file = "imoveis_comerciais.xlsx"


for state in states:
    scrape_zap_state(types, state, area_min=50, area_max=1000)

format_columns(exit_file)

send_email_with_csv(exit_file)
