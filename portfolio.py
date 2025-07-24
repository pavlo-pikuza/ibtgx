from connection import with_ib_connection

@with_ib_connection
async def show_portfolio(ib):
    positions = ib.positions()
    if not positions:
        print("Portfolio is empty")
        return

    for pos in positions:
        print(f"{pos.account}: {pos.contract.symbol} {pos.position} @ avg {pos.avgCost}")