import asyncio
import json
import httpx
from typing import Any,Tuple,List,Dict
import urllib
import urllib.parse
import aiohttp
from mcp.server.fastmcp import FastMCP,Context
import pandas as pd

# 初始化 MCP 服务器
mcp = FastMCP("GeneService")

GENE_SERVICE_URL='http://113.44.88.128:28080'
extract_terms_route = '/api/v1/master/gene//mcp-extract-gene'

async def fetch_gene_infomation(query: str,userGenes: list) -> Tuple[str, Dict[str, Any]]:
    """
    根据用户问题从目前现有的通用文化基因数据库以及用户的个人数据基因中获取相关资料。
    :param query: 用户的问题 
    :param token: 用于用户身份验证 
    :return: 检索出来的相关资料以及相关节点与边的字典；
    """
    genes = []
    res = """护肤的艺术，悦享耐心之美。

从墨尔本的小巷到全球的精致角落，Aesop始终秉持着对天然成分的专注、独特美学的追求以及社区文化的联结。我们相信，真正的美丽源于自然的馈赠与时间的沉淀。每一款产品都如一件艺术品般诞生，在经典与创新之间寻找平衡，用坚定的道德理念和深厚的文化灵感书写护肤新篇章。

香芹籽抗氧化精华、赋活芳香护手霜、均衡洗发露……每一件作品都是对品质生活的致敬。在Aesop的世界里，护肤不仅仅是仪式感，更是一种生活态度——它关乎耐心，也关乎自我发现。

正如Plutarch所言：“做事的从容与速度无法赋予作品持久的稳固或精确之美。”而Aesop则通过耐心与匠心，将这份哲思融入每一次触碰肌肤的瞬间。

让我们一起，在护肤的艺术中，感受耐心带来的无尽魅力。"""
    return res,genes


async def request_for_mcp_gene_service(prompt: str, 
                                      apikey: str,ctx: Context) -> \
            Tuple[str, Dict[str, Any]]|None:
        requests_data = {
        
            "apikey": apikey,
            "prompt": prompt,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=urllib.parse.urljoin(GENE_SERVICE_URL, 
                                                            extract_terms_route),
                                   json=requests_data) as resp:
                if resp.status != 200:
                    await ctx.error(f"从cgg获取mcp-gene-service信息失败") 
                    # log.error(f'Failed to request mcp-gene-service for : {resp.reason}')
                    return None, None
                else:
                    await ctx.info(f"从cgg获取mcp-gene-service信息成功！") 
                    response = await resp.json()
                    corpuses = response['relation_text']
                    genes = response['relation_genes']
                
                    return genes, corpuses


async def test_request_for_mcp_gene_service(prompt: str,
                                       apikey: str) -> \
        Tuple[str, Dict[str, Any]] | None:
    requests_data = {

        "apikey": apikey,
        "prompt": prompt,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=urllib.parse.urljoin(GENE_SERVICE_URL,
                                                         extract_terms_route),
                                json=requests_data) as resp:
            if resp.status != 200:
                print(f"从cgg获取mcp-gene-service信息失败")
                # log.error(f'Failed to request mcp-gene-service for : {resp.reason}')
                return None, None
            else:
                print(f"从cgg获取mcp-gene-service信息成功！")
                response = await resp.json()
                corpuses = response['relation_text']
                genes = response['relation_genes']

                return genes, corpuses


async def test():
    prompt = "理肤泉"
    apikey = "384fde3636e6e01e0194d2976d8f26410af3e846e573379cb1a09e2f0752d8cc"
    result  = await test_request_for_mcp_gene_service(prompt,apikey)
    print(result)
# 这里名称待修改，后期是改成query_xxxxxxx      xxxxx比如weather
@mcp.tool()
async def query_any_question(prompt: str,apiKey :str,ctx: Context)-> Tuple[str, Dict[str, Any]]|None:
    """
    根据用户问题从目前现有的通用文化基因数据库以及用户的个人数据基因中获取相关资料。
    :param query: 用户的问题 
    :param apiKey: 用于用户身份验证 
    :return: 检索出来的相关资料以及相关节点与边的字典；
    """
    await ctx.info(f"Submitting img2img task: prompt={prompt}") 

    #genes,relevantInfomation = await request_for_mcp_gene_service(prompt,apiKey,ctx)
    genes = {"nodes":["abc"],"links":["bcd"]}
    relevantInfomation = ""
    return genes,relevantInfomation

if __name__ == "__main__":
    # 以sse
    asyncio.run(test())
    #mcp.run(transport='stdio')  #如果运行在 http://0.0.0.0:8000，这时候不要开clash，不然连不上