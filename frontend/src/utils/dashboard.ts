import { Patient } from "../types/patient";
import { BedOverview } from "../types/dashboard";

export function buildBedOverview(
  patients: Patient[],
  totalBeds: number = 10
): BedOverview[] {
  const bedMap: Record<number, BedOverview> = {};

  patients.forEach((patient) => {
    bedMap[patient.bed_id] = {
      id: patient.bed_id,
      bed_number: `Bed ${patient.bed_id}`,
      status: "occupied",
      patient: {
        id: patient.id,
        first_name: patient.first_name,
        last_name: patient.last_name,
      },
    };
  });

  const beds: BedOverview[] = [];

  for (let i = 1; i <= totalBeds; i++) {
    if (bedMap[i]) {
      beds.push(bedMap[i]);
    } else {
      beds.push({
        id: i,
        bed_number: `Bed ${i}`,
        status: "available",
        patient: null,
      });
    }
  }

  return beds;
}