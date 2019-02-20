import csv
import datetime


READ_IN = 'utf8'
WRITE_OUT = 'utf8'

def load_lsb_csv(path, import_as_new=False):
    result = []
    last_row = None

    with open(path, 'r', encoding=READ_IN) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            date = row[1]
            date = datetime.datetime.strptime(date, "%d-%m-%Y").isoformat()[0:10]

            text = row[2].encode(WRITE_OUT).decode(WRITE_OUT)
            amount = row[3].replace(".", "").replace(",", ".")

            result.append({
                "Date": date,
                "Payee": text,
                "Memo": None,
                "Outflow": amount[1:] if amount[0] == "-" else None,
                "Inflow": amount if amount[0] != "-" else None
            })

            last_row = row

    if import_as_new:
        # This is only needed for the first import of an account - the first entry will be the balance at import
        import_balance = last_row[4]
        amount = import_balance.replace(".", "").replace(",", ".")
        last_record = result[-1]
        result = result[:-1]
        result.append({
            "Date": last_record["Date"],
            "Payee": "Balance at import",
            "Memo": None,
            "Outflow": amount[1:] if amount[0] == "-" else None,
            "Inflow": amount if amount[0] != "-" else None
        })

    return result

def to_ynab_file(records, filename):
    with open(filename, 'w', encoding=WRITE_OUT) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'],
                                delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for record in records:
            writer.writerow(record)


if __name__ == "__main__":
    import os

    directory = "/Users/asj/Downloads/ynab/"
    if not os.path.exists("%synab" % directory):
        os.mkdir("%synab" % directory)
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    for file in files:
        records = load_lsb_csv("%s%s" % (directory, file))
        to_ynab_file(records, "%synab/%s" % (directory, file))
