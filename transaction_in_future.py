from algosdk.v2client import algod
from algosdk import mnemonic, transaction
import datetime as dt

algod_token = 'YOUR API KEY HERE'
algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
headers = {'X-Api-key': algod_token}

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token,algod_address=algod_address, headers=headers)

# For demonstration purposes only. NEVER share mnemonics in real world use case
payment_receiver_mn = "PASTE mnemonic for payment receiver"
payer_mn = "PASTE mnemonic for payment receiver"

payment_receiver = {'pk':mnemonic.to_public_key(payment_receiver_mn),
                    'sk':mnemonic.to_private_key(payment_receiver_mn)}
payer = {'pk':mnemonic.to_public_key(payer_mn),
         'sk':mnemonic.to_private_key(payer_mn)}

#Current Round
current_round = algod_client.status().get('last-round')
# average block time
average_block_time = 4.5
#Target_Submission_Times
target_submission_rounds = []


today = dt.date.today()
payments = 12
for months in range(1,payments-1):
    payment_date = (today+dt.timedelta(days=30*months)).replace(day=1)
    #target round : current round + (seconds from now / average block time)
    target_round = int(current_round + ((payment_date - today).total_seconds() / average_block_time))

    first_valid_round = target_round
    last_valid_round = target_round + 1000
    print(f'{payment_date} payement submission round  is {target_round:.{0}f} ')


# for Demo purpose try to send trx ahead of time, it will fail because out of validity interval
params = algod_client.suggested_params()
gh = params.gh
fee = params.min_fee
send_amount = 10

for months in range(1,13):
    payment_date = (today+dt.timedelta(days=30*months)).replace(day=1)
    target_round = int(current_round + ((payment_date - today).total_seconds() / average_block_time))
    first_valid_round = target_round
    last_valid_round = target_round + 1000
    tx = transaction.PaymentTxn(payer['pk'], fee, first_valid_round, last_valid_round, gh, payment_receiver['pk'],send_amount,flat_fee=True)
    try:
        signed_tx = tx.sign(payer['sk'])
        tx_confirm = algod_client.send_transaction(signed_tx)
    except Exception as e:
        print(e)
        #algosdk.error.AlgodHTTPError: {"message":"TransactionPool.Remember: txn dead: round 14305815 outside of 14497814--14498814"}
    print(f'{payment_date} payement will be submitted at round {target_round:.{0}f}  with Transaction ID {signed_tx.transaction.get_txid()}')
    


first_valid_round = current_round
last_valid_round = current_round + 1000
tx = transaction.PaymentTxn(payer['pk'], fee, first_valid_round, last_valid_round, gh, payment_receiver['pk'],send_amount,flat_fee=True)
signed_tx = tx.sign(payer['sk'])
tx_confirm = algod_client.send_transaction(signed_tx)
print(tx_confirm)
