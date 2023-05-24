import PublicDataReader as pdr
# code = pdr.code_bdong()
# print(code)

from PublicDataReader import Kbland
api = Kbland()
params = {
    "월간주간구분코드": "02",
    "매물종별구분": "01",
    "매매전세코드": "01",
    "지역코드": "11",
    "기간": "1",
}
df = api.get_price_index(**params)
print(df.tail())