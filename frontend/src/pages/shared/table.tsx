import React, { useMemo, useState } from "react";

type Column = {
  key: string;
  title: string;
  dataIndex: string;
};

type CommonTableProps = {
  columns: Column[];
  data: Record<string, any>[];
  renderActions?: (row: Record<string, any>) => React.ReactNode;
  rowsPerPage?: number;
};

const CommonTable = ({
  columns,
  data,
  renderActions,
  rowsPerPage = 5,
}: CommonTableProps) => {
  const [search, setSearch] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [sortConfig, setSortConfig] = useState<{
    key: string;
    direction: "asc" | "desc";
  } | null>(null);

  const getStatusStyle = (status: string) => {
    if (status === "Active") {
      return "bg-green-100 text-green-700 px-2 py-1 rounded text-xs";
    }
    if (status === "Maintenance") {
      return "bg-orange-100 text-orange-600 px-2 py-1 rounded text-xs";
    }
    return "";
  };

  const handleSort = (key: string) => {
    let direction: "asc" | "desc" = "asc";

    if (sortConfig && sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    setSortConfig({ key, direction });
  };

  const filteredData = useMemo(() => {
    return data.filter((row) =>
      columns.some((col) =>
        String(row[col.dataIndex])
          .toLowerCase()
          .includes(search.toLowerCase())
      )
    );
  }, [search, data, columns]);

  const sortedData = useMemo(() => {
    if (!sortConfig) return filteredData;

    const sorted = [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
      return 0;
    });

    return sorted;
  }, [filteredData, sortConfig]);

  const totalPages = Math.ceil(sortedData.length / rowsPerPage);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * rowsPerPage;
    return sortedData.slice(start, start + rowsPerPage);
  }, [sortedData, currentPage, rowsPerPage]);

  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        borderRadius: 8,
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
        border: "1px solid #e5e7eb",
        padding: 16,
      }}
    >
      {/* tailwind: bg-white rounded-lg shadow border p-4 */}
      <div
        style={{
          marginBottom: 16,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {/* tailwind: mb-4 flex justify-between items-center */}
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setCurrentPage(1);
          }}
          style={{
            border: "1px solid #d1d5db",
            padding: "8px 12px",
            borderRadius: 6,
            width: 256,
            fontSize: 14,
          }}
        />
        {/* tailwind: border px-3 py-2 rounded w-64 text-sm */}
      </div>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        {/* tailwind: w-full border-collapse */}
        <thead
          style={{
            backgroundColor: "#f9fafb",
            color: "#4b5563",
            fontSize: 14,
          }}
        >
          {/* tailwind: bg-gray-50 text-gray-600 text-sm */}
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                onClick={() => handleSort(col.dataIndex)}
                style={{
                  textAlign: "left",
                  padding: "12px 16px",
                  fontWeight: 500,
                  borderBottom: "1px solid #e5e7eb",
                  cursor: "pointer",
                  userSelect: "none",
                }}
              >
                {/* tailwind: text-left px-4 py-3 font-medium border-b cursor-pointer select-none */}
                {col.title}
                {sortConfig?.key === col.dataIndex && (
                  <span style={{ marginLeft: 8 }}>
                    {sortConfig.direction === "asc" ? "↑" : "↓"}
                  </span>
                )}
              </th>
            ))}
            <th
              style={{
                textAlign: "left",
                padding: "12px 16px",
                fontWeight: 500,
                borderBottom: "1px solid #e5e7eb",
              }}
            >
              Actions
            </th>
          </tr>
        </thead>

        <tbody style={{ fontSize: 14, color: "#374151" }}>
          {/* tailwind: text-sm text-gray-700 */}
          {paginatedData.length > 0 ? (
            paginatedData.map((row, index) => (
              <tr
                key={index}
                style={{
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                {/* tailwind: border-b hover:bg-gray-50 transition */}
                {columns.map((col) => (
                  <td key={col.key} style={{ padding: "12px 16px" }}>
                    {col.key === "status" ? (
                      <span
                        style={{
                          backgroundColor:
                            row[col.dataIndex] === "Active"
                              ? "#dcfce7"
                              : row[col.dataIndex] === "Maintenance"
                              ? "#ffedd5"
                              : "",
                          color:
                            row[col.dataIndex] === "Active"
                              ? "#15803d"
                              : row[col.dataIndex] === "Maintenance"
                              ? "#c2410c"
                              : "",
                          padding: "4px 8px",
                          borderRadius: 4,
                          fontSize: 12,
                        }}
                      >
                        {row[col.dataIndex]}
                      </span>
                    ) : (
                      row[col.dataIndex]
                    )}
                  </td>
                ))}

                <td style={{ padding: "12px 16px" }}>
                  {renderActions && renderActions(row)}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length + 1} style={{ textAlign: "center", padding: "16px 0" }}>
                No data found
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginTop: 16,
          fontSize: 14,
        }}
      >
        {/* tailwind: flex justify-between items-center mt-4 text-sm */}
        <span>
          Page {currentPage} of {totalPages || 1}
        </span>

        <div style={{ display: "flex", gap: 8 }}>
          {/* tailwind: flex gap-2 */}
          <button
            style={{
              padding: "6px 12px",
              border: "1px solid #d1d5db",
              borderRadius: 6,
              opacity: currentPage === 1 ? 0.5 : 1,
            }}
            onClick={() => setCurrentPage((p) => p - 1)}
            disabled={currentPage === 1}
          >
            {/* tailwind: px-3 py-1 border rounded disabled:opacity-50 */}
            Prev
          </button>

          <button
            style={{
              padding: "6px 12px",
              border: "1px solid #d1d5db",
              borderRadius: 6,
              opacity: currentPage === totalPages || totalPages === 0 ? 0.5 : 1,
            }}
            onClick={() => setCurrentPage((p) => p + 1)}
            disabled={currentPage === totalPages || totalPages === 0}
          >
            {/* tailwind: px-3 py-1 border rounded disabled:opacity-50 */}
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default CommonTable;
