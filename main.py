import os
from datetime import datetime

import pandas as pd
import pytz

from email_utils import send_email_with_csv
from format_columns import format_columns
from scraper import scrape_zap_state

states = ["sc", "rs"]
types = [
    "sala_comercial",
    "imovel-comercial_comercial",
    "galpao_comercial",
    "garagem_comercial",
]


is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"

if is_github_actions:
    now = datetime.now(pytz.timezone("America/Sao_Paulo"))
else:
    now = datetime.now()

date_filter = now.strftime("%d/%m/%Y %H:%M")
exit_file = f"imoveis_{now.strftime('%d-%m-%Y_%Hh%M')}.xlsx"

results = []
for state in states:
    df = scrape_zap_state(types, state, area_min=50, area_max=1000)
    results.append(df)

final_df = pd.concat(results, ignore_index=True)

if os.path.exists(exit_file):
    existing_df = pd.read_excel(exit_file)
    combined_df = pd.concat([existing_df, final_df], ignore_index=True)
    final_df = combined_df.drop_duplicates(subset="Link")

final_df.to_excel(exit_file, index=False)
format_columns(exit_file)
send_email_with_csv(exit_file)
