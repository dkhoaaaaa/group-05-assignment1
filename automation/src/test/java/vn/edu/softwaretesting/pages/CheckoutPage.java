package vn.edu.softwaretesting.pages;

import java.math.BigDecimal;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import vn.edu.softwaretesting.pages.LoginPage.LoginResult;

/** Page Object for the SauceDemo checkout flow, including its prerequisites. */
public final class CheckoutPage {
    private static final By ADD_BACKPACK = By.id("add-to-cart-sauce-labs-backpack");
    private static final By ADD_BIKE_LIGHT = By.id("add-to-cart-sauce-labs-bike-light");
    private static final By CART_LINK = By.className("shopping_cart_link");
    private static final By CHECKOUT_BUTTON = By.id("checkout");
    private static final By FIRST_NAME = By.id("first-name");
    private static final By LAST_NAME = By.id("last-name");
    private static final By POSTAL_CODE = By.id("postal-code");
    private static final By CONTINUE_BUTTON = By.id("continue");
    private static final By CANCEL_BUTTON = By.id("cancel");
    private static final By ERROR = By.cssSelector("[data-test='error']");
    private static final By SUBTOTAL = By.xpath("//*[starts-with(normalize-space(text()), 'Item total:')]");
    private static final By TAX = By.xpath("//*[starts-with(normalize-space(text()), 'Tax:')]");
    private static final By TOTAL = By.xpath("//*[starts-with(normalize-space(text()), 'Total:')]");
    private static final By FINISH_BUTTON = By.id("finish");
    private static final By COMPLETE_HEADER = By.xpath("//*[normalize-space(.)='Thank you for your order!']");
    private static final By CART_BADGE = By.className("shopping_cart_badge");
    private static final By CART_ITEM_NAMES = By.cssSelector(".cart_item .inventory_item_name");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public CheckoutPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    /** Log in and create a one-item cart so each checkout test starts independently. */
    public CheckoutPage openWithBackpack(String baseUrl) {
        return openWithItems(baseUrl, false);
    }

    /** Log in and create a two-item cart for checkout total coverage. */
    public CheckoutPage openWithBackpackAndBikeLight(String baseUrl) {
        return openWithItems(baseUrl, true);
    }

    private CheckoutPage openWithItems(String baseUrl, boolean includeBikeLight) {
        LoginResult login = new LoginPage(driver, baseUrl).open()
                .login("standard_user", "secret_sauce");
        if (!login.accepted()) {
            throw new IllegalStateException("Could not sign in for checkout: " + login.message());
        }
        wait.until(ExpectedConditions.elementToBeClickable(ADD_BACKPACK)).click();
        if (includeBikeLight) {
            wait.until(ExpectedConditions.elementToBeClickable(ADD_BIKE_LIGHT)).click();
        }
        wait.until(ExpectedConditions.elementToBeClickable(CART_LINK)).click();
        wait.until(ExpectedConditions.elementToBeClickable(CHECKOUT_BUTTON)).click();
        try {
            wait.until(ExpectedConditions.visibilityOfElementLocated(FIRST_NAME));
        } catch (TimeoutException exception) {
            String pageText = driver.findElement(By.tagName("body")).getText();
            Path screenshot = Path.of("target", "checkout-setup-timeout.png");
            try {
                Files.createDirectories(screenshot.getParent());
                Files.write(screenshot, ((TakesScreenshot) driver)
                        .getScreenshotAs(OutputType.BYTES));
            } catch (IOException ignored) {
                // Keep the URL and page text diagnostic if screenshot capture fails.
            }
            throw new AssertionError("Could not open the checkout information form. Current URL: "
                    + driver.getCurrentUrl() + "; page text: " + pageText
                    + "; screenshot: target/checkout-setup-timeout.png", exception);
        }
        return this;
    }

    public CheckoutPage continueWith(String firstName, String lastName, String postalCode) {
        replaceText(FIRST_NAME, firstName);
        replaceText(LAST_NAME, lastName);
        replaceText(POSTAL_CODE, postalCode);
        driver.findElement(CONTINUE_BUTTON).click();
        return this;
    }

    public String errorMessage() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(ERROR)).getText();
    }

    public CheckoutPage cancelInformationStep() {
        wait.until(ExpectedConditions.elementToBeClickable(CANCEL_BUTTON)).click();
        return this;
    }

    public CheckoutPage cancelOverview() {
        wait.until(ExpectedConditions.elementToBeClickable(CANCEL_BUTTON)).click();
        wait.until(ExpectedConditions.urlContains("inventory.html"));
        return this;
    }

    public CheckoutPage waitForOverview() {
        try {
            wait.until(ExpectedConditions.urlContains("checkout-step-two.html"));
        } catch (TimeoutException exception) {
            String pageText = driver.findElement(By.tagName("body")).getText();
            Path screenshot = Path.of("target", "checkout-overview-timeout.png");
            try {
                Files.createDirectories(screenshot.getParent());
                Files.write(screenshot, ((TakesScreenshot) driver)
                        .getScreenshotAs(OutputType.BYTES));
            } catch (IOException ignored) {
                // Keep the original navigation diagnostic if screenshot capture fails.
            }
            throw new AssertionError("Continue did not leave the information page. Current URL: "
                    + driver.getCurrentUrl() + "; page text: " + pageText
                    + "; screenshot: target/checkout-overview-timeout.png", exception);
        }
        wait.until(ExpectedConditions.visibilityOfElementLocated(SUBTOTAL));
        return this;
    }

    public BigDecimal itemTotal() { return moneyFrom(SUBTOTAL); }
    public BigDecimal tax() { return moneyFrom(TAX); }
    public BigDecimal total() { return moneyFrom(TOTAL); }

    public CheckoutPage finishOrder() {
        wait.until(ExpectedConditions.elementToBeClickable(FINISH_BUTTON)).click();
        try {
            wait.until(ExpectedConditions.urlContains("checkout-complete.html"));
        } catch (TimeoutException exception) {
            String pageText = driver.findElement(By.tagName("body")).getText();
            Path screenshot = Path.of("target", "checkout-finish-timeout.png");
            try {
                Files.createDirectories(screenshot.getParent());
                Files.write(screenshot, ((TakesScreenshot) driver)
                        .getScreenshotAs(OutputType.BYTES));
            } catch (IOException ignored) {
                // Keep the original navigation diagnostic if screenshot capture fails.
            }
            throw new AssertionError("Finish did not leave the overview page. Current URL: "
                    + driver.getCurrentUrl() + "; page text: " + pageText
                    + "; screenshot: target/checkout-finish-timeout.png", exception);
        }
        wait.until(ExpectedConditions.visibilityOfElementLocated(COMPLETE_HEADER));
        return this;
    }

    public String confirmationMessage() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(COMPLETE_HEADER)).getText();
    }

    public boolean cartBadgeIsHidden() {
        return driver.findElements(CART_BADGE).isEmpty();
    }

    public String cartBadgeCount() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(CART_BADGE)).getText();
    }

    public boolean cartContainsBackpack() {
        return driver.findElements(CART_ITEM_NAMES).stream()
                .anyMatch(item -> item.getText().equals("Sauce Labs Backpack"));
    }

    public String currentUrl() { return driver.getCurrentUrl(); }

    private void replaceText(By locator, String value) {
        var input = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        input.clear();
        if (!value.isEmpty()) {
            input.sendKeys(value);
        }
        wait.until(ExpectedConditions.attributeToBe(locator, "value", value));
    }

    private BigDecimal moneyFrom(By locator) {
        String text = wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText();
        String amount = text.replaceAll("[^0-9.]", "");
        return new BigDecimal(amount);
    }
}
