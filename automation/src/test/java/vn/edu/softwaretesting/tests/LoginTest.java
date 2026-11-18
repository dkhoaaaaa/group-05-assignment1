package vn.edu.softwaretesting.tests;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import vn.edu.softwaretesting.core.WebTestBase;
import vn.edu.softwaretesting.pages.LoginPage;
import vn.edu.softwaretesting.pages.LoginPage.LoginResult;

@Tag("web")
@DisplayName("FR-LOGIN: Authentication")
class LoginTest extends WebTestBase {

    private LoginPage loginPage;

    @BeforeEach
    void openLoginPage() {
        loginPage = new LoginPage(driver, baseUrl).open();
    }

    @ParameterizedTest(name = "{0}: user=''{1}'', accepted={3}")
    @DisplayName("TC-LOGIN-DT: Kiểm thử đăng nhập theo bảng quyết định")
    @CsvFileSource(resources = "/login-data.csv", numLinesToSkip = 1)
    void loginDecisionTableTests(
            String testCaseId,
            String username,
            String password,
            boolean expectedAccepted,
            String expectedEvidence) {

        LoginResult actual = loginPage.login(username == null ? "" : username, password == null ? "" : password);

        assertEquals(expectedAccepted, actual.accepted(),
                () -> testCaseId + ": Kết quả accepted không khớp cho user: " + username);
        assertTrue(
                actual.currentUrl().contains(expectedEvidence)
                        || actual.message().contains(expectedEvidence),
                () -> testCaseId + ": Không tìm thấy expected evidence '" + expectedEvidence
                        + "'. Thực tế: URL=" + actual.currentUrl() + ", Message=" + actual.message());
    }
}
