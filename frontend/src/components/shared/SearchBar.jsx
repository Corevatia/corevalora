export const SearchBar = ({ value, onChange, onKeyDown }) => {
  return (
    <input
      type="search"
      minLength={1}
      maxLength={50}
      autoComplete="off"
      autoFocus
      placeholder="Search...."
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
    />
  );
};
