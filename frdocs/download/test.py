"""import urllib3
from urllib3 import request
import re
import lxml
from lxml import etree as et

test_date = '2024-01-05'
url = f'https://www.govinfo.gov/content/pkg/FR-{test_date}/xml/FR-{test_date}.xml'

r = urllib3.request("GET", url, fields={}, timeout=10)

if r.status >= 200 and r.status < 400:
    print(f"r ok {r.status}")
    try:
        print(r.json())
    except:
        print(f"response is not json")
    raw_content = r.data
    # print(raw_content.decode(encoding="utf-8"))
    sub_content = re.sub(b"</E>",b"",raw_content)
    #print(sub_content)

    parser = et.XMLParser(attribute_defaults=True)
    tree = et.XML(raw_content, parser=parser)
    print(tree)


else:
    print(f"r ok {r.status}")"""

from lxml import etree

# 주어진 XML 문서
xml_content = """
<FED>
<P>
The petition to participate form is available online in eCRB, the Copyright Royalty Board's online electronic filing application, at
<E T="03">https://app.crb.gov/.</E>
Thank you.
</P>
<P>Instructions: The petition to participate process has been simplified. Interested parties file a petition to participate by completing and filing the petition to participate form in eCRB and paying the fee in eCRB. Do not upload a petition to participate document.</P>
</FED>
"""
from lxml import etree

# 주어진 XML 문서
xml_content = """
<FEF>
<P>
The petition to participate form is available online in eCRB, the Copyright Royalty Board's online electronic filing application, at
<E T="03">https://app.crb.gov/.</E>
Thank you.
</P>
<P>Instructions: The petition to participate process has been simplified. Interested parties file a petition to participate by completing and filing the petition to participate form in eCRB and paying the fee in eCRB. Do not upload a petition to participate document.</P>
</FEF>
"""
from lxml import etree

# 주어진 XML 문서
xml_content = """
<FEF>
<P>
The petition to participate form is available online in eCRB, the Copyright Royalty Board's online electronic filing application, at
<E T="03">https://app.crb.gov/.</E>
Thank you.
</P>
<P>Instructions: The petition to participate process has been simplified. Interested parties file a petition to participate by completing and filing the petition to participate form in eCRB and paying the fee in eCRB. Do not upload a petition to participate document.</P>
</FEF>
"""

from lxml import etree

# 주어진 XML 문서
xml_content = """
<FEF>
<P>
The petition to participate form is available online in eCRB, the Copyright Royalty Board's online electronic filing application, at
<E T="03">https://app.crb.gov/.</E>
Thank you.
</P>
<P>Instructions: The petition to participate process has been simplified. Interested parties file a petition to participate by completing and filing the petition to participate form in eCRB and paying the fee in eCRB. Do not upload a petition to participate document.</P>
</FEF>
"""

# XML 문서를 파싱합니다.
root = etree.fromstring(xml_content)

# <P> 엘리먼트 내에 있는 각각의 텍스트 노드를 처리합니다.
for p_element in root.xpath("//P"):
    # <P> 엘리먼트 내에 있는 텍스트를 저장할 리스트를 생성합니다.
    text_list = []
    
    # <P> 엘리먼트 내에 있는 각각의 텍스트 노드를 가져와서 리스트에 추가합니다.
    for item in p_element.xpath(".//text()"):
        text_list.append(item.strip())

    # <E> 엘리먼트의 텍스트를 가져와서 리스트에 추가합니다.
    for element in p_element:
        # <E> 엘리먼트를 삭제합니다.
        element.getparent().remove(element)

    # 변경된 텍스트를 합쳐서 <P> 엘리먼트의 텍스트로 설정합니다.
    p_element.text = ' '.join(text_list)

# 변경된 XML을 출력합니다.
print(etree.tostring(root, pretty_print=True).decode())