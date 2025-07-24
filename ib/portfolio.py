from connection import with_ib_connection

@with_ib_connection
async def get_portfolio(ib):
    positions = ib.positions()
    if not positions:
        return "Portfolio is empty"

    res = ""
    for pos in positions:
        res += f"{pos.account}: {pos.contract.symbol} {pos.position} @ avg {pos.avgCost}\n"

    return res