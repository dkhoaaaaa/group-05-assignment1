package vn.edu.softwaretesting.pages;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public final class CheckoutPage {

    private static final By FIRST_NAME = By.id("first-name");
    private static final By LAST_NAME = By.id("last-name");
    private static final By POSTAL_CODE = By.id("postal-code");
    private static final By CONTINUE = By.id("continue");
    private static final By CANCEL = By.id("cancel");
    private static final By ERROR = By.cssSelector("[data-test='error']");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public CheckoutPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(8));
    }

    public CheckoutPage fillInformation(String firstName, String lastName,
                                        String postalCode) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(FIRST_NAME))
                .sendKeys(firstName);
        driver.findElement(LAST_NAME).sendKeys(lastName);
        driver.findElement(POSTAL_CODE).sendKeys(postalCode);
        return this;
    }

    public String continueExpectingError() {
        driver.findElement(CONTINUE).click();
        return wait.until(ExpectedConditions.visibilityOfElementLocated(ERROR))
                .getText();
    }

    public String continueToOverview() {
        driver.findElement(CONTINUE).click();
        wait.until(ExpectedConditions.or(
                ExpectedConditions.urlContains("checkout-step-two.html"),
                ExpectedConditions.visibilityOfElementLocated(ERROR)));
        return driver.getCurrentUrl();
    }

    public String cancel() {
        wait.until(ExpectedConditions.elementToBeClickable(CANCEL)).click();
        wait.until(ExpectedConditions.urlContains("cart.html"));
        return driver.getCurrentUrl();
    }
}