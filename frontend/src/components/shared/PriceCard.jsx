import { formatPrice } from "../../lib/format";

export const PriceCard = ({ asset, price, currency = "USD" }) => {
  return (
    <p>
      Asset: {asset} Price: {formatPrice(price, currency)}
    </p>
  );
};
