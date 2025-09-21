/**
 * Playwright E2E Tests for Know Your Rights feature
 * 
 * These tests validate dynamic behavior and ensure responses are not hardcoded.
 * Tests verify that different inputs produce different outputs with proper citations.
 */

import { test, expect } from '@playwright/test';

// Base URL for the application
const BASE_URL = 'http://localhost:5174';

test.describe('Know Your Rights E2E Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the Know Your Rights page
    await page.goto(`${BASE_URL}/know-your-rights`);
    
    // Wait for the page to load
    await expect(page.locator('h1')).toContainText('Know Your Rights');
  });

  test('Dynamic Response Test - Different inputs produce different outputs', async ({ page }) => {
    // Test Input A: Detailed bribe scenario
    const inputA = "A police officer stopped me at MG Road checkpoint on 2025-09-20 at 3 PM and demanded Rs.100 to avoid writing a speeding ticket. He said if I don't pay now, the fine will be Rs.500 and I'll have to go to court.";
    
    // Select bribe scenario
    await page.locator('[data-scenario="bribe"]').click();
    
    // Enter detailed input A
    await page.locator('textarea').fill(inputA);
    
    // Submit the form
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response (up to 2 minutes)
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Capture response A
    const responseA = await page.locator('[data-testid="legal-advice"]').textContent();
    const citationsA = await page.locator('[data-testid="citations"] .citation').count();
    
    // Verify response A has content
    expect(responseA).toBeTruthy();
    expect(responseA.length).toBeGreaterThan(100);
    expect(citationsA).toBeGreaterThan(0);
    
    // Check that response contains unique details from input A
    expect(responseA).toMatch(/MG Road|checkpoint|Rs\.100|100|police/i);
    
    // Reset for second test
    await page.locator('button:has-text("New Query")').click();
    
    // Test Input B: Shorter, different bribe scenario  
    const inputB = "Traffic cop near my office yesterday asked for money to let me go without a fine.";
    
    // Select bribe scenario again
    await page.locator('[data-scenario="bribe"]').click();
    
    // Enter input B
    await page.locator('textarea').fill(inputB);
    
    // Submit the form
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response B
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Capture response B
    const responseB = await page.locator('[data-testid="legal-advice"]').textContent();
    const citationsB = await page.locator('[data-testid="citations"] .citation').count();
    
    // Verify response B has content
    expect(responseB).toBeTruthy();
    expect(responseB.length).toBeGreaterThan(100);
    expect(citationsB).toBeGreaterThan(0);
    
    // CRITICAL: Verify responses are different (not hardcoded)
    expect(responseA).not.toBe(responseB);
    
    // Verify each response contains context from its input
    expect(responseB).toMatch(/office|yesterday|traffic|cop/i);
    
    // Both should contain constitutional/legal terms but with different details
    expect(responseA).toMatch(/Article|Constitution|rights|legal/i);
    expect(responseB).toMatch(/Article|Constitution|rights|legal/i);
  });

  test('Citation Validation Test', async ({ page }) => {
    const testInput = "Government officer demanded Rs.2000 bribe for issuing my birth certificate which should be free according to law.";
    
    // Select bribe scenario
    await page.locator('[data-scenario="bribe"]').click();
    
    // Enter input
    await page.locator('textarea').fill(testInput);
    
    // Submit
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Verify citations section exists
    await expect(page.locator('[data-testid="citations"]')).toBeVisible();
    
    // Check that at least one citation exists
    const citationCount = await page.locator('[data-testid="citations"] .citation').count();
    expect(citationCount).toBeGreaterThan(0);
    
    // Verify citations have proper structure
    const firstCitation = page.locator('[data-testid="citations"] .citation').first();
    await expect(firstCitation).toBeVisible();
    
    // Check citation contains reference text
    const citationText = await firstCitation.textContent();
    expect(citationText).toMatch(/Article|Section|Constitution|IPC|Act/);
  });

  test('Urgency Classification Test', async ({ page }) => {
    // Test emergency scenario
    const emergencyInput = "Someone is threatening to kill me and my family if I don't pay them money. I'm scared for our lives.";
    
    await page.locator('[data-scenario="threat"]').click();
    await page.locator('textarea').fill(emergencyInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="urgency-banner"]')).toBeVisible({ timeout: 120000 });
    
    // Check urgency level
    const urgencyText = await page.locator('[data-testid="urgency-banner"]').textContent();
    expect(urgencyText).toMatch(/Emergency|High Priority/i);
    
    // Verify emergency actions are recommended
    await expect(page.locator('[data-testid="recommended-actions"]')).toBeVisible();
    const actionsText = await page.locator('[data-testid="recommended-actions"]').textContent();
    expect(actionsText).toMatch(/Call Police|Emergency/i);
  });

  test('Disclaimer Presence Test', async ({ page }) => {
    const testInput = "Can you help me understand my rights regarding workplace harassment?";
    
    await page.locator('[data-scenario="workplace"]').click();
    await page.locator('textarea').fill(testInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Verify disclaimer is present and visible
    await expect(page.locator('[data-testid="disclaimer"]')).toBeVisible();
    
    const disclaimerText = await page.locator('[data-testid="disclaimer"]').textContent();
    expect(disclaimerText).toMatch(/not legal advice|consult.*lawyer/i);
  });

  test('Recommended Actions Test', async ({ page }) => {
    const testInput = "My neighbor has been harassing me daily with vulgar comments and blocking my path.";
    
    await page.locator('[data-scenario="harassment"]').click();
    await page.locator('textarea').fill(testInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="recommended-actions"]')).toBeVisible({ timeout: 120000 });
    
    // Check that actions are present
    const actionCount = await page.locator('[data-testid="recommended-actions"] .action-item').count();
    expect(actionCount).toBeGreaterThan(0);
    
    // Verify actions are relevant to harassment
    const actionsText = await page.locator('[data-testid="recommended-actions"]').textContent();
    expect(actionsText).toMatch(/Document|Evidence|Police|Legal/i);
  });

  test('Error Handling Test', async ({ page }) => {
    // Test with very short input (should show validation error)
    await page.locator('[data-scenario="other"]').click();
    await page.locator('textarea').fill('help');
    
    // Submit button should be disabled for short input
    const submitButton = page.locator('button:has-text("Get Rights Guidance")');
    await expect(submitButton).toBeDisabled();
    
    // Test with proper input length
    await page.locator('textarea').fill('I need help understanding my constitutional rights in this situation where I feel my rights are being violated.');
    await expect(submitButton).toBeEnabled();
  });

  test('Scenario Selection Test', async ({ page }) => {
    // Test that different scenarios show different placeholders
    
    // Bribe scenario
    await page.locator('[data-scenario="bribe"]').click();
    const bribePlaceholder = await page.locator('textarea').getAttribute('placeholder');
    expect(bribePlaceholder).toMatch(/bribe|corruption/i);
    
    // Threat scenario
    await page.locator('[data-scenario="threat"]').click();
    const threatPlaceholder = await page.locator('textarea').getAttribute('placeholder');
    expect(threatPlaceholder).toMatch(/threat|intimidation/i);
    
    // Online harassment scenario
    await page.locator('[data-scenario="online_harassment"]').click();
    const onlinePlaceholder = await page.locator('textarea').getAttribute('placeholder');
    expect(onlinePlaceholder).toMatch(/online|cyber|digital/i);
  });

  test('Copy and Download Functionality Test', async ({ page }) => {
    const testInput = "I need legal advice about a situation where my rights may have been violated.";
    
    await page.locator('[data-scenario="other"]').click();
    await page.locator('textarea').fill(testInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Test copy functionality
    await expect(page.locator('button:has-text("Copy Advice")')).toBeVisible();
    
    // Test download functionality
    await expect(page.locator('button:has-text("Evidence Checklist")')).toBeVisible();
    
    // Click download button (we can't easily test the actual download in Playwright without additional setup)
    await page.locator('button:has-text("Evidence Checklist")').click();
  });

  test('Follow-up Questions Test', async ({ page }) => {
    const testInput = "I think someone is stalking me and I'm not sure what to do about it.";
    
    await page.locator('[data-scenario="harassment"]').click();
    await page.locator('textarea').fill(testInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="follow-up-questions"]')).toBeVisible({ timeout: 120000 });
    
    // Check that follow-up questions exist
    const questionCount = await page.locator('[data-testid="follow-up-questions"] li').count();
    expect(questionCount).toBeGreaterThan(0);
    
    // Verify questions are relevant
    const questionsText = await page.locator('[data-testid="follow-up-questions"]').textContent();
    expect(questionsText).toMatch(/evidence|document|report|witness/i);
  });

});

test.describe('Constitution Chat Regression Tests', () => {
  
  test('Constitution Chat still works after Know Your Rights implementation', async ({ page }) => {
    // Navigate to Constitution Chat page
    await page.goto(`${BASE_URL}/constitution`);
    
    // Wait for page to load
    await expect(page.locator('h1')).toContainText('Constitution Chat');
    
    // Test basic constitutional question
    const constitutionQuestion = "What is Article 21 of the Indian Constitution?";
    
    await page.locator('input[placeholder*="Constitution"]').fill(constitutionQuestion);
    await page.locator('button:has-text("Send")').click();
    
    // Wait for response (up to 2 minutes)
    await expect(page.locator('.prose')).toBeVisible({ timeout: 120000 });
    
    // Verify response contains constitutional content
    const responseText = await page.locator('.prose').textContent();
    expect(responseText).toMatch(/Article 21|Right to Life|liberty|Constitution/i);
    
    // Verify citations exist
    await expect(page.locator('[data-testid="citations"], .citations, :has-text("Citations")')).toBeVisible();
  });

});

// Helper function to add test IDs to components (for reference in implementation)
test.describe('Test ID Requirements', () => {
  
  test('Verify required test IDs are present', async ({ page }) => {
    const testInput = "Test input for checking test IDs";
    
    await page.locator('[data-scenario="other"]').click();
    await page.locator('textarea').fill(testInput);
    await page.locator('button:has-text("Get Rights Guidance")').click();
    
    // Wait for response
    await expect(page.locator('[data-testid="legal-advice"]')).toBeVisible({ timeout: 120000 });
    
    // Check all required test IDs exist
    const requiredTestIds = [
      'legal-advice',
      'citations', 
      'recommended-actions',
      'urgency-banner',
      'follow-up-questions',
      'disclaimer'
    ];
    
    for (const testId of requiredTestIds) {
      await expect(page.locator(`[data-testid="${testId}"]`)).toBeVisible();
    }
  });
});