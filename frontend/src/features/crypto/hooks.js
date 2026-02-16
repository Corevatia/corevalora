import { useEffect, useState } from "react";
import { fetchCryptoPrice } from "./api";

export function useCryptoprice(name)
{
    const [data, setData] = useState(null);
    
    useEffect(() => {
        if(!name) return;

        fetchCryptoPrice(name)
            .then(setData);
  }, [name]);
  return data
}