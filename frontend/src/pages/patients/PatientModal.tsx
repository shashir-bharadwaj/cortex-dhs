import { useState, useEffect } from "react";
import {
    X,
    User,
    CalendarDays,
    Pencil,
    Droplet,
    Stethoscope,
    Phone,
} from "lucide-react";


interface PatientModalProps {
    patient: any;
    onClose: () => void;
}

export default function PatientModal({
    patient,
    onClose
}: PatientModalProps) {


    const [isEdit, setIsEdit] = useState(false);

    const [formData, setFormData] = useState<any>({});

    const [tempData, setTempData] = useState<any>({});

    useEffect(() => {

        if (patient) {

            const data = {

                crNo: `CR-${patient?.id || ""}`,

                name: patient?.name || "",

                contactNumber : patient?.contactNumber || "",

                ipNo: `IP-${patient?.id || ""}`,

                admitDate: patient?.admissionTime || "N/A",

                careUnit: patient?.icuUnit || "MICU",

                bedNo: patient?.bedId || "N/A",

                age: patient?.age || "",

                gender: patient?.gender || "",

                height: patient?.height || "N/A",

                weight: patient?.weight || "N/A",

                blood: patient?.bloodGroup || "N/A",

                comorbidities: patient?.comorbidities || "N/A",

                diagnosis: patient?.diagnosis || "N/A",

                doctor: patient?.doctor || "N/A",

                specialization: "Critical Care",

                status: patient?.status || "NORMAL",

                devices: patient?.devices || [],

                latestVitals: patient?.latestVitals || {}

            };

            setFormData(data);

            setTempData(data);

        }

    }, [patient]);

    const handleChange = (key: string, value: string) => {

        setTempData({
            ...tempData,
            [key]: value
        });

    };

    const handleSave = () => {
        setFormData(tempData);
        setIsEdit(false);
    };
return (
        <div style={styles.overlay}>

            <div style={styles.container}>
                {/* HEADER */}
                <div style={styles.header}>
                    <div>
                        <h2 style={styles.title}>
                            More Info
                        </h2>
                        <p style={styles.subtitle}>
                            {formData.name} - {formData.crNo}
                        </p>
                    </div>
                    <div style={styles.actions}>
                        {!isEdit ? (
                            <button
                                style={styles.editButton}
                                onClick={() => setIsEdit(true)}
                            >
                                <Pencil size={14} />
                                Edit
                            </button>
                        ) : (
                            <button
                                style={styles.saveButton}
                                onClick={handleSave}
                            >
                                Save

                            </button>
                        )}

                        <button
                            style={styles.closeButton}
                            onClick={onClose}
                        >

                            <X size={22} />

                        </button>
                    </div>
                </div>
                <Section
                    icon={<User size={16} />}
                    title="PATIENT IDENTIFICATION"
                >
                    <FieldView label="CR No" value={tempData.crNo} editable={isEdit} onChange={(v: any) => handleChange("crNo", v)} />
                    <FieldView label="Patient Name" value={tempData.name} editable={isEdit} onChange={(v: any) => handleChange("name", v)} />
                    <FieldView label="IP No" value={tempData.ipNo} editable={isEdit} />
                </Section>
                <Section
                    icon={<CalendarDays size={16} />}
                    title="ADMISSION DETAILS"
                >
                    <FieldView label="Admit Date" value={tempData.admitDate} />

                    <FieldView label="Care Unit" value={tempData.careUnit} />

                    <FieldView label="Bed No" value={tempData.bedNo} />

                    <FieldView label="Status" value={tempData.status} />

                </Section>
                <Section
                    icon={<User size={16} />}
                    title="PERSONAL DETAILS"
                >

                    <FieldView label="Age" value={tempData.age} />

                    <FieldView label="Gender" value={tempData.gender} />

                    <FieldView label="Height" value={tempData.height} />

                    <FieldView label="Weight" value={tempData.weight} />

                     <FieldView label="Blood Group" value={tempData.blood} />

                </Section>
                <Section
                    icon={
                        <Phone
                            size={16}
                        />
                    }
                    title="Contact"
                >
                    <FieldView
                        label="Contact Number"
                        value={tempData.contactNumber}
                        editable={false}
                    />
                </Section>
                <Section
                    icon={<Stethoscope size={16} />}
                    title="TREATMENT"
                >
                    <FieldView label="Doctor" value={tempData.doctor} />

                    <FieldView label="Specialization" value={tempData.specialization} />

                    <FieldView label="Diagnosis" value={tempData.diagnosis} />
                </Section>
                {/* <Section
                    icon={<Phone size={16} />}
                    title="DEVICES"
                >

                    {
                        tempData.devices?.length ?

                            tempData.devices.map((d: any, i: number) => (

                                <div key={i} style={styles.device}>

                                    <p style={styles.value}>
                                        {d?.device?.name || d?.deviceType}
                                    </p>


                                    <p style={styles.label}>
                                        Status : {d?.status}
                                    </p>

                                </div>

                            ))

                            :

                            <p>No devices connected</p>

                    }

                </Section> */}
            </div>
        </div>
    )
}





function Section({
    icon,
    title,
    children
}: any) {

    return (

        <div style={styles.section}>


            <div style={styles.sectionTitle}>

                {icon}

                {title}

            </div>



            <div style={styles.grid}>

                {children}

            </div>


        </div>

    )

}





function FieldView({
    label,
    value,
    editable,
    onChange
}: any) {

    return (

        <div>


            <p style={styles.label}>
                {label}
            </p>


            {
                editable ?


                    <input

                        value={value}

                        onChange={(e) => onChange?.(e.target.value)}

                        style={styles.input}

                    />


                    :


                    <p style={styles.value}>
                        {value}
                    </p>

            }


        </div>

    )

}






const styles: any = {


    overlay: {
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        width: "100vw",
        height: "100vh",
        background: "rgba(0,0,0,.45)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 99999
    },


    container: {
        background: "#fff",
        width: "80%",
        maxWidth: "800px",
        height: "85vh",
        overflowY: "auto",
        borderRadius: "16px",
        padding: "24px",
        boxShadow: "0 20px 40px rgba(0,0,0,.3)"
    },


    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid #ddd",
        paddingBottom: "15px"
    },


    title: {
        fontSize: "22px",
        fontWeight: 700
    },


    subtitle: {
        color: "#6b7280"
    },


    actions: {
        display: "flex",
        gap: "10px"
    },


    section: {
        marginTop: "20px",
        border: "1px solid #ddd",
        borderRadius: "12px",
        padding: "18px"
    },


    sectionTitle: {
        display: "flex",
        gap: "8px",
        color: "#00897b",
        fontWeight: 600,
        marginBottom: "20px"
    },


    grid: {
        display: "grid",
        gridTemplateColumns: "repeat(3,1fr)",
        gap: "25px"
    },


    label: {
        fontSize: "14px",
        color: "#6b7280"
    },


    value: {
        fontSize: "16px",
        fontWeight: 600
    },


    input: {
        height: "35px",
        border: "1px solid #ccc",
        borderRadius: "6px",
        padding: "5px"
    },


    editButton: {
        padding: "7px 15px",
        borderRadius: "8px"
    },


    saveButton: {
        padding: "7px 15px",
        background: "#00897b",
        color: "#fff",
        border: "none",
        borderRadius: "8px"
    },


    closeButton: {
        border: "none",
        background: "transparent",
        cursor: "pointer"
    },


    device: {
        border: "1px solid #ddd",
        padding: "12px",
        borderRadius: "10px"
    }


};