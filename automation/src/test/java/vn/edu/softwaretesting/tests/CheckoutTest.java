package vn.edu.softwaretesting.tests;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.math.RoundingMode;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

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

    @Test
    @DisplayName("TC-CHK-01: full information moves to checkout overview")
    void fullInformationMovesToOverview() {
        checkout.openWithBackpack(baseUrl)
                .continueWith("An", "Nguyen", "700000")
                .waitForOverview();
        assertTrue(checkout.currentUrl().endsWith("checkout-step-two.html"),
                () -> "TC-CHK-01 got URL: " + checkout.currentUrl());
    }

    @ParameterizedTest(name = "{0}: first=''{1}'', last=''{2}'', postal=''{3}'' -> {4}")
    @DisplayName("TC-CHK-02: missing information shows the expected error")
    @CsvSource({
        "TC-CHK-02.1, '', Nguyen, 700000, Error: First Name is required",
        "TC-CHK-02.2, An, '',     700000, Error: Last Name is required",
        "TC-CHK-02.3, An, Nguyen, '',     Error: Postal Code is required",
        "TC-CHK-02.4, '', '',     '',     Error: First Name is required",
        "TC-CHK-02.5, An, '',     '',     Error: Last Name is required"
    })
    void missingInformationShowsError(String id, String first, String last,
                                      String postal, String expectedError) {
        checkout.openWithBackpack(baseUrl).continueWith(first, last, postal);
        assertAll(
                () -> assertEquals(expectedError, checkout.errorMessage(), id),
                () -> assertTrue(checkout.currentUrl().endsWith("checkout-step-one.html"),
                        () -> id + " should stay on step one, got: " + checkout.currentUrl()));
    }

    @Test
    @DisplayName("TC-CHK-03: cancel on information step returns to cart and keeps the item")
    void cancelInformationStepReturnsToCart() {
        checkout.openWithBackpack(baseUrl).cancelInformationStep();
        assertAll(
                () -> assertTrue(checkout.currentUrl().endsWith("cart.html"),
                        () -> "TC-CHK-03 got URL: " + checkout.currentUrl()),
                () -> assertTrue(checkout.cartContainsBackpack(),
                        "Sauce Labs Backpack should remain in the cart"),
                () -> assertEquals("1", checkout.cartBadgeCount()));
    }

    @Test
    @Tag("known-bug")
    @DisplayName("TC-CHK-01 [BUG-03]: problem_user can fill information and continue")
    void problemUserCanFillInformation() {
        checkout.openWithBackpackAs(baseUrl, "problem_user");
        assertDoesNotThrow(() -> checkout.continueWith("An", "Nguyen", "700000"),
                "BUG-03: Last Name does not keep the typed text for problem_user");
        checkout.waitForOverview();
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
