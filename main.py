from datetime import datetime

import pandas as pd

from email_utils import send_email_with_csv
from format_columns import format_columns
from scraper import scrape_zap_state

states = ["sc", "rs"]
types = ["galpao-deposito-armazem"]
exit_file = "imoveis_comerciais.xlsx"

now = datetime.now()
date_filter = now.strftime("%d/%m/%Y")

exit_file = f"imoveis_{date_filter.replace('/', '-')}.xlsx"

results = []

for state in states:
    df = scrape_zap_state(types, state, area_min=50, area_max=1000)

    results.append(df)

final_df = pd.concat(results, ignore_index=True)
final_df.to_excel(exit_file, index=False)

format_columns(exit_file)

send_email_with_csv(exit_file)
