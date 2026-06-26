import DashboardPageAdmin from "./AdminDashboard";
import DashboardPage from "./DashboardPage";


export default function DashboardMain() {
  const userRole = localStorage.getItem("role");
  //const { userRole } = useApp();
  switch (userRole) {
    case "nurse":
      return <DashboardPage />;
    case "admin":
      return <DashboardPageAdmin/>;
    default:
      return <div>No Dashboard Available</div>;
  }
}