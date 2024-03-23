 

from pay import PayClass

callPay = PayClass.momopay("200", "EUR", "ddoiidio322", "237672973390", "Njadia testing")


if callPay['response'] ==202 or callPay['response']==200:

    verify = PayClass.verifymomo(callPay['ref'])
    print(verify)

else:
    print("THERE WAS A PROBLEM WITH REQUEST PLEASE CAN YOU TRY AGAIN")
    