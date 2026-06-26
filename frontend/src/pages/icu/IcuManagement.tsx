import React, { useEffect, useState } from "react";

import { Pencil, Trash2 } from "lucide-react";
import { addICU, getICU, updateICU } from "../../Service/adminService";
import DeleteConfirmPopup from "./DeleteConfirmationPopup";
import CommonTable from "../../shared/table";

//import { useSnackbar } from "@/hooks/use-snackbar";

interface ICUData {
  id: number;
  icu_name: string;
  type: string;
  department: string;
  beds: number;
  devices: number;
  gateway: string;
  status: string;
}

const IcuManagement = () => {
  const [open, setOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);

  const [openDelete, setOpenDelete] = useState(false);
  const [selectedId, setSelectedId] = useState<number>(0);

  const [data, setData] = useState<ICUData[]>([]);
  //const snackbar = useSnackbar();

  const [form, setForm] = useState({
    id: 0,
    icu_name: "",
    type: "",
    department: "",
    beds: "",
    devices: "",
    gateway: "",
    status: "",
  });

  useEffect(() => {
    loadICU();
  }, []);

  const loadICU = async () => {
    try {
      const response = await getICU();
      setData(response);
    } catch (error: any) {
      const message =
        error.response?.data?.message || "Something went wrong";
      //snackbar.error(message);
    }
  };


  const columns = [
    { title: "ICU Name", dataIndex: "icu_name", key: "icu_name" },
    { title: "Type", dataIndex: "type", key: "type" },
    { title: "Department", dataIndex: "department", key: "department" },
    { title: "Beds", dataIndex: "beds", key: "beds" },
    { title: "Devices", dataIndex: "devices", key: "devices" },
    { title: "Gateway", dataIndex: "gateway", key: "gateway" },
    { title: "Status", dataIndex: "status", key: "status" },
  ];


  const handleSubmit = async () => {
    try {
      if (isEdit) {
        const response = await updateICU(form.id, form);

        //snackbar.success("ICU Updated Successfully");

        setData((prev) =>
          prev.map((item) =>
            item.id === form.id ? response : item
          )
        );

      } else {

        const response = await addICU(form);

        //snackbar.success("ICU Added Successfully");

        setData((prev) => [...prev, response]);
      }

      setOpen(false);

      setForm({
        id: 0,
        icu_name: "",
        type: "",
        department: "",
        beds: "",
        devices: "",
        gateway: "",
        status: "",
      });

      setIsEdit(false);

    } catch (error:any) {

      const message =
        error.response?.data?.message || "Something went wrong";

      //snackbar.error(message);
    }
  };


  const handleAdd = () => {
    setIsEdit(false);

    setForm({
      id: 0,
      icu_name: "",
      type: "",
      department: "",
      beds: "",
      devices: "",
      gateway: "",
      status: "",
    });

    setOpen(true);
  };


  const handleEdit = (row: ICUData) => {

    setIsEdit(true);

    setForm({
      id: row.id,
      icu_name: row.icu_name,
      type: row.type,
      department: row.department,
      beds: row.beds.toString(),
      devices: row.devices.toString(),
      gateway: row.gateway,
      status: row.status,
    });

    setOpen(true);
  };


  const handleDeleteClick = (id:number) => {
    setSelectedId(id);
    setOpenDelete(true);
  };


  return (

  

      <div style={{ padding:20 }}> {/* tailwind: p-5 */}


        {/* Header */}

        <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:16 }}> {/* tailwind: flex justify-between items-center mb-4 */}

          <h2 style={{ fontSize:20, fontWeight:600 }}> {/* tailwind: text-xl font-semibold */}
            ICU Management
          </h2>


          <button
            onClick={handleAdd}
            style={{
              backgroundColor:"#2563eb",
              color:"#fff",
              padding:"8px 16px",
              borderRadius:4
            }} /* tailwind: bg-blue-600 text-white px-4 py-2 rounded */
          >
            Add ICU Unit
          </button>

        </div>


        {/* Table */}

        <CommonTable
          columns={columns}
          data={data}
          renderActions={(row:ICUData)=>(

            <div style={{ display:"flex", gap:12, alignItems:"center" }}> {/* tailwind: flex gap-3 items-center */}


              <Pencil
                size={18}
                onClick={()=>handleEdit(row)}
                style={{
                  cursor:"pointer",
                  color:"#2563eb"
                }} 
                /* tailwind: cursor-pointer text-blue-600 hover:text-blue-800 */
              />


              <Trash2
                size={18}
                onClick={()=>handleDeleteClick(row.id)}
                style={{
                  cursor:"pointer",
                  color:"#dc2626"
                }}
                /* tailwind: cursor-pointer text-red-600 hover:text-red-800 */
              />

            </div>

          )}
        />


        <DeleteConfirmPopup
          open={openDelete}
          id={selectedId}
          module="icu-units"
          message="Are you sure you want to delete this ICU?"
          onClose={()=>setOpenDelete(false)}
          onSuccess={loadICU}
        />



        {open && (

          <div style={{
            position:"fixed",
            inset:0,
            backgroundColor:"rgba(0,0,0,0.4)",
            display:"flex",
            justifyContent:"center",
            alignItems:"center"
          }}> {/* tailwind: fixed inset-0 bg-black/40 flex justify-center items-center */}


            <div style={{
              background:"#fff",
              padding:24,
              borderRadius:4,
              width:384
            }}> {/* tailwind: bg-white p-6 rounded w-96 */}



              <h2 style={{
                fontSize:18,
                fontWeight:700,
                marginBottom:16
              }}> {/* tailwind: text-lg font-bold mb-4 */}

                {isEdit ? "Update ICU":"Add ICU"}

              </h2>


              {[
                "icu_name",
                "type",
                "department",
                "beds",
                "devices",
                "gateway",
                "status",
              ].map((field)=>(

                <input
                  key={field}
                  type={
                    field==="beds" || field==="devices"
                      ?"number"
                      :"text"
                  }
                  placeholder={field}
                  value={(form as any)[field]}
                  style={{
                    width:"100%",
                    border:"1px solid #ddd",
                    padding:8,
                    marginBottom:12
                  }} 
                  /* tailwind: w-full border p-2 mb-3 */
                  onChange={(e)=>
                    setForm({
                      ...form,
                      [field]:e.target.value,
                    })
                  }
                />

              ))}



              <div style={{
                display:"flex",
                justifyContent:"flex-end",
                gap:8
              }}> {/* tailwind: flex justify-end gap-2 */}


                <button
                  onClick={()=>setOpen(false)}
                  style={{
                    padding:"8px 16px",
                    border:"1px solid #ddd",
                    borderRadius:4
                  }}
                > {/* tailwind: px-4 py-2 border rounded */}

                  Cancel

                </button>


                <button
                  onClick={handleSubmit}
                  style={{
                    padding:"8px 16px",
                    background:"#2563eb",
                    color:"#fff",
                    borderRadius:4
                  }}
                > {/* tailwind: px-4 py-2 bg-blue-600 text-white rounded */}

                  {isEdit ? "Update":"Add"}

                </button>


              </div>

            </div>

          </div>

        )}

      </div>

  

  );
};


export default IcuManagement;