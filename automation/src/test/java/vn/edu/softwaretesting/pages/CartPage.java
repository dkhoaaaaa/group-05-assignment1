package vn.edu.softwaretesting.pages;

import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public final class CartPage {

    private static final By CART_BADGE =
            By.cssSelector(".shopping_cart_badge");
    private static final By CART_ITEMS =
            By.cssSelector(".cart_item .inventory_item_name");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public CartPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector(".cart_list")));
    }

    public CartPage removeProduct(String productSlug) {
        By removeButton = By.cssSelector(
                "[data-test='remove-" + productSlug + "']");
        driver.findElement(removeButton).click();
        wait.until(ExpectedConditions.invisibilityOfElementLocated(removeButton));
        return this;
    }

    public List<String> getProductNames() {
        return driver.findElements(CART_ITEMS).stream()
                .map(item -> item.getText())
                .toList();
    }

    public String getCartBadgeCount() {
        return wait.until(
                ExpectedConditions.visibilityOfElementLocated(CART_BADGE))
                .getText();
    }

    public boolean isCartBadgeDisplayed() {
        return !driver.findElements(CART_BADGE).isEmpty()
                && driver.findElement(CART_BADGE).isDisplayed();
    }

    public CartPage waitForCartBadgeCount(String expectedCount) {
        wait.until(ExpectedConditions.textToBe(CART_BADGE, expectedCount));
        return this;
    }

    public CartPage waitForCartBadgeToDisappear() {
        wait.until(ExpectedConditions.invisibilityOfElementLocated(CART_BADGE));
        return this;
    }
}
