import time
from datetime import datetime
import random
from rethinkdb import RethinkDB


STATE = {
  "type": "channels",
  "channels": [
    {"name": "Ch1",
      "on": False},
    {"name": "Ch2",
      "on": False},
    {"name": "Ch3",
      "on": False},
    {"name": "Ch4",
      "on": False},
    {"name": "Ch5",
      "on": False},
    {"name": "Ch6",
      "on": False},
    {"name": "Ch7",
      "on": False},
    {"name": "Ch8",
      "on": False}
  ]
}


def check_channels(r):
  # busca documento com informação sobre canais
  if 'id' in STATE:
    print(STATE['id'])
    STATE.update(r.table('ensaios').get(STATE['id']).run())
  else:
    print("Finding state doc")
    cursor  = r.table('ensaios').filter(r.row["type"] == "channels").run()
    channels_res = []
    for doc in cursor:
      channels_res.append(doc)
    # se não existe documento com informações sobre canais
    # criamos um
    if len(channels_res) == 0:
      print("Bootstraping state doc")
      r.table("ensaios").insert(STATE).run()
    else:
      STATE.update(channels_res[0])


def main():
  r = RethinkDB()
  r.connect("localhost", 28015).repl()

  # cria tabela caso não exista
  try:
    r.db('test').tableCreate('ensaios')
    r.table('ensaios').indexCreate('date')
  except Exception as e:
    pass

  while True:
    check_channels(r)

    for ch in STATE["channels"]:
      check_channels(r)
      
      r.table("ensaios").insert(
        [
          {
            "ensaio_id": "Teste 1",
            "ch": {"name": ch["name"]},
            "val": random.random(),
            "date": datetime.now().isoformat()
          }
        ]
      ).run()
      print("insert done.")
      time.sleep(5)

if __name__ == '__main__':
  main()