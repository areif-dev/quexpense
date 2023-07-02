#!/usr/bin/python

from argparse import ArgumentParser, ArgumentError
import os
from datetime import datetime


def setup_args() -> ArgumentParser:
    """ Establish the command line args that Quexpense expects """

    parser = ArgumentParser(
        prog="quexpense",
        description="Quickly add expenses to a Plain Text Accounting ledger",
    )
    parser.add_argument(
        "-f", "--file", help="The journal file to write the new expense to. If none is provided, then default to using $LEDGER_FILE"
    )
    parser.add_argument(
        "description",
        type=str,
        help="The description for this transaction that should appear in the first" \
        "line right after the date"
    )
    parser.add_argument(
        "expense_account",
        type=str,
        help="The expense subaccount that this transaction should count against. \
        For example, if a transaction is for a gas expense, the command might be \
        `quexpense gas liabilities:discover:credit 45.00`. Omit the 'expense' top level account"
    )
    parser.add_argument(
        "paying_account",
        type=str,
        help="The account to draw funds from to pay for the expense. For example, \
        if a transaction to pay for gas is to be paid on a credit card, then the \
        command might be `quexpense gas liabilities:discover:credit 45.00`"
    )
    parser.add_argument(
        "value",
        type=float,
        help="The amount of money to draw from the paying_account and send to \
        expense account. Should be a number like 45.00 or 10. Omit '$' or other \
        currency denotation."
    )
    args = parser.parse_args()
    return args


def main():
    args = setup_args()

    journal_file = args.file
    if journal_file is None:
        journal_file = os.environ.get("LEDGER_FILE")

        if journal_file is None:
            print("quexpense: error: No journal file specified. Please specify -f /path/to/ledger.journal or define $LEDGER_FILE")
            return 1

    with open(journal_file, "a") as f:
        time = datetime.now().strftime("%Y-%m-%d")
        f.write(f"\n\n{time} {args.description}\n")
        f.write("  expenses:%s  $%.2f\n" % (args.expense_account, args.value))
        f.write("  %s  $-%.2f\n" % (args.paying_account, args.value))
        f.write("  [assets:budget:spendable]  $%.2f\n" % (args.value))
        f.write("  [assets:budget:%s]  $-%.2f" % (args.expense_account, args.value))


if __name__ == "__main__":
    main()
