import requests
from pprint import pprint
from eth_utils import to_bytes

import json
class uniswapAPI():

    def __init__(self):
        pass

    def run_query(self,query,variable):
        #json_file={'query':query,"variables":variable}
        
        request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
                                '',
                                json={'query':query,"variables":variable})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

    
    
    def get_token_pool(self,crypto):
        query = """
            query get_token_pool($crypto:String!){
                tokens(where:{symbol:$crypto}) {
                name
                id
                poolCount
                whitelistPools {
                id
                token0 {
                    id
                    symbol
                }
                token1 {
                    id
                    symbol
                }
                

                }
            }
            }



        """
        variables={"crypto":crypto}
        data=self.run_query(query,variables)
        return data
    
    def get_token_info(self,crypto):
        query = """
            query get_token_info($crypto:String!){
                tokens(where:{symbol:$crypto}) {
                name
                id
                totalSupply
                volume
                volumeUSD
                txCount
                feesUSD
                poolCount
                totalValueLockedUSD
                totalValueLockedUSDUntracked
               
                derivedETH

            }
            }

        """
        #print(query)
        variables={"crypto":crypto}
        data=self.run_query(query,variables)
        return data
    
    def pool_info(self,pool_address):
        query = """
            query pool_info($pool_address:String!){
                pools(where:{id:$pool_address}) {
                id
                createdAtTimestamp
                token0 {
                    id 
                    symbol
                }
                token1{
                    id
                    symbol
                }
                txCount
                tick
                feeTier
                liquidity
                sqrtPrice
                feeGrowthGlobal0X128
                feeGrowthGlobal1X128
                token0Price
                token1Price
                volumeToken0
                volumeToken1
                totalValueLockedToken0
                totalValueLockedToken1
                totalValueLockedUSD
                liquidityProviderCount
                ticks(orderBy:tickIdx,orderDirection:asc){
                    id
                    tickIdx
                    poolAddress
                    liquidityGross
                    liquidityNet
                    liquidityProviderCount
                    volumeToken0
                    volumeToken1
                    volumeUSD
                    feeGrowthOutside0X128
                    feeGrowthOutside1X128
                }
                collects{
                    id 
                    transaction
                    timestamp
                    pool
                    owner             
                    amount0
                    amount1
                    amountUSD
                    tickLower
                    tickUpper
                    logIndex                    
                
                }

                swaps{
                    id 
                    transaction
                    timestamp
                    pool
                    token0
                    token1                  
                    sender
                    origin
                    amount0                    
                    amount1
                    amountUSD                  
                    logIndex
                
                }

                burns{
                    id 
                    transaction
                    timestamp
                    pool
                    token0
                    token1
                    owner
                    origin
                    amount
                    amount0                 
                    amount1
                    amountUSD
                    tickLower
                    tickUpper
                    logIndex
                

                }

                mints{
                    id 
                    transaction
                    timestamp
                    pool
                    token0
                    token1
                    owner
                    sender
                    origin                   
                    amount
                    amount0                   
                    amount1
                    amountUSD
                    tickLower
                    tickUpper
                    logIndex
                

                }

                }
                }


        """
        variables={"pool_address":pool_address}
        data=self.run_query(query,variables)
        return data
    
    def tick_info(self, tick_id):
        query = """
            query tick_info($tick_id:String!){
                ticks(where:{id:$tick_id}) {
                id
                tickIdx
                poolAddress
                liquidityGross
                liquidityNet
                liquidityProviderCount
                volumeToken0
                volumeToken1
                volumeUSD
                feeGrowthOutside0X128
                feeGrowthOutside1X128
                pool{
                    id
                    token0{
                        id
                        symbol
                    }
                    token1{
                        id
                        symbol
                    }
                }
                }
            }

        """
        variables={"tick_id":tick_id}
        data=self.run_query(query,variables)
        return data
    

    # def swap_info_by_recipient(self,recipient_id):
    #     query = """
    #         query swap_info($recipient_id:String!){
    #             swaps(where:{recipient:$recipient_id}) {
    #             id
    #             timestamp
    #             transaction{
    #                 id
    #                 timestamp
    #                 gasUsed
    #                 gasPrice
    #             }
    #             token0 {
    #                 id
    #                 symbol
    #             }
    #             token1 {
    #                 id
    #                 symbol
    #             }
    #             amount0
    #             amount1
    #             amountUSD
    #             sender
    #             recipient
    #             pool{
    #                 id
    #             }
    #             tick
    #             sqrtPriceX96
    #             logIndex
                
             
    #             }
    #         }

    #     """
    #     variables={"recipient_id":recipient_id.encode()}
    #     data=self.run_query(query,variables)
    #     return data
    
    # def swap_info_by_sender(self,sender_id):
    #     query = """
    #         query swap_info($sender_id:Bytes!){
    #             swaps(where:{sender:$sender_id}) {
    #             id
    #             timestamp
    #             transaction{
    #                 id
    #                 timestamp
    #                 gasUsed
    #                 gasPrice
    #             }
    #             token0 {
    #                 id
    #                 symbol
    #             }
    #             token1 {
    #                 id
    #                 symbol
    #             }
    #             amount0
    #             amount1
    #             amountUSD
    #             sender
    #             recipient
    #             pool{
    #                 id
    #             }
    #             tick
    #             sqrtPriceX96
    #             logIndex
                
             
    #             }
    #         }

    #     """
    #     sender_bytes = to_bytes(hexstr=sender_id)
    #     #print(sender_bytes)

    #     variables={"sender_id":sender_id}
    #     #print(variables)
    #     data=self.run_query(query,variables)
    #     return data

    def pool_hour_data(self,pool_id,timestamp):
        timestamp=int(timestamp)
        query = """
            query pool_hour_data($pool_id:String!,$timestamp:Int!){
                poolHourDatas(where:{pool:$pool_id,periodStartUnix:$timestamp}) {
                id
                periodStartUnix
                
                pool{
                    id
                    token0{
                        id
                        symbol
                    }
                    token1{
                        id
                        symbol
                    }
                }
                tvlUSD
                volumeToken0
                volumeToken1
                volumeUSD
                txCount
                open
                high
                low
                close
              
              
                }
            }

        """
        variables={"pool_id":pool_id,"timestamp":timestamp}
        data=self.run_query(query,variables)
        return data
    
    # def tick_hour_data(self,pool_address,tick_index,timestamp):
    #     pool_id = f"{pool_address}-{tick_index}-{timestamp}"
    #     print(pool_id)

    #     query = """
    #         query tick_hour_data($pool_id: ID!) {
    #             tickHourDatas(id: $pool_id) {
    #                 id
    #                 periodStartUnix
    #                 pool {
    #                     id
    #                     token0 {
    #                         id
    #                         symbol
    #                     }
    #                     token1 {
    #                         id
    #                         symbol
    #                     }
    #                 }
    #                 tick {
    #                     id
    #                     tickIdx
    #                 }
    #                 liquidityGross
    #                 liquidityNet
    #                 volumeToken0
    #                 volumeToken1
    #                 volumeUSD
    #                 feesUSD
    #             }
    #         }
    #     """

    #     variables = {"pool_id": pool_id}
    #     data = self.run_query(query, variables)
    #     return data

    def token_hour_data(self,crypto_address,timestamp):
        query = """
            query token_hour_data($crypto_address:String!,$timestamp:Int!){
                tokenHourDatas(where:{token:$crypto_address,periodStartUnix:$timestamp}) {
                id
                periodStartUnix
                token{
                    id
                    symbol
                }
                tvlUSD
                volumeToken0
                volumeToken1
                volumeUSD
                txCount
                open
                high
                low
                close
              
              
                }
            }

        """
        variables={"crypto_address":crypto_address,"timestamp":timestamp}
        data=self.run_query(query,variables)
        return data




uniswap_client=uniswapAPI()
#print(uniswap_client.pool_info("0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"))
#print(uniswap_client.tick_info("0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8#-78600"))

#print(uniswap_client.get_token_info("USDC"))
#print(uniswap_client.get_token_info(""))
print(uniswap_client.token_hour_data("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",1689206400))