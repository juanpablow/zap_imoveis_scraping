import csv
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright


def montar_url(base_path, cidade_slug, tipo_slug, state, pagina, area_min, area_max):
    base_url = (
        f"https://www.zapimoveis.com.br/aluguel/{tipo_slug}/{state}/{cidade_slug}/"
    )
    params = {
        "transacao": "aluguel",
        "onde": f",{cidade_slug},Santa Catarina,,,,,city,BR>Santa Catarina>{cidade_slug},,,",
        "tipos": tipo_slug.replace("-", "_"),
        "pagina": pagina,
        "areaMinima": area_min,
        "areaMaxima": area_max,
    }
    return f"{base_url}?{urlencode(params)}"


def scrape_zap_multiplas_cidades(cidades, tipos, area_min=50, area_max=1000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        with open("imoveis_comerciais.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Cidade",
                    "Tipo",
                    "Titulo",
                    "Endereco",
                    "Area",
                    "Preço",
                    "Link",
                ]
            )

            for cidade in cidades:
                for tipo in tipos:
                    pagina = 1
                    while True:
                        url = montar_url(
                            "aluguel", cidade, tipo, pagina, area_min, area_max
                        )
                        print(f"[{cidade} - {tipo}] Página {pagina} -> {url}")

                        page.goto(url)
                        try:
                            page.wait_for_selector(
                                "li[data-cy='rp-property-cd']", timeout=10000
                            )
                        except:
                            print(
                                "  ⚠️  Nenhum resultado encontrado ou fim das páginas."
                            )
                            break

                        items = page.query_selector_all("li[data-cy='rp-property-cd']")
                        if not items:
                            break  # Fim da paginação

                        for item in items:
                            try:
                                titulo = item.query_selector("h2")
                                endereco = item.query_selector(
                                    "p[data-cy='rp-cardProperty-street-txt']"
                                )
                                area = item.query_selector(
                                    "li[data-cy='rp-cardProperty-propertyArea-txt']"
                                )
                                preco = item.query_selector(
                                    "div[data-cy='rp-cardProperty-price-txt']"
                                )
                                link = item.query_selector("a")

                                writer.writerow(
                                    [
                                        cidade,
                                        tipo,
                                        titulo.inner_text().strip() if titulo else "",
                                        endereco.inner_text().strip()
                                        if endereco
                                        else "",
                                        area.inner_text().strip() if area else "",
                                        preco.inner_text().strip() if preco else "",
                                        link.get_attribute("href") if link else "",
                                    ]
                                )
                            except Exception as e:
                                print("Erro ao processar item:", e)

                        pagina += 1

        browser.close()


cidades = ["sc", "palhoca", "blumenau"]
tipos = ["galpao-deposito-armazem"]

scrape_zap_multiplas_cidades(cidades, tipos)
