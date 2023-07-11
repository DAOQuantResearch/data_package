import requests
from pprint import pprint



def run_query(query):
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

query = """
{
swaps(where: {timestamp_gt: 1645100254, timestamp_lt: 1645100434}) {
id
transaction {
id
blockNumber
timestamp
}
timestamp
pool {
id
token0{
id
name
}
token1 {
id
name
}
}
sender
recipient
origin
amount0
amount1
amountUSD
}
}
"""
result = run_query(query)

# print the results
print('Print Result - {}'.format(result))
print('#############')
# pretty print the results
pprint(result)