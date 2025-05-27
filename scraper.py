from urllib.parse import urlencode

import pandas as pd
from playwright.sync_api import sync_playwright


def build_url(type_slug, state, page, area_min, area_max):
    base_url = f"https://www.zapimoveis.com.br/aluguel/{type_slug}/{state}/"
    params = {
        "transacao": "aluguel",
        # "onde": f",{state},,,,,,,state,BR>{state},,,",
        "tipos": type_slug.replace("-", "_"),
        "pagina": page,
        "areaMinima": area_min,
        "areaMaxima": area_max,
        "ordem": "Mais recente",
    }
    return f"{base_url}?{urlencode(params)}"


def scrape_zap_state(types, state, area_min=50, area_max=1000):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        for type in types:
            current_page = 1
            while True:
                url = build_url(type, state, current_page, area_min, area_max)
                print(f"[{state.upper()} - {type}] Página {current_page} -> {url}")

                page.goto(url)
                try:
                    page.wait_for_selector(
                        "li[data-cy='rp-property-cd']", timeout=15000
                    )
                    page.wait_for_timeout(1200)

                except:
                    print("Nenhum resultado encontrado ou fim das páginas.")
                    break

                items = page.query_selector_all("li[data-cy='rp-property-cd']")
                if not items:
                    break

                for item in items:
                    try:
                        title = item.query_selector("h2")
                        address = item.query_selector(
                            "p[data-cy='rp-cardProperty-street-txt']"
                        )
                        area = item.query_selector(
                            "li[data-cy='rp-cardProperty-propertyArea-txt']"
                        )
                        price = item.query_selector(
                            "div[data-cy='rp-cardProperty-price-txt']"
                        )
                        link = item.query_selector("a")

                        # writer.writerow(
                        #     [
                        #         state.upper(),
                        #         type,
                        #         title.inner_text().strip() if title else "",
                        #         address.inner_text().strip() if address else "",
                        #         area.inner_text().strip() if area else "",
                        #         price.inner_text().strip() if price else "",
                        #         link.get_attribute("href") if link else "",
                        #     ]
                        # )

                        title_text = (
                            title.evaluate("node => node.textContent").strip()
                            if title
                            else ""
                        )
                        address_text = (
                            address.evaluate("node => node.textContent").strip()
                            if address
                            else ""
                        )
                        area_text = (
                            area.evaluate("node => node.textContent").strip()
                            if area
                            else ""
                        )
                        price_text = (
                            price.evaluate("node => node.textContent").strip()
                            if price
                            else ""
                        )
                        link_href = link.get_attribute("href") if link else ""

                        results.append(
                            [
                                state.upper(),
                                # type,
                                title_text,
                                address_text,
                                area_text,
                                price_text,
                                link_href,
                            ]
                        )

                    except Exception as e:
                        print("Erro ao processar item:", e)

                current_page += 1

        browser.close()

    df = pd.DataFrame(
        results,
        columns=["Estado", "Título", "Endereço", "Área", "Preço", "Link"],
    )

    return df
    # df.to_excel("imoveis_comerciais.xlsx", index=False)


if __name__ == "__main__":
    types = ["galpao-deposito-armazem"]
    scrape_zap_state(types)
