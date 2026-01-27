CPI_ADJUSTMENT_2018_TO_2024 = 1.21
CPI_ADJUSTMENT_2018_TO_2025 = 1.24
CPI_ADJUSTMENT_2020_TO_2024 = 1.14
CPI_ADJUSTMENT_2020_TO_2025 = 1.17

STAT_CAN_TABLES: dict[str, str] = {
    "tuition": "37-10-0003-01",
    "earnings": "37-10-0280-01",
    "debt": "37-10-0036-01",
    "enrollments": "37-10-0011-01",
}

YEARS_TO_KEEP = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

FIELDS = [
    "education",
    "visual_arts",
    "humanities",
    "social_sciences",
    "law",
    "business",
    "physical_sciences",
    "comp_sci",
    "engineering",
    "architecture",
    "agriculture",
    "health",
    "nursing",
    "medicine",
    "dentistry",
    "pharmacy",
    "veterinary",
    "optometry",
    "personal_services",
    "other",
]

ENROLLMENTS_FIELD_MAP = {
    "Education": "education",
    "Visual and performing arts, and communications technologies": "visual_arts",
    "Humanities": "humanities",
    "Social and behavioural sciences and law": "social_sciences",
    "Business, management and public administration": "business",
    "Physical and life sciences and technologies": "physical_sciences",
    "Mathematics, computer and information sciences": "comp_sci",
    "Architecture, engineering and related technologies": "engineering",
    "Agriculture, natural resources and conservation": "agriculture",
    "Health and related fields": "health",
    "Personal, protective and transportation services": "personal_services",
    "Other field of study": "other",
    "Personal improvement and leisure": "other",
    "Unclassified, field of study": "other",
}

TUITION_FIELD_MAP = {
    "Education": "education",
    "Visual and performing arts, and communications technologies": "visual_arts",
    "Humanities": "humanities",
    "Social and behavioural sciences, and legal studies": "social_sciences",
    "Law": "law",
    "Business, management and public administration": "business",
    "Physical and life sciences and technologies": "physical_sciences",
    "Mathematics, computer and information sciences": "comp_sci",
    "Engineering": "engineering",
    "Architecture": "architecture",
    "Agriculture, natural resources and conservation": "agriculture",
    "Dentistry": "dentistry",
    "Medicine": "medicine",
    "Nursing": "nursing",
    "Pharmacy": "pharmacy",
    "Veterinary medicine": "veterinary",
    "Optometry": "optometry",
    "Other health, parks, recreation and fitness": "health",
    "Personal, protective and transportation services": "personal_services",
    "Other, field of study": "other",
}

EARNINGS_FIELD_MAP = {
    "Education": "education",
    "Visual and performing arts, and communications technologies": "visual_arts",
    "Humanities": "humanities",
    "Social and behavioural sciences and law": "social_sciences",
    "Business, management and public administration": "business",
    "Physical and life sciences and technologies": "physical_sciences",
    "Mathematics, computer and information sciences": "comp_sci",
    "Architecture, engineering, and related technologies": "engineering",
    "Agriculture, natural resources and conservation": "agriculture",
    "Health and related fields": "health",
    "Personal, protective and transportation services": "personal_services",
    "Other instructional programs": "other",
}
