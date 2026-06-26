import { deleteData } from "../../Service/adminService";

type DeleteConfirmPopupProps = {
  open: boolean;
  id: number;
  module: string;
  message: string;
  onClose: () => void;
  onSuccess?: () => void;
};

const DeleteConfirmPopup = ({
  open,
  id,
  module,
  message,
  onClose,
  onSuccess,
}: DeleteConfirmPopupProps) => {
  // const snackbar = useSnackbar();

  if (!open) return null;

  const handleDelete = async () => {
    try {
      await deleteData(id, module);
      // snackbar.success("Deleted successfully");
      onSuccess?.();
      onClose();
    } catch (error: any) {
      // keep the existing behavior intact
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      {/* tailwind: fixed inset-0 bg-black/40 flex items-center justify-center z-50 */}
      <div
        style={{
          backgroundColor: "#ffffff",
          borderRadius: 8,
          padding: 24,
          width: 320,
          boxShadow: "0 10px 15px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* tailwind: bg-white rounded-lg p-6 w-[320px] shadow-lg */}
        <h2
          style={{
            fontSize: 18,
            fontWeight: 600,
            marginBottom: 12,
          }}
        >
          {/* tailwind: text-lg font-semibold mb-3 */}
          Delete Confirmation
        </h2>

        <p
          style={{
            color: "#4b5563",
            marginBottom: 20,
          }}
        >
          {/* tailwind: text-gray-600 mb-5 */}
          {message}
        </p>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: 12,
          }}
        >
          {/* tailwind: flex justify-end gap-3 */}
          <button
            onClick={onClose}
            style={{
              border: "1px solid #d1d5db",
              padding: "8px 16px",
              borderRadius: 6,
            }}
          >
            {/* tailwind: border px-4 py-2 rounded-md */}
            No
          </button>

          <button
            onClick={handleDelete}
            style={{
              backgroundColor: "#ef4444",
              color: "#ffffff",
              padding: "8px 16px",
              borderRadius: 6,
            }}
          >
            {/* tailwind: bg-red-500 text-white px-4 py-2 rounded-md */}
            Yes
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmPopup;
