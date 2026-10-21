package vn.edu.softwaretesting.tests;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import vn.edu.softwaretesting.core.WebTestBase;
import vn.edu.softwaretesting.pages.CheckoutPage;

@Tag("web")
@DisplayName("FR-03: Checkout")
class CheckoutTest extends WebTestBase {
    private CheckoutPage checkout;

    @BeforeEach
    void preparePageObject() {
        checkout = new CheckoutPage(driver);
    }

    static Stream<Arguments> requiredInformationCases() {
        return Stream.of(
                Arguments.of("TC-CHK-01", "", "", "", "Error: First Name is required"),
                Arguments.of("TC-CHK-02", "Ada", "", "10101", "Error: Last Name is required"),
                Arguments.of("TC-CHK-03", "Ada", "Lovelace", "", "Error: Postal Code is required")
        );
    }

    @ParameterizedTest(name = "{0}: empty required field shows the expected validation")
    @MethodSource("requiredInformationCases")
    void missingRequiredInformationShowsError(String id, String first, String last,
                                               String postal, String expectedError) {
        checkout.openWithBackpack(baseUrl);
        checkout.continueWith(first, last, postal);
        assertEquals(expectedError, checkout.errorMessage());
    }

    @Test
    @DisplayName("TC-CHK-04: checkout overview displays the correct totals")
    void checkoutOverviewCalculatesTotals() {
        checkout.openWithBackpack(baseUrl);
        checkout.continueWith("An", "Nguyen", "700000").waitForOverview();

        BigDecimal itemTotal = checkout.itemTotal();
        BigDecimal expectedTax = itemTotal.multiply(new BigDecimal("0.08"))
                .setScale(2, RoundingMode.HALF_UP);
        BigDecimal expectedTotal = itemTotal.add(expectedTax).setScale(2, RoundingMode.HALF_UP);
        assertEquals(0, new BigDecimal("29.99").compareTo(itemTotal));
        assertEquals(0, expectedTax.compareTo(checkout.tax()));
        assertEquals(0, expectedTotal.compareTo(checkout.total()));
        assertTrue(checkout.currentUrl().contains("checkout-step-two.html"));
    }

    @Test
    @DisplayName("TC-CHK-05: Finish completes the order and clears the cart")
    void finishCompletesOrderAndClearsCart() {
        checkout.openWithBackpack(baseUrl);
        checkout.continueWith("An", "Nguyen", "700000")
                .waitForOverview()
                .finishOrder();
        assertEquals("Thank you for your order!", checkout.confirmationMessage());
        assertTrue(checkout.cartBadgeIsHidden(), "Cart badge should be hidden after order completion");
    }

    @Test
    @DisplayName("TC-CHK-06: cancel from overview returns to inventory and preserves the item")
    void cancelFromOverviewReturnsToInventory() {
        checkout.openWithBackpack(baseUrl);
        checkout.continueWith("An", "Nguyen", "700000")
                .waitForOverview()
                .cancelOverview();
        assertTrue(checkout.currentUrl().endsWith("inventory.html"),
                "Cancel should return to inventory.html");
        assertEquals("1", checkout.cartBadgeCount(),
                "The backpack should remain in the cart after cancelling checkout");
    }

    @Test
    @DisplayName("TC-CHK-07: two-item checkout calculates totals and completes the order")
    void twoItemCheckoutCalculatesTotalsAndCompletesOrder() {
        checkout.openWithBackpackAndBikeLight(baseUrl)
                .continueWith("An", "Nguyen", "700000")
                .waitForOverview();

        BigDecimal itemTotal = checkout.itemTotal();
        assertEquals(0, new BigDecimal("39.98").compareTo(itemTotal));
        assertEquals(0, new BigDecimal("3.20").compareTo(checkout.tax()));
        assertEquals(0, new BigDecimal("43.18").compareTo(checkout.total()));

        checkout.finishOrder();
        assertEquals("Thank you for your order!", checkout.confirmationMessage());
        assertTrue(checkout.cartBadgeIsHidden(), "Cart badge should be hidden after order completion");
    }
}
