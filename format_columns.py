from openpyxl import load_workbook


def format_columns(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        word_column = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[word_column].width = max_length + 2

    wb.save(excel_file)


if __name__ == "__main__":
    format_columns("imoveis_comerciais.xlsx")
