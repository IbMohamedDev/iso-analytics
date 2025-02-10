import React from "react";

const TableCell = ({ children }) => {
  return (
    <td className="border px-4 py-2 text-center">
      <div className="w-full h-full flex items-center justify-center">{children}</div>
    </td>
  );
};

export default TableCell;