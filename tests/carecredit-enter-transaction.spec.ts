import { expect, Page, test } from '@playwright/test';

const ENTRY_URL =
  'https://www.carecreditprovidercenter.com/BC_CC_Demo/cc-htmls/enter-a-transaction.html';

const transactionTypes = [
  'Purchase',
  'Refund',
  'Authorization Only',
  'Forced Purchase',
] as const;

async function openEnterTransaction(page: Page) {
  await page.goto(ENTRY_URL, { waitUntil: 'domcontentloaded' });
  await expect(
    page.getByRole('heading', { name: /Process a Transaction/i }),
  ).toBeVisible();
}

async function selectTransactionType(page: Page, transactionType: string) {
  const radio = page.getByRole('radio', { name: transactionType });
  if ((await radio.count()) > 0) {
    await radio.check();
    return;
  }

  const labelledInput = page.getByLabel(transactionType, { exact: true });
  if ((await labelledInput.count()) > 0) {
    await labelledInput.check({ force: true });
    return;
  }

  await page.getByText(new RegExp(`^${escapeRegExp(transactionType)}$`)).click();
}

async function continueTransaction(page: Page, transactionType: string) {
  await selectTransactionType(page, transactionType);

  await Promise.all([
    page.waitForURL((url) => !url.toString().includes('enter-a-transaction'), {
      timeout: 15000,
    }),
    page.getByRole('button', { name: /continue/i }).click(),
  ]);

  await expect(
    page.getByRole('heading', { name: /Process Transaction/i }),
  ).toBeVisible();
  await expect(page.getByText(new RegExp(`^${escapeRegExp(transactionType)}$`)).first()).toBeVisible();
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test.describe('CareCredit enter a transaction', () => {
  test('shows all available transaction types', async ({ page }) => {
    await openEnterTransaction(page);

    for (const transactionType of transactionTypes) {
      await expect(page.getByText(new RegExp(`^${escapeRegExp(transactionType)}$`))).toBeVisible();
    }

    await expect(
      page.getByRole('button', { name: /cancel transaction/i }),
    ).toBeVisible();
    await expect(page.getByRole('button', { name: /continue/i })).toBeVisible();
  });

  test('opens and closes cancel confirmation', async ({ page }) => {
    await openEnterTransaction(page);

    await page.getByRole('button', { name: /cancel transaction/i }).click();
    await expect(
      page.getByRole('heading', { name: /Confirm Cancellation/i }),
    ).toBeVisible();
    await expect(
      page.getByText(/Any changes you have made will be lost\./i),
    ).toBeVisible();

    await page.getByRole('button', { name: /No, Go Back/i }).click();
    await expect(
      page.getByRole('heading', { name: /Confirm Cancellation/i }),
    ).not.toBeVisible();
  });

  test('navigates to the purchase transaction flow', async ({ page }) => {
    await openEnterTransaction(page);
    await continueTransaction(page, 'Purchase');
    await expect(page).toHaveURL(/transaction-purchase/i);
  });

  test('navigates to the refund transaction flow', async ({ page }) => {
    await openEnterTransaction(page);
    await continueTransaction(page, 'Refund');
    await expect(page).toHaveURL(/transaction-revolving-refund/i);
    await expect(page.getByText(/Recent Transactions/i).first()).toBeVisible();
  });

  test('navigates to the authorization only flow', async ({ page }) => {
    await openEnterTransaction(page);
    await continueTransaction(page, 'Authorization Only');
  });

  test('navigates to the forced purchase flow', async ({ page }) => {
    await openEnterTransaction(page);
    await continueTransaction(page, 'Forced Purchase');
  });
});
