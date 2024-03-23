

from pay import PayClass
#Transfer money from disbursement account
withdrawmoney = PayClass.withdrawmtnmomo("200", "EUR", "djsjlkjs34123", "237672973390", "Njangi payment completed")

print(withdrawmoney['response'])
print(withdrawmoney['ref'])

