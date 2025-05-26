from email_utils import send_email_with_csv

from scraper import scrap_zap_state

state = "sc"
types = ["galpao-deposito-armazem"]
exit_file = "imoveis_comerciais.csv"

scrap_zap_state(types, state, area_min=50, area_max=1000)

send_email_with_csv(exit_file)
