
export default function Holding({asset, amount, currentPrice})
{
    const currentvalue = amount * currentPrice;
    return(
    <div>
        <h3>
            {asset.toUpperCase()}
        </h3>
        <p>Amount: {amount}</p>
        <p>Value: {currentvalue}$</p>
    </div>
    )
}