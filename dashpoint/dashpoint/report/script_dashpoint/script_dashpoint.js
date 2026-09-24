// Copyright (c) 2026, Shenbaga Devi B and contributors
// For license information, please see license.txt

frappe.query_reports["Script Dashpoint"] = {
	filters: [
		{
		 	fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "rider",
            label: "Rider",
            fieldtype: "Link",
            options: "Rider"
		},
	],
};
