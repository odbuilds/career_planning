"""
100 AI automation use case seeds for SMBs (50-100 employees).
Covers Finance, HR, Operations, IT, Legal, Customer Success, and Marketing.
Excludes sales by design.
"""

USE_CASES = [
    # ─── FINANCE (25) ────────────────────────────────────────────────────────
    {
        "id": "fin_001", "dept": "finance",
        "name": "Automated Invoice Processing & Data Extraction",
        "search_hint": "LLM OCR invoice processing automation SMB accounts payable",
    },
    {
        "id": "fin_002", "dept": "finance",
        "name": "Expense Report Automation & Policy Compliance",
        "search_hint": "AI expense report automation receipt extraction policy check",
    },
    {
        "id": "fin_003", "dept": "finance",
        "name": "Accounts Payable Workflow Automation",
        "search_hint": "accounts payable AI automation three-way match workflow",
    },
    {
        "id": "fin_004", "dept": "finance",
        "name": "Cash Flow Forecasting with AI",
        "search_hint": "AI cash flow forecasting small business ML prediction",
    },
    {
        "id": "fin_005", "dept": "finance",
        "name": "Bank Reconciliation Automation",
        "search_hint": "automated bank reconciliation AI matching python accounting",
    },
    {
        "id": "fin_006", "dept": "finance",
        "name": "Month-End Close Acceleration",
        "search_hint": "AI month-end close automation checklist workflow finance",
    },
    {
        "id": "fin_007", "dept": "finance",
        "name": "Tax Document Preparation & Classification",
        "search_hint": "AI tax document classification preparation automation SMB",
    },
    {
        "id": "fin_008", "dept": "finance",
        "name": "Financial Anomaly & Fraud Detection",
        "search_hint": "AI fraud detection financial anomaly detection small business",
    },
    {
        "id": "fin_009", "dept": "finance",
        "name": "Budget Variance Analysis & Alerting",
        "search_hint": "AI budget variance analysis automated alerting finance LLM",
    },
    {
        "id": "fin_010", "dept": "finance",
        "name": "Vendor Payment Scheduling & Optimization",
        "search_hint": "AI vendor payment scheduling early discount optimization",
    },
    {
        "id": "fin_011", "dept": "finance",
        "name": "Contract Value Extraction & Financial Analysis",
        "search_hint": "LLM contract extraction financial terms NLP automation",
    },
    {
        "id": "fin_012", "dept": "finance",
        "name": "Automated Financial Report Generation",
        "search_hint": "AI automated financial report generation narrative python LLM",
    },
    {
        "id": "fin_013", "dept": "finance",
        "name": "Procurement Request & PO Automation",
        "search_hint": "AI procurement automation purchase order workflow approval",
    },
    {
        "id": "fin_014", "dept": "finance",
        "name": "Spend Analytics & Category Classification",
        "search_hint": "AI spend analytics categorization classification SMB automation",
    },
    {
        "id": "fin_015", "dept": "finance",
        "name": "Payroll Error Detection & Validation",
        "search_hint": "AI payroll error detection validation automation HR finance",
    },
    {
        "id": "fin_016", "dept": "finance",
        "name": "Audit Trail Documentation & Preparation",
        "search_hint": "AI audit preparation documentation automation compliance finance",
    },
    {
        "id": "fin_017", "dept": "finance",
        "name": "Revenue Recognition Automation",
        "search_hint": "AI revenue recognition ASC 606 IFRS 15 automation",
    },
    {
        "id": "fin_018", "dept": "finance",
        "name": "SaaS & Subscription Cost Optimization",
        "search_hint": "AI SaaS spend optimization tool discovery savings automation",
    },
    {
        "id": "fin_019", "dept": "finance",
        "name": "Customer Credit Risk Assessment",
        "search_hint": "AI credit risk assessment SMB customer scoring automation",
    },
    {
        "id": "fin_020", "dept": "finance",
        "name": "Accounts Receivable Collections Automation",
        "search_hint": "AI accounts receivable collections dunning automation follow-up",
    },
    {
        "id": "fin_021", "dept": "finance",
        "name": "Financial Document Classification & Routing",
        "search_hint": "AI financial document classification routing OCR automation",
    },
    {
        "id": "fin_022", "dept": "finance",
        "name": "Regulatory Compliance Monitoring (SOX/GAAP)",
        "search_hint": "AI SOX GAAP compliance monitoring automation alerts finance",
    },
    {
        "id": "fin_023", "dept": "finance",
        "name": "CFO Dashboard & KPI Automation",
        "search_hint": "AI CFO dashboard KPI automation real-time reporting LLM",
    },
    {
        "id": "fin_024", "dept": "finance",
        "name": "Insurance Claims Processing Assistance",
        "search_hint": "AI insurance claims processing automation extraction SMB",
    },
    {
        "id": "fin_025", "dept": "finance",
        "name": "Multi-Entity Consolidation & Intercompany Elimination",
        "search_hint": "AI multi-entity financial consolidation intercompany automation",
    },

    # ─── HR (25) ─────────────────────────────────────────────────────────────
    {
        "id": "hr_001", "dept": "hr",
        "name": "Resume Screening & Candidate Ranking",
        "search_hint": "AI resume screening ranking LLM candidate matching automation",
    },
    {
        "id": "hr_002", "dept": "hr",
        "name": "Job Description Generation & Optimization",
        "search_hint": "AI job description generation bias reduction optimization LLM",
    },
    {
        "id": "hr_003", "dept": "hr",
        "name": "Employee Onboarding Workflow Automation",
        "search_hint": "AI employee onboarding automation checklist workflow chatbot",
    },
    {
        "id": "hr_004", "dept": "hr",
        "name": "HR Policy Q&A Chatbot",
        "search_hint": "HR policy chatbot RAG Q&A employee questions automation",
    },
    {
        "id": "hr_005", "dept": "hr",
        "name": "Performance Review Drafting & Calibration Assistance",
        "search_hint": "AI performance review writing calibration assistant LLM HR",
    },
    {
        "id": "hr_006", "dept": "hr",
        "name": "Exit Interview Analysis & Retention Insights",
        "search_hint": "AI exit interview analysis sentiment themes automation HR",
    },
    {
        "id": "hr_007", "dept": "hr",
        "name": "Benefits Enrollment Guidance & Decision Support",
        "search_hint": "AI benefits enrollment chatbot guidance decision support HR",
    },
    {
        "id": "hr_008", "dept": "hr",
        "name": "Time-Off Request Processing & Coverage Planning",
        "search_hint": "AI time-off automation approval coverage scheduling HR",
    },
    {
        "id": "hr_009", "dept": "hr",
        "name": "Compliance Training Delivery & Tracking",
        "search_hint": "AI compliance training personalization tracking LMS automation",
    },
    {
        "id": "hr_010", "dept": "hr",
        "name": "Skills Gap Analysis & Learning Path Recommendations",
        "search_hint": "AI skills gap analysis learning recommendation HR development",
    },
    {
        "id": "hr_011", "dept": "hr",
        "name": "Employee Sentiment Analysis & Engagement Monitoring",
        "search_hint": "AI employee sentiment analysis engagement survey NLP HR",
    },
    {
        "id": "hr_012", "dept": "hr",
        "name": "Workforce Analytics & Headcount Planning",
        "search_hint": "AI workforce analytics headcount planning prediction HR",
    },
    {
        "id": "hr_013", "dept": "hr",
        "name": "HR Helpdesk Ticket Triage & Automation",
        "search_hint": "AI HR helpdesk automation ticket triage routing chatbot",
    },
    {
        "id": "hr_014", "dept": "hr",
        "name": "Succession Planning & Talent Identification",
        "search_hint": "AI succession planning talent identification automation HR",
    },
    {
        "id": "hr_015", "dept": "hr",
        "name": "Compensation Benchmarking & Pay Equity Analysis",
        "search_hint": "AI compensation benchmarking pay equity analysis automation HR",
    },
    {
        "id": "hr_016", "dept": "hr",
        "name": "Offer Letter Generation & Approval Workflow",
        "search_hint": "AI offer letter generation automation approval workflow HR",
    },
    {
        "id": "hr_017", "dept": "hr",
        "name": "Background Check Coordination & Status Tracking",
        "search_hint": "AI background check coordination automation status HR",
    },
    {
        "id": "hr_018", "dept": "hr",
        "name": "Employee Handbook Maintenance & Version Control",
        "search_hint": "AI employee handbook automation updates versioning HR",
    },
    {
        "id": "hr_019", "dept": "hr",
        "name": "360-Degree Feedback Aggregation & Theming",
        "search_hint": "AI 360 feedback aggregation themes NLP HR performance",
    },
    {
        "id": "hr_020", "dept": "hr",
        "name": "Turnover Prediction & Retention Risk Flagging",
        "search_hint": "AI turnover prediction churn risk ML HR analytics",
    },
    {
        "id": "hr_021", "dept": "hr",
        "name": "DEI Reporting & Bias Detection in Hiring",
        "search_hint": "AI DEI reporting bias detection hiring automation HR analytics",
    },
    {
        "id": "hr_022", "dept": "hr",
        "name": "Employee Recognition & Milestone Automation",
        "search_hint": "AI employee recognition automation milestone birthday anniversary HR",
    },
    {
        "id": "hr_023", "dept": "hr",
        "name": "Recruitment Pipeline Coordination & Scheduling",
        "search_hint": "AI recruiting automation interview scheduling pipeline coordination",
    },
    {
        "id": "hr_024", "dept": "hr",
        "name": "New Hire FAQ & Pre-boarding Chatbot",
        "search_hint": "AI new hire FAQ pre-boarding chatbot automation HR",
    },
    {
        "id": "hr_025", "dept": "hr",
        "name": "Attendance Pattern Analysis & Absence Management",
        "search_hint": "AI attendance pattern analysis absence management prediction HR",
    },

    # ─── OPERATIONS (20) ─────────────────────────────────────────────────────
    {
        "id": "ops_001", "dept": "operations",
        "name": "Meeting Transcription & Action Item Extraction",
        "search_hint": "AI meeting transcription action items extraction automation tools",
    },
    {
        "id": "ops_002", "dept": "operations",
        "name": "Email Triage & Priority Routing",
        "search_hint": "AI email triage priority classification routing automation LLM",
    },
    {
        "id": "ops_003", "dept": "operations",
        "name": "Project Status Report Generation",
        "search_hint": "AI project status report generation automation LLM PM tools",
    },
    {
        "id": "ops_004", "dept": "operations",
        "name": "Internal Knowledge Base Q&A (RAG)",
        "search_hint": "RAG internal knowledge base Q&A chatbot enterprise automation",
    },
    {
        "id": "ops_005", "dept": "operations",
        "name": "Process Documentation Automation",
        "search_hint": "AI process documentation SOPs automation generation LLM",
    },
    {
        "id": "ops_006", "dept": "operations",
        "name": "Vendor Onboarding & Due Diligence Automation",
        "search_hint": "AI vendor onboarding due diligence automation workflow",
    },
    {
        "id": "ops_007", "dept": "operations",
        "name": "Contract Review & Red Flag Detection",
        "search_hint": "AI contract review red flag detection NLP legal automation",
    },
    {
        "id": "ops_008", "dept": "operations",
        "name": "Approval Workflow Automation",
        "search_hint": "AI approval workflow automation routing escalation business",
    },
    {
        "id": "ops_009", "dept": "operations",
        "name": "SLA Monitoring & Proactive Alerting",
        "search_hint": "AI SLA monitoring alerting automation operations workflow",
    },
    {
        "id": "ops_010", "dept": "operations",
        "name": "Asset Lifecycle & Inventory Tracking",
        "search_hint": "AI asset tracking inventory lifecycle management automation",
    },
    {
        "id": "ops_011", "dept": "operations",
        "name": "Supply Chain Risk Monitoring",
        "search_hint": "AI supply chain risk monitoring disruption prediction automation",
    },
    {
        "id": "ops_012", "dept": "operations",
        "name": "Facilities Management Request Automation",
        "search_hint": "AI facilities management request routing automation workplace",
    },
    {
        "id": "ops_013", "dept": "operations",
        "name": "Cross-Department KPI Reporting Dashboard",
        "search_hint": "AI cross-functional KPI reporting dashboard automation LLM",
    },
    {
        "id": "ops_014", "dept": "operations",
        "name": "Document Version Control & Smart Archiving",
        "search_hint": "AI document version control archiving classification automation",
    },
    {
        "id": "ops_015", "dept": "operations",
        "name": "Business Travel Request & Expense Pre-Approval",
        "search_hint": "AI business travel automation policy compliance pre-approval",
    },
    {
        "id": "ops_016", "dept": "operations",
        "name": "Quality Control Checklist & Defect Detection",
        "search_hint": "AI quality control checklist defect detection automation operations",
    },
    {
        "id": "ops_017", "dept": "operations",
        "name": "Operational Risk Assessment & Dashboard",
        "search_hint": "AI operational risk assessment dashboard automation monitoring",
    },
    {
        "id": "ops_018", "dept": "operations",
        "name": "Customer Complaint Routing & Resolution Tracking",
        "search_hint": "AI customer complaint routing classification resolution tracking",
    },
    {
        "id": "ops_019", "dept": "operations",
        "name": "Internal Audit Scheduling & Evidence Collection",
        "search_hint": "AI internal audit scheduling evidence collection automation",
    },
    {
        "id": "ops_020", "dept": "operations",
        "name": "Regulatory Filing Preparation & Deadline Tracking",
        "search_hint": "AI regulatory filing automation deadline tracking compliance ops",
    },

    # ─── IT (10) ─────────────────────────────────────────────────────────────
    {
        "id": "it_001", "dept": "it",
        "name": "IT Helpdesk First-Level Support Automation",
        "search_hint": "AI IT helpdesk automation first-level support chatbot ticket",
    },
    {
        "id": "it_002", "dept": "it",
        "name": "Security Incident Triage & Response Automation",
        "search_hint": "AI security incident triage response SOAR automation SMB",
    },
    {
        "id": "it_003", "dept": "it",
        "name": "User Access Provisioning & Deprovisioning",
        "search_hint": "AI user access provisioning deprovisioning IAM automation",
    },
    {
        "id": "it_004", "dept": "it",
        "name": "Infrastructure Monitoring & Intelligent Alerting",
        "search_hint": "AI infrastructure monitoring anomaly detection alerting automation",
    },
    {
        "id": "it_005", "dept": "it",
        "name": "Software License Management & Optimization",
        "search_hint": "AI software license management optimization discovery automation",
    },
    {
        "id": "it_006", "dept": "it",
        "name": "Code Review Assistance & Static Analysis",
        "search_hint": "AI code review assistance static analysis automation GitHub",
    },
    {
        "id": "it_007", "dept": "it",
        "name": "IT Documentation Generation & Maintenance",
        "search_hint": "AI IT documentation generation runbook automation maintenance",
    },
    {
        "id": "it_008", "dept": "it",
        "name": "Log Analysis & Anomaly Detection",
        "search_hint": "AI log analysis anomaly detection automation ML operations",
    },
    {
        "id": "it_009", "dept": "it",
        "name": "Patch Management & Vulnerability Prioritization",
        "search_hint": "AI patch management vulnerability prioritization automation IT",
    },
    {
        "id": "it_010", "dept": "it",
        "name": "Disaster Recovery Planning & Testing Automation",
        "search_hint": "AI disaster recovery planning testing automation documentation IT",
    },

    # ─── LEGAL / COMPLIANCE (10) ──────────────────────────────────────────────
    {
        "id": "legal_001", "dept": "legal",
        "name": "NDA Review & Redlining Automation",
        "search_hint": "AI NDA review redlining automation LLM contract legal",
    },
    {
        "id": "legal_002", "dept": "legal",
        "name": "Regulatory Change Monitoring & Impact Analysis",
        "search_hint": "AI regulatory change monitoring impact analysis automation legal",
    },
    {
        "id": "legal_003", "dept": "legal",
        "name": "GDPR / Privacy Compliance Automation",
        "search_hint": "AI GDPR privacy compliance automation data mapping SMB",
    },
    {
        "id": "legal_004", "dept": "legal",
        "name": "Contract Renewal Tracking & Obligation Management",
        "search_hint": "AI contract renewal tracking obligation management automation",
    },
    {
        "id": "legal_005", "dept": "legal",
        "name": "Employment Law Compliance Assistant",
        "search_hint": "AI employment law compliance assistant automation HR legal",
    },
    {
        "id": "legal_006", "dept": "legal",
        "name": "Intellectual Property Tracking & Alert System",
        "search_hint": "AI intellectual property tracking alert system automation IP",
    },
    {
        "id": "legal_007", "dept": "legal",
        "name": "Third-Party Vendor Risk & Compliance Assessment",
        "search_hint": "AI third-party vendor risk compliance assessment automation",
    },
    {
        "id": "legal_008", "dept": "legal",
        "name": "Contract Template Management & Self-Service Portal",
        "search_hint": "AI contract template management self-service portal automation",
    },
    {
        "id": "legal_009", "dept": "legal",
        "name": "Policy Acknowledgement & Attestation Tracking",
        "search_hint": "AI policy acknowledgement tracking attestation automation compliance",
    },
    {
        "id": "legal_010", "dept": "legal",
        "name": "Litigation Hold & eDiscovery Support",
        "search_hint": "AI litigation hold eDiscovery support automation legal",
    },

    # ─── CUSTOMER SUCCESS (5) ─────────────────────────────────────────────────
    {
        "id": "cs_001", "dept": "customer_success",
        "name": "Customer Feedback Classification & Routing",
        "search_hint": "AI customer feedback classification routing NLP automation",
    },
    {
        "id": "cs_002", "dept": "customer_success",
        "name": "Renewal Risk Scoring & Churn Prediction",
        "search_hint": "AI renewal risk churn prediction scoring automation customer success",
    },
    {
        "id": "cs_003", "dept": "customer_success",
        "name": "Customer Onboarding Checklist & Progress Automation",
        "search_hint": "AI customer onboarding checklist automation progress tracking",
    },
    {
        "id": "cs_004", "dept": "customer_success",
        "name": "Support Knowledge Base Q&A & Deflection",
        "search_hint": "AI support knowledge base RAG Q&A deflection automation",
    },
    {
        "id": "cs_005", "dept": "customer_success",
        "name": "Account Health Scoring & QBR Preparation",
        "search_hint": "AI account health scoring QBR preparation automation customer success",
    },

    # ─── MARKETING / COMMS (5) ───────────────────────────────────────────────
    {
        "id": "mktg_001", "dept": "marketing",
        "name": "Internal Newsletter & Comms Generation",
        "search_hint": "AI internal newsletter generation automation employee comms LLM",
    },
    {
        "id": "mktg_002", "dept": "marketing",
        "name": "Competitive Intelligence Monitoring & Digest",
        "search_hint": "AI competitive intelligence monitoring digest automation market",
    },
    {
        "id": "mktg_003", "dept": "marketing",
        "name": "Job Posting Drafting & Multi-Channel Distribution",
        "search_hint": "AI job posting automation multi-channel distribution HR marketing",
    },
    {
        "id": "mktg_004", "dept": "marketing",
        "name": "Brand & Mention Monitoring",
        "search_hint": "AI brand mention monitoring sentiment alerting automation",
    },
    {
        "id": "mktg_005", "dept": "marketing",
        "name": "Content Calendar Planning & Brief Generation",
        "search_hint": "AI content calendar planning brief generation automation marketing",
    },
]

DEPT_LABELS = {
    "finance": "Finance",
    "hr": "Human Resources",
    "operations": "Operations",
    "it": "IT & Engineering",
    "legal": "Legal & Compliance",
    "customer_success": "Customer Success",
    "marketing": "Marketing & Communications",
}
