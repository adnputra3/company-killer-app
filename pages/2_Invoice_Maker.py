import streamlit as st
from datetime import date

st.set_page_config(page_title="Invoice Maker", page_icon="🧾", layout="wide")
st.title("🧾 Invoice Maker")

seller_name = st.text_input("Your Business Name", "Acme Studio")
seller_email = st.text_input("Your Email", "hello@acme.com")
client_name = st.text_input("Client Name", "Client Co.")
invoice_no = st.text_input("Invoice Number", "INV-001")
invoice_date = st.date_input("Invoice Date", value=date.today())

qty = st.number_input("Qty", min_value=1, value=1)
unit_price = st.number_input("Unit Price", min_value=0.0, value=500.0)
tax_rate = st.number_input("Tax (%)", min_value=0.0, value=11.0)

subtotal = qty * unit_price
tax = subtotal * (tax_rate / 100.0)
total = subtotal + tax

st.write(f"Subtotal: **${subtotal:,.2f}**")
st.write(f"Tax ({tax_rate:.1f}%): **${tax:,.2f}**")
st.write(f"Total: **${total:,.2f}**")

invoice_text = f"INVOICE\nInvoice No: {invoice_no}\nDate: {invoice_date}\nFrom: {seller_name} ({seller_email})\nTo: {client_name}\nQty: {qty}\nUnit Price: ${unit_price:,.2f}\nSubtotal: ${subtotal:,.2f}\nTax: ${tax:,.2f}\nTOTAL: ${total:,.2f}\n"
st.download_button("⬇️ Download Invoice (TXT)", data=invoice_text, file_name=f"{invoice_no}.txt", mime="text/plain")
