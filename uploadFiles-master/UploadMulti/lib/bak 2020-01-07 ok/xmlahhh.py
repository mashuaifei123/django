from docx import Document
from lxml import etree

doc = Document('K:\mashuaifei\iacuc\A2020006-T014-01 BTC-IAC-0011-3.0 IACUC-动物管理和使用审批表 3.0 2020-03-06生效 20200704 - 副本.docx')
body_xml_str = doc._body._element.xml # 获取body中的xml
body_xml = etree.fromstring(body_xml_str) # 转换成lxml结点
print(etree.tounicode(body_xml)) # 打印查看

for p in doc.paragraphs:
    p_xml_str = p._p.xml # 按段落获取xml
    p_xml = etree.fromstring(p_xml_str) # 转换成lxml结点
    print(etree.tounicode(p_xml)) # 打印查看
