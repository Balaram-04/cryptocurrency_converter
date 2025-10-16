// static/converter/js/app.js
document.addEventListener('DOMContentLoaded', function(){
  const form = document.getElementById('convertForm');
  const result = document.getElementById('result');
  const historyDiv = document.getElementById('history');

  async function postConvert(payload) {
    const resp = await fetch('/api/convert/', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'},
      body: new URLSearchParams(payload)
    });
    return resp.json();
  }

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const from_currency = document.getElementById('from_currency').value.trim();
    const to_currency = document.getElementById('to_currency').value.trim();
    const amount = document.getElementById('amount').value;

    result.textContent = 'Converting...';
    try {
      const data = await postConvert({from_currency, to_currency, amount});
      if (data.error) {
        result.innerHTML = '<b>Error:</b> ' + (data.error || JSON.stringify(data));
        return;
      }
      result.innerHTML = `<strong>${data.from_amount} ${data.from_currency}</strong> = <strong>${data.to_amount}</strong> ${data.to_currency} <br> Rate: ${data.rate}`;
      // append to history
      const item = document.createElement('div');
      item.textContent = `${new Date().toLocaleString()} — ${data.from_amount} ${data.from_currency} → ${data.to_amount.toFixed(6)} ${data.to_currency}`;
      historyDiv.prepend(item);
    } catch (err) {
      result.textContent = 'Network error';
    }
  });
});
