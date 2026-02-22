export const SearchBar = ({ value, onChange, onKeyDown }) => {
  return (
    <input
      type="search"
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
    />
  );
};
