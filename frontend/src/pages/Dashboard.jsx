import { useState } from "react";
import Portfolio from "../components/crypto/Portfolio";
import CryptoSearch from "../components/crypto/CryptoSearch";


export function Dashboard()
{
    const [holdings, setHolding] = useState([])
    
        function AddHolding({asset,amount,price,symbol})
        {
            const amt = Number(amount);
            const prc = Number(price);
            setHolding(prev => {
                const existing = prev.find(h => h.asset === asset)
                if (!existing)
                {
                return [...prev, {asset: asset, symbol: symbol, amount: amt, price:prc}]
                }
                
                const newamount = existing.amount + amt;
            
                return prev.map(h => 
                h.asset === asset
                ? {...h, amount: newamount}
                : h
                );
            });
        }
        function DeleteHolding({asset})
        {
            setHolding(prev => prev.filter(h => h.asset !== asset))
        }

      return (
        <div style={{ display: "flex", height: "100vh" }}>
          <div style={{ flex: 1, overflow: "auto", borderRight: "1px solid #ddd" }}>
            <CryptoSearch onAddHolding={AddHolding}/>
          </div>
          <div style={{ width: "400px", overflow: "auto" }}>
            <Portfolio holdings={holdings} onDelete={DeleteHolding}/>
          </div>
        </div>
      );
}