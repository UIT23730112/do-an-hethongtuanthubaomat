from typing import List, Dict

COMPLIANCE_RULES: List[Dict] = [
    {
        "rule_id": "LFT-01",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Website có công bố chính sách bảo vệ dữ liệu cá nhân/privacy policy dễ truy cập (footer hoặc trước khi thu thập dữ liệu)",
        "keywords": [
            "privacy policy",
            "chính sách bảo vệ dữ liệu",
            "chính sách quyền riêng tư",
            "điều khoản bảo mật"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "LFT-02",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Chính sách xác định rõ bên kiểm soát dữ liệu (tên tổ chức, cá nhân)",
        "keywords": [
            "data controller",
            "bên kiểm soát dữ liệu",
            "chủ thể kiểm soát",
            "tổ chức xử lý",
            "công ty chịu trách nhiệm"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "LFT-03",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Chính sách cung cấp thông tin liên hệ của bên kiểm soát/xử lý dữ liệu (email, hotmail, địa chỉ)",
        "keywords": [
            "contact information",
            "thông tin liên hệ",
            "liên lạc",
            "email",
            "địa chỉ",
            "hotline"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "LFT-04",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Chính sách nêu rõ căn cứ pháp lý cho việc xử lý dữ liệu cá nhân (đồng ý, nghĩa vụ pháp luật, hợp đồng, lợi ích hợp pháp…)",
        "keywords": [
            "legal basis",
            "căn cứ pháp lý",
            "pháp lý",
            "cơ sở xử lý",
            "đồng ý",
            "consent"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "LFT-05",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Chính sách mô tả loại dữ liệu cá nhân được thu thập (dữ liệu cơ bản, dữ liệu nhạy cảm nếu có)",
        "keywords": [
            "data types",
            "loại dữ liệu",
            "dữ liệu thu thập",
            "dữ liệu nhạy cảm",
            "thông tin thu thập"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "LFT-06",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Nội dung chính sách được trình bày rõ ràng, dễ hiểu, không dùng thuật ngữ mơ hồ gây hiểu nhầm cho người dùng",
        "keywords": [
            "clear language",
            "dễ hiểu",
            "rõ ràng",
            "minh bạch",
            "không mơ hồ"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "LFT-07",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Website thông báo cho người dùng trước hoặc tại thời điểm thu thập dữ liệu (không thu thập 'ngầm')",
        "keywords": [
            "notification",
            "thông báo",
            "thu thập dữ liệu",
            "trước khi thu thập",
            "inform"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "LFT-08",
        "group": "Lawfulness, Fairness, Transparency",
        "description": "Chính sách không chứa điều khoản gây bất lợi, ép buộc hoặc che giấy quyền của chủ thể dữ liệu",
        "keywords": [
            "fair terms",
            "điều khoản công bằng",
            "không ép buộc",
            "không bất lợi",
            "quyền người dùng"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "PL-01",
        "group": "Purpose Limitation",
        "description": "Chính sách nêu rõ từng mục đích cụ thể của việc thu thập và xử lý dữ liệu cá nhân",
        "keywords": [
            "purpose",
            "mục đích",
            "xử lý dữ liệu",
            "sử dụng dữ liệu",
            "lý do thu thập"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "PL-02",
        "group": "Purpose Limitation",
        "description": "Mục đích xử lý phù hợp với loại dữ liệu thu thập (không thu thập vượt nhu cầu mục đích)",
        "keywords": [
            "proportional",
            "phù hợp",
            "cần thiết",
            "tương xứng",
            "appropriate"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "PL-03",
        "group": "Purpose Limitation",
        "description": "Chính sách không sử dụng mục đích chung chung hoặc mơ hồ (ví dụ: 'cải thiện dịch vụ', 'mục đích nội bộ' không giải thích)",
        "keywords": [
            "specific purpose",
            "mục đích cụ thể",
            "không chung chung",
            "rõ ràng",
            "chi tiết"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "PL-04",
        "group": "Purpose Limitation",
        "description": "Website thông báo và/hoặc xin lại sự đồng ý nếu thay đổi mục đích xử lý dữ liệu so với ban đầu",
        "keywords": [
            "change purpose",
            "thay đổi mục đích",
            "xin lại đồng ý",
            "thông báo thay đổi",
            "purpose change"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "PL-05",
        "group": "Purpose Limitation",
        "description": "Chính sách phân biệt rõ mục đích chính và mục đích phụ (marketing, phân tích, chia sẻ cho bên thứ ba nếu có)",
        "keywords": [
            "primary purpose",
            "secondary purpose",
            "mục đích chính",
            "mục đích phụ",
            "marketing",
            "phân tích"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "DM-01",
        "group": "Data Minimization",
        "description": "Chính sách chỉ liệt kê các loại dữ liệu cần thiết cho từng mục đích xử lý, không thu thập tràn lan",
        "keywords": [
            "minimal data",
            "tối thiểu dữ liệu",
            "cần thiết",
            "không tràn lan",
            "limited collection"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "DM-02",
        "group": "Data Minimization",
        "description": "Website không yêu cầu dữ liệu cá nhân nhạy cảm nếu không có mục đích và căn cứ pháp lý rõ ràng",
        "keywords": [
            "sensitive data",
            "dữ liệu nhạy cảm",
            "special category",
            "bảo vệ đặc biệt",
            "sensitive information"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "DM-03",
        "group": "Data Minimization",
        "description": "Các biểu mẫu không thu thập dữ liệu vượt quá chức năng dịch vụ",
        "keywords": [
            "excessive data",
            "vượt quá",
            "không cần thiết",
            "biểu mẫu",
            "form fields"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "DM-04",
        "group": "Data Minimization",
        "description": "Chính sách giải thích lý do thu thập cho từng nhóm dữ liệu chính",
        "keywords": [
            "explain collection",
            "giải thích",
            "lý do thu thập",
            "tại sao thu thập",
            "reason for collection"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "AC-01",
        "group": "Accuracy",
        "description": "Chính sách cam kết duy trì dữ liệu cá nhân chính xác và cập nhật",
        "keywords": [
            "accurate data",
            "chính xác",
            "cập nhật",
            "up to date",
            "accuracy"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "AC-02",
        "group": "Accuracy",
        "description": "Chủ thể dữ liệu có quyền yêu cầu chỉnh sửa, cập nhật dữ liệu cá nhân",
        "keywords": [
            "right to rectify",
            "quyền chỉnh sửa",
            "sửa dữ liệu",
            "cập nhật thông tin",
            "rectification"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "AC-03",
        "group": "Accuracy",
        "description": "Website cung cấp cơ chế hoặc hướng dẫn rõ ràng để người dùng thực hiện quyền chỉnh sửa",
        "keywords": [
            "rectification mechanism",
            "cơ chế chỉnh sửa",
            "hướng dẫn",
            "cách sửa",
            "how to update"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "SL-01",
        "group": "Storage Limitation",
        "description": "Chính sách xác định rõ thời hạn lưu trữ dữ liệu cá nhân hoặc tiêu chí xác định thời hạn",
        "keywords": [
            "retention period",
            "thời hạn lưu trữ",
            "lưu trữ",
            "bao lâu",
            "storage duration"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "SL-02",
        "group": "Storage Limitation",
        "description": "Dữ liệu cá nhân không được lưu trữ quá thời hạn cần thiết so với mục đích đã công bố",
        "keywords": [
            "not exceed",
            "không quá hạn",
            "phù hợp thời hạn",
            "đủ cần thiết",
            "limited storage"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "SL-03",
        "group": "Storage Limitation",
        "description": "Chính sách quy định rõ việc xóa, hủy hoặc ẩn danh dữ liệu khi hết thời hạn lưu trữ",
        "keywords": [
            "deletion",
            "xóa",
            "hủy",
            "ẩn danh",
            "kết thúc lưu trữ",
            "destroy"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "SL-04",
        "group": "Storage Limitation",
        "description": "Chủ thể dữ liệu được thông tin về thời gian lưu trữ hoặc quyền yêu cầu xóa dữ liệu",
        "keywords": [
            "right to deletion",
            "quyền xóa",
            "thông tin lưu trữ",
            "yêu cầu xóa",
            "right to erasure"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "IC-01",
        "group": "Integrity and Confidentiality",
        "description": "Chính sách cam kết áp dụng biện pháp kỹ thuật và tổ chức để bảo vệ dữ liệu cá nhân",
        "keywords": [
            "security measures",
            "biện pháp bảo vệ",
            "an toàn",
            "bảo mật",
            "technical measures"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "IC-02",
        "group": "Integrity and Confidentiality",
        "description": "Dữ liệu cá nhân được bảo vệ khỏi truy cập, sử dụng trái phép",
        "keywords": [
            "unauthorized access",
            "truy cập trái phép",
            "sử dụng trái phép",
            "bảo vệ",
            "prevent access"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "IC-03",
        "group": "Integrity and Confidentiality",
        "description": "Có biện pháp bảo vệ dữ liệu trong quá trình truyền và lưu trữ (ví dụ: mã hóa)",
        "keywords": [
            "encryption",
            "mã hóa",
            "bảo vệ truyền",
            "bảo vệ lưu trữ",
            "transmission security"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "IC-04",
        "group": "Integrity and Confidentiality",
        "description": "Chính sách quy định phân quyền truy cập dữ liệu cho nhân sự có thẩm quyền",
        "keywords": [
            "access control",
            "phân quyền",
            "truy cập",
            "nhân sự",
            "authorized personnel"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "IC-05",
        "group": "Integrity and Confidentiality",
        "description": "Có cơ chế phát hiện, xử lý và hạn chế sự cố rò rỉ dữ liệu",
        "keywords": [
            "data breach",
            "rò rỉ dữ liệu",
            "sự cố",
            "xử lý sự cố",
            "breach response"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "IC-06",
        "group": "Integrity and Confidentiality",
        "description": "Website thông báo nghĩa vụ bảo mật của bên thứ ba khi chia sẻ dữ liệu",
        "keywords": [
            "third party security",
            "bên thứ ba",
            "nghĩa vụ bảo mật",
            "chia sẻ dữ liệu",
            "third party obligations"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "IC-07",
        "group": "Integrity and Confidentiality",
        "description": "Chính sách đề cập đến việc kiểm tra, đánh giá định kỳ các biện pháp bảo mật",
        "keywords": [
            "regular review",
            "đánh giá định kỳ",
            "kiểm tra",
            "review security",
            "periodic assessment"
        ],
        "severity": "LOW",
        "weight": 1
    },
    {
        "rule_id": "ACT-01",
        "group": "Accountability",
        "description": "Chính sách xác định rõ trách nhiệm của bên kiểm soát và/hoặc bên xử lý dữ liệu cá nhân",
        "keywords": [
            "responsibilities",
            "trách nhiệm",
            "bên xử lý",
            "accountability",
            "roles"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "ACT-02",
        "group": "Accountability",
        "description": "Website lưu trữ và duy trì hồ sơ liên quan đến hoạt động xử lý dữ liệu (records, logs, policies)",
        "keywords": [
            "records",
            "hồ sơ",
            "lưu trữ hồ sơ",
            "documentation",
            "processing records"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "ACT-03",
        "group": "Accountability",
        "description": "Có cơ chế kiểm tra, đánh giá nội bộ hoặc đánh giá định kỳ về việc tuân thủ bảo vệ dữ liệu cá nhân",
        "keywords": [
            "compliance assessment",
            "đánh giá tuân thủ",
            "kiểm tra nội bộ",
            "internal audit",
            "compliance check"
        ],
        "severity": "MEDIUM",
        "weight": 2
    },
    {
        "rule_id": "ACT-04",
        "group": "Accountability",
        "description": "Chính sách đề cập đến việc đánh giá tác động xử lý dữ liệu cá nhân đối với các hoạt động có rủi ro cao",
        "keywords": [
            "impact assessment",
            "đánh giá tác động",
            "rủi ro cao",
            "DPIA",
            "data protection impact"
        ],
        "severity": "HIGH",
        "weight": 3
    },
    {
        "rule_id": "ACT-05",
        "group": "Accountability",
        "description": "Có cơ chế tiếp nhận, xử lý khiếu nại và chịu trách nhiệm pháp lý khi xảy ra vi phạm dữ liệu cá nhân",
        "keywords": [
            "complaints",
            "khiếu nại",
            "trách nhiệm pháp lý",
            "xử lý khiếu nại",
            "complaint mechanism"
        ],
        "severity": "HIGH",
        "weight": 3
    }
]