import { Phone, Calendar, Users, BarChart3 } from "lucide-react";

const statItems = [
    {
        key: "totalCalls",
        label: "Total Calls Made",
        icon: Phone,
        iconColor: "text-blue-600",
        bgColor: "bg-blue-100",
    },
    {
        key: "appointmentsBooked",
        label: "Appointments Booked",
        icon: Calendar,
        iconColor: "text-green-600",
        bgColor: "bg-green-100",
    },
    {
        key: "conversionRate",
        label: "Conversion Rate",
        icon: BarChart3,
        iconColor: "text-purple-600",
        bgColor: "bg-purple-100",
        suffix: "%",
    },
    {
        key: "activeCampaigns",
        label: "Active Campaigns",
        icon: Users,
        iconColor: "text-orange-600",
        bgColor: "bg-orange-100",
    },
];

export default function StatsCards({ stats }) {
    return (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-6 lg:mb-8">
            {statItems.map((item) => (
                <div key={item.key} className="bg-white p-4 lg:p-6 rounded-xl border border-[#EAECF0]">
                    <div className="flex items-center justify-between mb-3 lg:mb-4">
                        <div className={`w-10 h-10 lg:w-12 lg:h-12 ${item.bgColor} rounded-lg flex items-center justify-center`}>
                            <item.icon size={20} className={`${item.iconColor} lg:w-6 lg:h-6`} />
                        </div>
                    </div>
                    <div className="text-xl lg:text-2xl font-semibold text-[#101828] mb-1">
                        {stats[item.key]}
                        {item.suffix}
                    </div>
                    <div className="text-xs lg:text-sm text-[#667085]">
                        {item.label}
                    </div>
                </div>
            ))}
        </div>
    );
}
