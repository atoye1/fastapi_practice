import PublicDataReader as pdr
from PublicDataReader import TransactionPrice
service_key = r"/bFeirMmNDzYg70ob5u8zSXfeq8agzNnPtXZy4EZhJbri2i5uwG8Xf95BWuebdwkcHpZnuKakHFslckYdnb0yA=="
api = TransactionPrice(service_key)
sigungu_name = "분당구"
code = pdr.code_bdong()
code.loc[(code['시군구명'].str.contains(sigungu_name)) &
         (code['읍면동명'] == '')]

df = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="41135",
    year_month="202212",
)
print(len(df))
print(df)
