# Quexspence

Python script to quickly add expenses to a Plain Text Accounting journal file.

This script uses balanced virtual posts to implement a form of envelope budgeting. The expense account specified in the command line will not only add a posting to expenses:{acct}, but it will also create a virtual posting to [assets:budget:{acct}] in a negative value. In order to balance the transaction, a positive amount will be posted virtually to [assets:budget:spendable] for the same amount.

## usage: quexpense [-h] [-f FILE] description expense_account paying_account value

## positional arguments:

  - description           The description for this transaction that should appear in the firstline right after the date
  - expense_account       The expense subaccount that this transaction should count against. For example, if a transaction is for a gas
                        expense, the command might be `quexpense gas liabilities:discover:credit 45.00`. Omit the 'expense' top level
                        account
  - paying_account        The account to draw funds from to pay for the expense. For example, if a transaction to pay for gas is to be paid
                        on a credit card, then the command might be `quexpense gas liabilities:discover:credit 45.00`
  - value                 The amount of money to draw from the paying_account and send to expense account. Should be a number like 45.00 or
                        10. Omit '$' or other currency denotation.

## options:
 - -h, --help            show this help message and exit
 - -f FILE, --file FILE  The journal file to write the new expense to. If none is provided, then default to using $LEDGER_FILE

## Example

```bash
quexpense -f ledger.journal "This is a test transaction" misc liabilities:bank:credit 45
```

This will create a transaction that looks like this in ledger.journal

```
2023-06-12 This is a test transaction
    expenses:misc     $45.00
    liabilities:bank:credit     $-45.00
    [assets:budget:spendable]     $45.00
    [assets:budget:misc]      $-45.00
```
