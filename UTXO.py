import uuid
import random
import time

# UTXOクラス
class UTXO:
  def __init__(self, txid, index, amount, owner):
    self.txid = txid # Tx ID
    self.index = index #Output Index
    self.amount = amount # Amount
    self.owner = owner # Owner

# トランザクションを生成する関数
def create_transaction(utxos, sender, recipient, amount, gas_fee):
  print(f"\nCreating transaction from {sender} to {recipient} for {amount} coins.")
  input_utxos = []
  total_input = 0

  #UTXOを選択
  for utxo in utxos:
    if utxo.owner == sender:
      input_utxos.append(utxo)
      total_input += utxo.amount
      if total_input >= amount + gas_fee:
        break

  # 残高が足りない場合
  if total_input < amount + gas_fee:
    print(f"Insufficient balance for {sender}.")
    return None, utxos

  #トランザクションの出力を作成
  new_txid = str(uuid.uuid4())
  outputs =[
      UTXO(new_txid, 0, amount, recipient) #受取人のUTXO
  ]
  if total_input > amount + gas_fee:
    outputs.append(UTXO(new_txid, 1, total_input - (amount + gas_fee), sender)) # お釣りのUTXO

  # ガス代を収集
  miner = "Miner" # マイナー
  outputs.append(UTXO(new_txid, 2, gas_fee, miner)) # ガス代をマイナーに送付

  # UTXOリストを更新
  utxos = [utxo for utxo in utxos if utxo not in input_utxos] #使用済みのUTXOを削除
  utxos.extend(outputs) # 新しいUTXOを追加

  print("Transaction created successfully.")
  return outputs, utxos

# 関数: 所有者の残高を表示
def display_balance(utxos, owners):
  balances = {}
  for owner in owners:
    balances[owner] = sum(utxo.amount for utxo in utxos if utxo.owner == owner)
    print(f"{owner}'s balance: {balances[owner]}")
  return balances

# マイニングによる供給
def mine_block(utxos, miner, reward):
  print(f"\nMining new block... Reward: {reward} to {miner}.")
  new_txid = str(uuid.uuid4())
  utxos.append(UTXO(new_txid, 0, reward, miner))
  return utxos

# ウォレットと初期UTXO
owners = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
utxos = [
    UTXO(txid="genesis", index=i, amount=random.randint(50, 200), owner=owner)
    for i, owner in enumerate(owners)
]

# シミュレーション開始
print("=== Initial State ===")
display_balance(utxos, owners)

# シミュレーションのループ
gas_fee = 2 #固定のガス代
miner = "Miner" # マイナー
utxos.append(UTXO(txid="genesis", index=len(owners), amount=0, owner=miner)) # マイナーの初期化

try:
  for _ in range(10): #10回のトランザクションをシミュレーション
    time.sleep(5) # 5秒ごとに実行
    sender = random.choice(owners)
    recipient = random.choice([o for o in owners if o != sender])
    amount = random.randint(1, 50)

    # トランザクション作成
    outputs, utxos = create_transaction(utxos, sender, recipient, amount, gas_fee)

    # 残高を表示
    print("\n=== Updated Balaneces ===")
    display_balance(utxos, owners + [miner])

    # マイニングによる供給
    utxos = mine_block(utxos, miner, reward=10)

except KeyboardInterrupt:
  print("\nSimulation stopped.")



