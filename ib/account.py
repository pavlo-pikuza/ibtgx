from ib_insync import util

from connection import with_ib_connection

@with_ib_connection
async def get_accounts(ib):
    accounts = ib.managedAccounts()
    return accounts

@with_ib_connection
async def get_account_balance(ib, account):
    summary = await ib.accountSummaryAsync()
    df = util.df(summary)
    fields = ['NetLiquidation', 'BuyingPower', 'AvailableFunds', 'TotalCashValue']
    return df.loc[(df['tag'].isin(fields)) & (df['account'] == account),['tag','value','currency']].reset_index(drop=True)