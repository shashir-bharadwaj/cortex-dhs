import { getPatients } from "./patientApi";
import { BedOverview } from "../types/dashboard";
import { buildBedOverview } from "../utils/dashboard";

export async function getBedOverview(): Promise<BedOverview[]> {
  const patients = await getPatients();
  return buildBedOverview(patients, 10);
}