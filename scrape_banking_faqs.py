import requests
from bs4 import BeautifulSoup
import os
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

ICICI_URLS = {
    "Accounts": {
        "Savings Account": "https://www.icicibank.com/personal-banking/accounts/savings-account?ITM=nli_savingsAccount_accountssavingsAccountna_megamenuContainer_0_CMS_savingsAccount_NLI",
        "Salary Account": "https://www.icicibank.com/personal-banking/accounts/salary-account?ITM=nli_savingsAccount_accountssavingsAccountna_megamenuContainer_1_CMS_salaryAccount_NLI"
    },
    "Deposits": {
        "Overview": "https://www.icicibank.com/personal-banking/deposits?ITM=nli_cms_deposits_header_nav",
        "Fixed Deposit": "https://www.icicibank.com/personal-banking/deposits/fixed-deposit?ITM=nli_cms_deposits_main_nav",
        "Recurring Deposit": "https://www.icicibank.com/personal-banking/deposits/recurring-deposits?ITM=nli_cms_deposits_main_nav",
        "iWish Goal-Based Saving": "https://www.icicibank.com/personal-banking/deposits/iwish?ITM=nli_cms_deposits_main_nav"
    },
    "Payments": {
        "Fund Transfer": "https://www.icicibank.com/personal-banking/online-services/funds-transfer?ITM=nli_deposits_deposits_megamenuItem_1_CMS_payments_moneyTransfer_NLI",
        "Overdue Loan Payment": "https://www.icicibank.com/online-services/clicktopayloan?ITM=nli_deposits_deposits_megamenuItem_2_CMS_payments_overdueLoanPayment_NLI",
        "Credit Card Bill Payment": "https://www.icicibank.com/online-services/clicktopay?ITM=nli_deposits_deposits_megamenuItem_3_CMS_payments_creditCardBillPayment_NLI",
        "Tax Payment": "https://www.icicibank.com/personal-banking/online-services/online-tax-payment?ITM=nli_deposits_deposits_megamenuItem_4_CMS_payments_taxPayment_NLI",
        "Bill Payments & Recharges": "https://www.icicibank.com/personal-banking/bill-payment?ITM=nli_deposits_deposits_megamenuItem_5_CMS_payments_billPaymentsRecharges_NLI",
        "Contactless Payments": "https://www.icicibank.com/personal-banking/cards/debit-card/contactless-mobile-payments?ITM=nli_deposits_deposits_megamenuItem_6_CMS_payments_contactlessPayments_NLI",
        "Digital Rupee": "https://www.icicibank.com/personal-banking/online-services/funds-transfer/digital-rupee?ITM=nli_deposits_deposits_megamenuItem_7_CMS_payments_eWallet_NLI",
        "FASTag": "https://www.icicibank.com/personal-banking/cards/prepaid-card/fastag?ITM=nli_deposits_deposits_megamenuItem_8_CMS_payments_fasttag_NLI",
        "UPI": "https://www.icicibank.com/upi?ITM=nli_deposits_deposits_megamenuItem_2_CMS_payments_upi_NLI",
        "Forex Services": "https://www.icicibank.com/online-services/forex?ITM=nli_deposits_deposits_megamenuItem_3_CMS_payments_forexServices_NLI"
    },
    "Cards": {
        "Times Black Credit Card": "https://www.icicibank.com/personal-banking/cards/credit-card/times-black-icici-credit-card?ITM=nli_creditCard_cards_creditCard_productHighlight_1CTA_CMS_details_NLI"
    },
    "Loans": {
        "Personal Loan": "https://www.icicibank.com/personal-banking/loans/personal-loan?ITM=nli_timesBlackIciciCreditCard_cards_creditCard_timesBlackIciciCreditCard_megamenuItem_1_CMS_loans_personalLoan_NLI",
        "Home Loan": "https://www.icicibank.com/personal-banking/loans/home-loan?ITM=nli_timesBlackIciciCreditCard_cards_creditCard_timesBlackIciciCreditCard_megamenuItem_2_CMS_loans_homeLoan_NLI",
        "Car Loan": "https://www.icicibank.com/personal-banking/loans/car-loan?ITM=nli_timesBlackIciciCreditCard_cards_creditCard_timesBlackIciciCreditCard_megamenuItem_3_CMS_loans_carLoan_NLI",
        "Education Loan": "https://www.icicibank.com/personal-banking/loans/education-loan?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_4_CMS_loans_educationLoan_NLI",
        "Loan Against Securities": "https://www.icicibank.com/personal-banking/loans/loan-against-securities?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_5_CMS_loans_loansAgainstSecurities_NLI",
        "Loan Against Shares": "https://www.icicibank.com/in/en/personal-banking/loans/loan-against-securities/loan-against-shares?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_6_CMS_loans_loanAgainstShares_NLI",
        "Loan Against Mutual Funds": "https://www.icicibank.com/personal-banking/loans/loan-against-securities/mutual-funds?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_7_CMS_loans_loanAgainstMutualFunds_NLI",
        "Loan Against Property": "https://www.icicibank.com/personal-banking/loans/home-loan/loan-against-property?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_8_CMS_loans_loanAgainstProperty_NLI",
        "EMI Calculator": "https://www.icicibank.com/personal-banking/loans/personal-loan/emi-calculator?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_1_CMS_loans_personalLoanEmiCalculator_NLI"
    },
    "Investments": {
        "Mutual Funds": "https://www.icicibank.com/personal-banking/investments/mutual-funds?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_1_CMS_investments_mutualFunds_NLI",
        "3-in-1 Account": "https://www.icicibank.com/personal-banking/investments/three-in-one-account?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_2_CMS_investments_3In1AccountInvestInStocks_NLI",
        "Demat Account": "https://www.icicibank.com/personal-banking/investments/open-demat-account?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_3_CMS_investments_dematAccount_NLI",
        "National Pension System (NPS)": "https://www.icicibank.com/personal-banking/investments/government-schemes/nps-national-pension-system?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_4_CMS_investments_nationalPensionSystem_NLI",
        "Public Provident Fund (PPF)": "https://www.icicibank.com/personal-banking/investments/ppf?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_5_CMS_investments_publicProvidentFund_NLI",
        "Government Schemes": "https://www.icicibank.com/personal-banking/investments/government-schemes?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_6_CMS_investments_governmentSchemes_NLI",
        "Personal Finance Management": "https://www.icicibank.com/personal-banking/online-services/personal-finance-management?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_7_CMS_investments_managePersonalFinance_NLI",
        "SIP Calculator": "https://www.icicibank.com/calculator/sip-calculator?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_1_CMS_investments_sipCalculator_NLI",
        "Lumpsum Calculator": "https://www.icicibank.com/personal-banking/investments/mutual-funds/lumpsum-calculator?ITM=nli_educationLoan_loans_educationLoan_megamenuItem_2_CMS_investments_lumpsumCalculator_NLI"
    }
}

SAVE_DIR = "scraped_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def scrape_and_save(category, subcategory, url):
    try:
        print(f"Scraping [{category}] - {subcategory}...")
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        text = soup.get_text(separator="\n")
        cleaned = "\n".join([clean_text(line) for line in text.splitlines() if line.strip()])
        filename = f"{category.lower().replace(' ', '_')}_{subcategory.lower().replace(' ', '_')}.txt"
        with open(os.path.join(SAVE_DIR, filename), "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Error scraping [{category}] - {subcategory}: {e}")

if __name__ == "__main__":
    for category, subdict in ICICI_URLS.items():
        for subcategory, url in subdict.items():
            scrape_and_save(category, subcategory, url)
