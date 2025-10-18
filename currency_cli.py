#!/usr/bin/env python3
\"\"\"currency_cli.py - A simple command-line currency converter using exchangerate.host

Features:
- Convert amount from one currency to another
- Show latest exchange rate for a currency pair
- List supported currency symbols

No API key required. Uses https://exchangerate.host

Usage examples:
  python currency_cli.py convert 100 USD INR
  python currency_cli.py rate USD EUR
  python currency_cli.py symbols
\"\"\"
import argparse
import sys
import requests

API_BASE = "https://api.exchangerate.host"

def get_symbols():
    resp = requests.get(f"{API_BASE}/symbols", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("symbols", {})

def convert(amount, frm, to):
    params = {"from": frm, "to": to, "amount": amount}
    resp = requests.get(f"{API_BASE}/convert", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_rate(frm, to):
    params = {"base": frm, "symbols": to}
    resp = requests.get(f"{API_BASE}/latest", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rate = data.get("rates", {}).get(to)
    return rate

def main(argv=None):
    parser = argparse.ArgumentParser(prog="currency_cli", description="Simple currency converter (exchangerate.host)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_convert = sub.add_parser("convert", help="Convert amount from one currency to another")
    p_convert.add_argument("amount", type=float, help="Amount to convert")
    p_convert.add_argument("from_currency", help="Source currency (e.g. USD)")
    p_convert.add_argument("to_currency", help="Target currency (e.g. INR)")

    p_rate = sub.add_parser("rate", help="Get latest exchange rate for a currency pair")
    p_rate.add_argument("from_currency", help="Base currency (e.g. USD)")
    p_rate.add_argument("to_currency", help="Target currency (e.g. EUR)")

    p_symbols = sub.add_parser("symbols", help="List supported currency symbols")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "symbols":
            symbols = get_symbols()
            for k, v in sorted(symbols.items()):
                print(f"{k}: {v['description']}")
        elif args.cmd == "convert":
            result = convert(args.amount, args.from_currency.upper(), args.to_currency.upper())
            if result.get("success"):
                print(f\"{result['query']['amount']} {result['query']['from']} = {result['result']} {result['query']['to']}\")
                print(f\"Rate: 1 {result['query']['from']} = {result['info']['rate']} {result['query']['to']}\")
                print(f\"Date: {result.get('date')}\")
            else:
                print(\"Conversion failed. Response:\", result)
        elif args.cmd == "rate":
            rate = get_rate(args.from_currency.upper(), args.to_currency.upper())
            if rate is not None:
                print(f\"1 {args.from_currency.upper()} = {rate} {args.to_currency.upper()}\")
            else:
                print(\"Rate not available.\")
    except requests.exceptions.RequestException as e:
        print(\"Network or API error:\", e, file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
