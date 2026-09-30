"""
*************************
Mã sinh viên: 202418941
Họ tên: Hà Văn Mạnh
*************************
"""

# ==============================================================================
# B1. LỚP EMPLOYEE
# ==============================================================================
class Employee:
    """
    Lớp Employee đại diện cho nhân sự thông thường trong hệ thống.
    """
    def __init__(self, id: str = "UNKNOWN", full_name: str = "Unnamed employee", base_salary: float = 0.0):
        # Ràng buộc bất biến: Mã và họ tên không rỗng, lương không âm
        if not id or not id.strip():
            raise ValueError("[Lỗi Bất Biến] Mã nhân sự không được để rỗng.")
        if not full_name or not full_name.strip():
            raise ValueError("[Lỗi Bất Biến] Họ tên nhân sự không được để rỗng.")
        if base_salary < 0:
            raise ValueError("[Lỗi Bất Biến] Lương cơ bản không được âm.")

        self._id = id.strip()
        self._full_name = full_name.strip()
        self._base_salary = float(base_salary)

    def __del__(self):
        # Destructor in thông báo quan sát vòng đời
        print(f"  [Destructor Employee] Hủy nhân sự '{self._full_name}' (ID: {self._id})")

    def get_id(self) -> str:
        return self._id

    def get_full_name(self) -> str:
        return self._full_name

    def get_base_salary(self) -> float:
        return self._base_salary

    def increase_salary(self, value: float, by_percentage: bool = False) -> None:
        """Nạp chồng phương thức tăng lương."""
        if value <= 0:
            raise ValueError("[Lỗi Bất Biến] Giá trị tăng lương phải dương (> 0).")

        if by_percentage:
            increase_amount = self._base_salary * (value / 100.0)
            self._base_salary += increase_amount
            print(f"  => Tăng {value}% lương cho {self._full_name}. Lương mới: {self._base_salary:,.0f} VNĐ")
        else:
            self._base_salary += value
            print(f"  => Tăng {value:,.0f} VNĐ cho {self._full_name}. Lương mới: {self._base_salary:,.0f} VNĐ")

    def calculate_monthly_cost(self) -> float:
        """Đa hình: Mặc định bằng lương cơ bản."""
        return self._base_salary

    def display_info(self) -> None:
        """Đa hình: In thông tin nhân sự."""
        print(f"[Employee] ID: {self._id} | Họ tên: {self._full_name} | Lương cơ bản: {self._base_salary:,.0f} VNĐ")


# ==============================================================================
# B2. LỚP SOFTWARE ENGINEER
# ==============================================================================
class SoftwareEngineer(Employee):
    """
    Lớp SoftwareEngineer kế thừa từ Employee, bổ sung ngôn ngữ và phụ cấp.
    """
    def __init__(self, id: str, full_name: str, base_salary_or_lang: str | float, 
                 primary_language: str = "", technical_allowance: float = 0.0):
        
        # Nạp chồng constructor dựa trên kiểu dữ liệu của tham số thứ 3
        if isinstance(base_salary_or_lang, str):
            # Constructor 1: (id, full_name, primary_language)
            super().__init__(id, full_name, 0.0)
            lang = base_salary_or_lang
            allowance = 0.0
        else:
            # Constructor 2: (id, full_name, base_salary, primary_language, technical_allowance)
            super().__init__(id, full_name, base_salary_or_lang)
            lang = primary_language
            allowance = technical_allowance

        # Ràng buộc bất biến: Ngôn ngữ không rỗng, phụ cấp không âm
        if not lang or not lang.strip():
            raise ValueError("[Lỗi Bất Biến] Ngôn ngữ lập trình chính không được để rỗng.")
        if allowance < 0:
            raise ValueError("[Lỗi Bất Biến] Phụ cấp kỹ thuật không được âm.")

        self._primary_language = lang.strip()
        self._technical_allowance = float(allowance)

    def __del__(self):
        print(f"  [Destructor SoftwareEngineer] Hủy kỹ sư '{self._full_name}' (ID: {self._id})")
        super().__del__()

    def get_primary_language(self) -> str:
        return self._primary_language

    def get_technical_allowance(self) -> float:
        return self._technical_allowance

    def calculate_monthly_cost(self) -> float:
        """Ghi đè: Tổng lương cơ bản + Phụ cấp kỹ thuật."""
        return self._base_salary + self._technical_allowance

    def display_info(self) -> None:
        """Ghi đè: In thêm thông tin kỹ sư."""
        print(f"[SoftwareEngineer] ID: {self._id} | Họ tên: {self._full_name} | "
              f"Lương CB: {self._base_salary:,.0f} VNĐ | Ngôn ngữ: {self._primary_language} | "
              f"Phụ cấp: {self._technical_allowance:,.0f} VNĐ | Tổng chi phí: {self.calculate_monthly_cost():,.0f} VNĐ")


# ==============================================================================
# B3. LỚP PROJECT TEAM
# ==============================================================================
class ProjectTeam:
    """
    Lớp ProjectTeam quản lý dự án và danh sách liên kết không sở hữu (Aggregation) các nhân sự.
    """
    def __init__(self, project_code: str, project_name: str, leader: Employee = None):
        if not project_code or not project_code.strip():
            raise ValueError("[Lỗi Bất Biến] Mã dự án không được để rỗng.")
        if not project_name or not project_name.strip():
            raise ValueError("[Lỗi Bất Biến] Tên dự án không được để rỗng.")

        self._project_code = project_code.strip()
        self._project_name = project_name.strip()
        self._leader: Employee | None = None
        self._members: list[Employee] = []  # Danh sách liên kết không sở hữu

        # Constructor 2: Nếu có leader truyền vào, thiết lập và đưa vào danh sách thành viên
        if leader is not None:
            self._leader = leader
            self._members.append(leader)

    def __del__(self):
        # Destructor chỉ hủy danh sách nội bộ, KHÔNG hủy các đối tượng Employee
        print(f"  [Destructor ProjectTeam] Hủy dự án '{self._project_name}' (Mã: {self._project_code}). "
              f"Các đối tượng Employee bên trong vẫn an toàn.")
        self._members.clear()
        self._leader = None

    def contains(self, employee_id: str) -> bool:
        """Kiểm tra một nhân sự có trong nhóm hay không."""
        return any(emp.get_id() == employee_id for emp in self._members)

    def add_member(self, employee: Employee, make_leader: bool = False) -> bool:
        """Nạp chồng addMember."""
        # Bất biến: Không có 2 thành viên cùng mã trong 1 nhóm
        if self.contains(employee.get_id()):
            print(f"  [Cảnh báo Add] Nhân sự ID '{employee.get_id()}' đã tồn tại trong nhóm {self._project_code}!")
            return False

        self._members.append(employee)
        if make_leader:
            self._leader = employee
            print(f"  => Đã thêm {employee.get_full_name()} vào nhóm và đặt làm TRƯỞNG NHÓM.")
        else:
            print(f"  => Đã thêm thành viên {employee.get_full_name()} vào nhóm.")
        return True

    def remove_member(self, employee_id: str) -> bool:
        """Xóa thành viên khỏi nhóm."""
        if not self.contains(employee_id):
            print(f"  [Cảnh báo Remove] Không tìm thấy nhân sự ID '{employee_id}' trong nhóm!")
            return False

        # Bất biến: Không được xóa trưởng nhóm khi chưa chọn trưởng nhóm thay thế
        if self._leader and self._leader.get_id() == employee_id:
            print(f"  [Từ chối Xóa] KHÔNG THỂ XÓA ID '{employee_id}' vì đang là Trưởng nhóm! Hãy đổi trưởng nhóm trước.")
            return False

        self._members = [emp for emp in self._members if emp.get_id() != employee_id]
        print(f"  => Đã xóa thành công nhân sự ID '{employee_id}' khỏi nhóm.")
        return True

    def change_leader(self, employee: Employee) -> bool:
        """Đổi trưởng nhóm mới."""
        # Bất biến: Trưởng nhóm mới phải được thêm vào nhóm nếu chưa phải thành viên
        if not self.contains(employee.get_id()):
            print(f"  => Trưởng nhóm mới chưa thuộc nhóm. Tự động thêm vào danh sách...")
            self._members.append(employee)
            
        self._leader = employee
        print(f"  => Đã đổi Trưởng nhóm mới thành: {employee.get_full_name()} (ID: {employee.get_id()})")
        return True

    def calculate_total_monthly_cost(self) -> float:
        """Tính tổng chi phí nhân sự hằng tháng của cả nhóm dự án."""
        return sum(emp.calculate_monthly_cost() for emp in self._members)

    def display_team(self) -> None:
        """Hiển thị danh sách thông tin nhóm."""
        print(f"\n=================== DỰ ÁN: {self._project_name} ({self._project_code}) ===================")
        leader_name = self._leader.get_full_name() if self._leader else "Chưa có"
        print(f"Trưởng nhóm: {leader_name}")
        print(f"Số lượng thành viên: {len(self._members)}")
        print("---------------- Danh sách thành viên ----------------")
        for idx, emp in enumerate(self._members, 1):
            print(f"{idx}. ", end="")
            emp.display_info()  # Lời gọi đa hình
        print(f"--> TỔNG CHI PHÍ HẰNG THÁNG CỦA NHÓM: {self.calculate_total_monthly_cost():,.0f} VNĐ")
        print("====================================================================================\n")


# ==============================================================================
# C: KIỂM THỬ THEO KỊCH BẢN 15 BƯỚC + TRƯỜNG HỢP BIÊN
# ==============================================================================
def run_lab_test_suite():
    print("\n****************************************************************")
    print("      BẮT ĐẦU KIỂM THỬ HỆ THỐNG QUẢN LÝ DỰ ÁN VÀ NHÂN SỰ")
    print("****************************************************************\n")

    # 1. Tạo hai Employee bằng hai constructor khác nhau
    print("--- [Bước 1] Tạo 2 Employee bằng 2 constructor khác nhau ---")
    emp1 = Employee("NV01", "Nguyễn Văn Anh")  # Constructor 2
    emp2 = Employee("NV02", "Trần Thị Bình", 12000000)  # Constructor 3
    emp1.display_info()
    emp2.display_info()

    # 2. Tạo hai Software Engineer bằng hai constructor khác nhau
    print("\n--- [Bước 2] Tạo 2 Software Engineer bằng 2 constructor khác nhau ---")
    se1 = SoftwareEngineer("SE01", "Lê Minh Cường", "Python")  # Constructor 1
    se2 = SoftwareEngineer("SE02", "Phạm Hoàng Dũng", 20000000, "C++", 5000000)  # Constructor 2
    se1.display_info()
    se2.display_info()

    # 3. Tăng lương một nhân sự bằng số tiền cố định
    print("\n--- [Bước 3] Tăng lương cố định (Tăng 3.000.000 VNĐ cho NV01) ---")
    emp1.increase_salary(3000000)

    # 4. Tăng lương một nhân sự khác theo phần trăm
    print("\n--- [Bước 4] Tăng lương theo phần trăm (Tăng 15% cho NV02) ---")
    emp2.increase_salary(15, by_percentage=True)

    # 5. Tạo nhóm dự án không có trưởng nhóm
    print("\n--- [Bước 5] Tạo nhóm dự án 1 chưa có trưởng nhóm ---")
    team1 = ProjectTeam("PRJ01", "Hệ thống AI Chatbot")

    # 6. Thêm một nhân sự vào nhóm bằng addMember(employee)
    print("\n--- [Bước 6] Thêm nhân sự NV01 vào nhóm 1 ---")
    team1.add_member(emp1)

    # 7. Thêm một kỹ sư bằng addMember(employee, true) để đặt làm trưởng nhóm
    print("\n--- [Bước 7] Thêm kỹ sư SE02 làm Trưởng nhóm 1 ---")
    team1.add_member(se2, make_leader=True)

    # 8. Thử thêm lại một thành viên đã tồn tại
    print("\n--- [Bước 8] Thử thêm lại NV01 vào nhóm 1 (Kiểm tra trùng mã) ---")
    team1.add_member(emp1)

    # 9. Hiển thị danh sách bằng lời gọi đa hình
    print("\n--- [Bước 9] Hiển thị thông tin nhóm 1 bằng lời gọi ĐA HÌNH ---")
    team1.display_team()

    # 10. Tính tổng chi phí nhân sự hằng tháng
    print(f"--- [Bước 10] Xác nhận Tổng chi phí nhóm 1: {team1.calculate_total_monthly_cost():,.0f} VNĐ ---")

    # 11. Thử xóa trưởng nhóm hiện tại và kiểm tra thao tác bị từ chối
    print("\n--- [Bước 11] Thử xóa Trưởng nhóm hiện tại (SE02 - ID: SE02) ---")
    team1.remove_member("SE02")

    # 12. Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm
    print("\n--- [Bước 12] Đổi Trưởng nhóm sang SE01, sau đó xóa SE02 ---")
    team1.change_leader(se1)
    team1.remove_member("SE02")
    print("\nDanh sách nhóm 1 sau khi đổi trưởng nhóm và xóa SE02:")
    team1.display_team()

    # 13. Tạo nhóm thứ hai và thêm nhân sự đã có ở nhóm thứ nhất (Kết tập nhiều nhóm)
    print("--- [Bước 13] Tạo nhóm 2 và thêm NV01 (Đã nằm ở nhóm 1) ---")
    team2 = ProjectTeam("PRJ02", "Ứng dụng Mobile Racing")
    team2.add_member(emp1)  # NV01 đồng thời xuất hiện ở cả Team 1 và Team 2
    team2.add_member(se2, make_leader=True)
    team2.display_team()

    # 14 & 15. Hủy nhóm thứ hai bằng cách kết thúc khối lệnh cục bộ & Chứng minh nhân sự vẫn tồn tại
    print("--- [Bước 14 & 15] Hủy nhóm 2 và chứng minh NV01 vẫn tồn tại ---")
    def sub_scope_destroy_team():
        temp_team = ProjectTeam("TEMP_PRJ", "Dự án Thử Nghiệm Tạm Thời")
        temp_team.add_member(emp1)
        print("  --> Trong hàm: Dự án tạm thời đã được tạo và chứa NV01.")
        print("  --> Bắt đầu thoát khỏi scope (hủy temp_team)...")

    sub_scope_destroy_team()
    print("  --> Đã thoát khỏi scope. Dự án tạm thời bị giải phóng thành công!")
    print("  --> Kiểm tra đối tượng NV01 vẫn hoạt động bình thường:")
    emp1.display_info()

    print("\n****************************************************************")
    print("              KẾT THÚC TOÀN BỘ KỊCH BẢN KIỂM THỬ")
    print("****************************************************************\n")


if __name__ == "__main__":
    run_lab_test_suite()


