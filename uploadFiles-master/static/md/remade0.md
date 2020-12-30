# 欢迎使用 TTWV 转换系统
------
**TTWV** 是用于转换数据格式的BS架构系统. 建立在Django,Python,Pandas,Google-Tesseract-OCR,WS-API等框架库基础上.
> * [呼吸转换](/UploadMulti/progress-bar-upload/)
> * [血压转换](/UploadMulti/progress-bar-upload/)
> * [心电转换](/UploadMulti/progress-bar-upload/)
> * [标签生成](/UploadMulti/tsm-upload/)
> * [显著性](/UploadMulti/spss-upload/)
> * [SPSS数据格式](/UploadMulti/xzx-upload/)
## 0. 注意事项
* 1.请先清除已有文件在转换点击`删除所有文件`按钮
* 2.请导出与试验数据相关联的Pristima系统内的分组对照表.并将表格保存为**`分组表.xls`** 每个转换中都必须上传**分组表**.
* 3.已完成的内容会显示在`已完成－文件列表`
* 4.呼吸转换会比较慢一般在5分钟以上根据文件多少，所以请耐心等待．
* 5.如果没有转换成功会提示异常．并删除已上传的文件列表请核对后在转换.
* 6.请下载所有文件有些文件为统计分析调用的格式请一并交给SD.

## 1. [呼吸转换](/UploadMulti/progress-bar-upload/)
* 根据试验阶段顺序重命名word文件.
```例:01-P1.docx, 02-D24.docx, 03-Pr3.docx. . ...```
* 注意检查word文档中所有的图片必须满足固定位置，数据框应在图片的右上角.
## 2. [血压转换](/UploadMulti/progress-bar-upload/)
* 应确认所有从血压计系统中导出的文件名称在本次转换时唯一.
* 注意血压计系统中"COMMENT"栏位应该输入试验阶段.
* 如果导出完成后发现数据中有类似`异常数据:`请对原始数据进行检查确认.
## 3. [心电转换](/UploadMulti/progress-bar-upload/)
* 请按照固定模板格式excel文件手动填写数据并注意保证试验阶段顺序
* 每笔数据的第一栏位必须填写.
## 4. [标签生成](/UploadMulti/tsm-upload/)
* 请按照固定模板格式excel文件手动填写数据并注意保证无空内容
* 如果无法生成请检查excel文件.请注意后缀名一定为.xlsx格式文件
## 5. [显著性](/UploadMulti/spss-upload/)
## 6. [SPSS数据格式](/UploadMulti/xzx-upload/)

## 7. 转换文件的流程

```flow
st=>start: 开始
op=>operation: 删除系统中已存在的文件
op2=>operation: 上传文件
op3=>operation: 转换
e=>end: 下载已完成文件
st->op->op2->op3->e
```
## -1. 修订历史
* 版本号 2.01 Bate
- [ ] 修订 呼吸转换中排序问题
- [x] 新增 分析数据导出
- [x] 新增 识别图片中带有A-Z情况-呼吸
- [x] 新增 五位动物ID识别判断问题修复
- [x] 新增 供试品标签生成
------
```python
'再一次感谢您花费时间阅读这份欢迎稿，开始转换吧！别忘记QC数据哦'
# 作者 Rock
```
