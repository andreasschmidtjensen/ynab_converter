# YNAB Converter

A simple tool I use to convert my bank statements (Lån & Spar Bank in Denmark) to the format used by You Need A Budget.

## Usage

    # Load the CSV file
    records = load_lsb_csv(<load location>)
    # save to new file in proper format
    to_ynab_file(records, <save location>)
