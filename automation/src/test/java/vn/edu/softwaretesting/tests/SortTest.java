package vn.edu.softwaretesting.tests;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

import vn.edu.softwaretesting.core.WebTestBase;
import vn.edu.softwaretesting.pages.InventoryPage;
import vn.edu.softwaretesting.pages.LoginPage;

/**
 * Test cases cho FR-04: Sắp xếp sản phẩm
 * Sử dụng kỹ thuật EP (Equivalence Partitioning)
 */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class SortTest extends WebTestBase {

    private LoginPage loginPage;
    private InventoryPage inventoryPage;

    @BeforeEach
    void initPages() {
        loginPage = new LoginPage(driver, baseUrl);
        inventoryPage = new InventoryPage(driver);
    }

    private void login() {
        loginPage.open();
        LoginPage.LoginResult result = loginPage
                .login("standard_user", "secret_sauce");
        System.out.printf(Locale.US,
                "[LOGIN] accepted=%s | url=%s | message=%s%n",
                result.accepted(), result.currentUrl(), result.message());
        inventoryPage.open();
    }

    /** In ra bảng tên/giá sản phẩm hiện tại để đối chiếu khi test FAIL. */
    private void logItems(String label) {
        List<String> names = inventoryPage.getItemNames();
        List<Double> prices = inventoryPage.getItemPrices();
        System.out.printf(Locale.US, "%n=== %s ===%n", label);
        for (int i = 0; i < names.size(); i++) {
            double price = i < prices.size() ? prices.get(i) : 0.0;
            System.out.printf(Locale.US, "  [%d] %-30s $%.2f%n",
                    i, names.get(i), price);
        }
        System.out.printf(Locale.US, "  -> Tổng %d sản phẩm%n%n", names.size());
    }

    // ==================== Test Cases với EP ====================

    @Test
    @Order(1) //Xác định thứ tự chạy của phương thức test.
    @DisplayName("TC-SORT-EP1: Kiểm tra sắp xếp Name A->Z (EP)")
    void testSortNameATOZ() {
        login();

        inventoryPage.selectSort("az");
        List<String> names = inventoryPage.getItemNames();

        // Kiểm tra danh sách đã được sắp xếp A->Z
        List<String> sortedNames = new ArrayList<>(names);
        Collections.sort(sortedNames);

        logItems("TC-SORT-EP1 - Sort Name A->Z");
        System.out.printf(Locale.US, "  Thực tế  : %s%n", names);
        System.out.printf(Locale.US, "  Mong đợi  : %s%n", sortedNames);
        assertEquals(sortedNames, names, "Danh sách phải được sắp xếp A->Z");
    }

    @Test
    @Order(2)
    @DisplayName("TC-SORT-EP2: Kiểm tra sắp xếp Name Z->A (EP)")
    void testSortNameZTOA() {
        login();

        inventoryPage.selectSort("za");
        List<String> names = inventoryPage.getItemNames();

        // Kiểm tra danh sách đã được sắp xếp Z->A
        List<String> sortedNames = new ArrayList<>(names);
        Collections.sort(sortedNames, Collections.reverseOrder());

        logItems("TC-SORT-EP2 - Sort Name Z->A");
        System.out.printf(Locale.US, "  Thực tế  : %s%n", names);
        System.out.printf(Locale.US, "  Mong đợi  : %s%n", sortedNames);
        assertEquals(sortedNames, names, "Danh sách phải được sắp xếp Z->A");
    }

    @ParameterizedTest //Cho phép một phương thức test chạy nhiều lần với các bộ dữ liệu đầu vào khác nhau.
    @Order(3)
    @ValueSource(strings = {"az", "za", "lohi", "hilo"}) //Cung cấp danh sách dữ liệu đầu vào cho
    @DisplayName("TC-SORT-EP3-6: Kiểm tra tất cả 4 kiểu sort (Parameterized)")
    void testAllSortOptions(String sortOption) {
        login();

        inventoryPage.selectSort(sortOption);

        // Kiểm tra dropdown đã được chọn đúng
        logItems("TC-SORT-EP3-6 - Sort option: " + sortOption);
        System.out.printf(Locale.US, "  Số sản phẩm hiển thị: %d%n",
                inventoryPage.getItemCount());
        assertTrue(inventoryPage.isLoaded(), "Trang phải load đầy đủ sau khi sort");
        assertTrue(inventoryPage.getItemCount() > 0, "Phải có sản phẩm hiển thị");
    }

    // ==================== Test Cases với BVA ====================

    @ParameterizedTest
    @Order(4)
    @CsvSource({
        "lohi, 0, true,   // Sản phẩm giá thấp nhất ở đầu",
        "hilo, 0, false,  // Sản phẩm giá cao nhất ở đầu"
    })//Cung cấp nhiều tham số cho một lần chạy test bằng dữ liệu CSV
    @DisplayName("TC-SORT-BVA1-2: Kiểm tra boundary với giá min/max")
    void testBoundaryPriceSort(String sortOption, int firstItemIndex, boolean isLowestFirst) {
        login();

        inventoryPage.selectSort(sortOption);
        List<Double> prices = inventoryPage.getItemPrices();

        assertTrue(prices.size() > firstItemIndex, "Phải có ít nhất 1 sản phẩm");

        double firstPrice = prices.get(firstItemIndex);
        double minPrice = prices.stream().min(Double::compare).orElse(0.0);
        double maxPrice = prices.stream().max(Double::compare).orElse(0.0);

        logItems("TC-SORT-BVA1-2 - Sort option: " + sortOption);
        System.out.printf(Locale.US, "  Giá tại index %d : $%.2f%n",
                firstItemIndex, firstPrice);
        System.out.printf(Locale.US, "  Giá min trong danh sách: $%.2f%n", minPrice);
        System.out.printf(Locale.US, "  Giá max trong danh sách: $%.2f%n", maxPrice);
        System.out.printf(Locale.US, "  Kỳ vọng đầu danh sách là giá %s%n",
                isLowestFirst ? "NHỎ NHẤT" : "LỚN NHẤT");

        if (isLowestFirst) {
            assertEquals(minPrice, firstPrice, "Sản phẩm đầu tiên phải có giá thấp nhất");
        } else {
            assertEquals(maxPrice, firstPrice, "Sản phẩm đầu tiên phải có giá cao nhất");
        }
    }

    @Test
    @Order(5)
    @DisplayName("TC-SORT-BVA3: Kiểm tra boundary - sản phẩm giữa danh sách")
    void testMiddleItemSort() {
        login();

        inventoryPage.selectSort("az");
        List<String> names = inventoryPage.getItemNames();

        int size = names.size();
        logItems("TC-SORT-BVA3 - Sản phẩm giữa danh sách (sort A->Z)");
        if (size >= 3) {
            int middleIndex = size / 2;
            String middleName = names.get(middleIndex);
            String prevName = names.get(middleIndex - 1);
            String nextName = names.get(middleIndex + 1);

            System.out.printf(Locale.US,
                    "  prev[%d]=%s | middle[%d]=%s | next[%d]=%s%n",
                    middleIndex - 1, prevName,
                    middleIndex, middleName,
                    middleIndex + 1, nextName);

            // Kiểm tra sản phẩm giữa thỏa mãn: prev <= middle <= next
            assertTrue(prevName.compareTo(middleName) <= 0,
                    "Tên trước phải <= tên giữa");
            assertTrue(middleName.compareTo(nextName) <= 0,
                    "Tên giữa phải <= tên sau");
        } else {
            System.out.printf(Locale.US,
                    "  Bỏ qua: chỉ có %d sản phẩm, cần >= 3%n", size);
        }
    }

    // ==================== Test Case với MethodSource ====================

    static List<String> sortOptions() {
        return List.of("az", "za", "lohi", "hilo");
    }

    @ParameterizedTest
    @Order(6)
    @MethodSource("sortOptions")
    @DisplayName("TC-SORT-EP-METHOD: Kiểm tra sort với MethodSource")
    void testSortWithMethodSource(String sortOption) {
        login();

        inventoryPage.selectSort(sortOption);
        List<String> names = inventoryPage.getItemNames();

        logItems("TC-SORT-EP-METHOD - Sort option: " + sortOption);

        // Tất cả sort options phải trả về danh sách không rỗng
        assertTrue(names.size() > 0, "Sort " + sortOption + " phải trả về sản phẩm");
    }

    // ==================== Test Default (không sort) ====================

    @Test
    @Order(7)
    @DisplayName("TC-SORT-EP5: Kiểm tra trạng thái mặc định (không sort)")
    void testDefaultSort() {
        login();

        // Không chọn sort - giữ nguyên thứ tự mặc định
        List<String> defaultNames = inventoryPage.getItemNames();

        assertTrue(defaultNames.size() > 0, "Phải có sản phẩm hiển thị");

        // Thứ tự mặc định của Swag Labs là Name A->Z
        List<String> expectedOrder = new ArrayList<>(defaultNames);
        Collections.sort(expectedOrder);

        logItems("TC-SORT-EP5 - Thứ tự mặc định (không chọn sort)");
        System.out.printf(Locale.US, "  Thực tế  : %s%n", defaultNames);
        System.out.printf(Locale.US, "  Mong đợi  : %s%n", expectedOrder);
        assertEquals(expectedOrder, defaultNames,
                "Thứ tự mặc định phải là A->Z");
    }
}
