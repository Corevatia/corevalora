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
      className="text-center text-lg p-1.5 px-3 rounded-md border border-neutral-300 dark:border-neutral-700 bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100"
    />
  );
};
