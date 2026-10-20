package vn.edu.softwaretesting.tests;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import vn.edu.softwaretesting.core.WebTestBase;
import vn.edu.softwaretesting.pages.InventoryPage;
import vn.edu.softwaretesting.pages.LoginPage;

/**
 * Test cases cho NFR-01: Hiệu năng
 * Thời gian load trang inventory <= 3 giây (trung vị 5 lần đo)
 */
public class PerformanceTest extends WebTestBase {

    private static final double THRESHOLD_SECONDS = 3.0;
    private static final int MEASUREMENT_COUNT = 5;

    private LoginPage loginPage;
    private InventoryPage inventoryPage;

    @BeforeEach
    void initPages() {
        loginPage = new LoginPage(driver, baseUrl);
        inventoryPage = new InventoryPage(driver);
    }

    @Test
    @DisplayName("TC-NFR-01: Đo thời gian load trang inventory (performance_glitch_user)")
    @Timeout(60)
    void testInventoryPageLoadTime() {
        List<Double> loadTimes = new ArrayList<>();

        for (int i = 1; i <= MEASUREMENT_COUNT; i++) {
            // Đăng nhập với performance_glitch_user (user có bug load chậm)
            loginPage.open();
            Instant start = Instant.now();
            LoginPage.LoginResult result = loginPage.login("performance_glitch_user", "secret_sauce");
            Instant end = Instant.now();

            // Chỉ đo nếu login thành công
            if (result.accepted()) {
                // Đo thời gian load trang inventory
                Instant pageStart = Instant.now();
                inventoryPage.open();
                inventoryPage.waitForPageLoaded();
                Instant pageEnd = Instant.now();

                Duration pageLoadDuration = Duration.between(pageStart, pageEnd);
                double loadTimeSeconds = pageLoadDuration.toMillis() / 1000.0;
                loadTimes.add(loadTimeSeconds);

                System.out.printf("Lần đo %d: %.3f giây%n", i, loadTimeSeconds);
            }

            // Đóng trình duyệt và mở lại cho lần đo tiếp theo
            driver.quit();
            openBrowser();
            loginPage = new LoginPage(driver, baseUrl);
            inventoryPage = new InventoryPage(driver);
        }

        // Tính trung vị (median)
        Collections.sort(loadTimes);
        double median;
        int size = loadTimes.size();
        if (size % 2 == 0) {
            median = (loadTimes.get(size / 2 - 1) + loadTimes.get(size / 2)) / 2.0;
        } else {
            median = loadTimes.get(size / 2);
        }

        System.out.printf("%n=== KẾT QUẢ ĐO HIỆU NĂNG ===%n");
        System.out.printf("Số lần đo: %d%n", size);
        System.out.printf("Thời gian các lần đo: %s%n", loadTimes);
        System.out.printf("Trung vị: %.3f giây%n", median);
        System.out.printf("Ngưỡng yêu cầu: %.1f giây%n", THRESHOLD_SECONDS);
        System.out.printf("Kết quả: %s%n",
                median <= THRESHOLD_SECONDS ? "PASS [PASS]" : "FAIL [FAIL]");

        // Test sẽ FAIL vì performance_glitch_user có bug load chậm
        // Bug: BUG-01 - Trung vị thời gian load > 3 giây
        assertTrue(median <= THRESHOLD_SECONDS,
                String.format("Trung vị thời gian load phải <= %.1f giây (thực tế: %.3f giây)",
                        THRESHOLD_SECONDS, median));
    }

    @Test
    @DisplayName("TC-NFR-01-BASELINE: Đo baseline với standard_user (để so sánh)")
    @Timeout(30)
    void testInventoryPageLoadTimeBaseline() {
        // Đăng nhập với standard_user (user bình thường)
        loginPage.open();
        loginPage.login("standard_user", "secret_sauce");

        // Đo thời gian load trang inventory
        Instant start = Instant.now();
        inventoryPage.open();
        inventoryPage.waitForPageLoaded();
        Instant end = Instant.now();

        Duration loadDuration = Duration.between(start, end);
        double loadTimeSeconds = loadDuration.toMillis() / 1000.0;

        System.out.printf("Baseline (standard_user): %.3f giây%n", loadTimeSeconds);

        // Baseline thường < 3 giây
        assertTrue(loadTimeSeconds <= THRESHOLD_SECONDS,
                "Baseline với standard_user phải <= 3 giây");
    }
}
