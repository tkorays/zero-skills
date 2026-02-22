# Error Codes Reference

## 概览

飞书文档 API 错误码格式: `177xxxx`

## 客户端错误 (4xx)

### 参数错误

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770001 | invalid param | 确认传入的参数是否合法 |
| 1770002 | not found | 文档不存在，确认 document_id 是否正确 |
| 1770003 | resource deleted | 确认资源是否已被删除 |
| 1770024 | invalid operation | 确认操作是否合法 |

### 文档限制

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770004 | too many blocks in document | 确认文档 Block 数量是否超上限 |
| 1770005 | too deep level in document | 确认文档 Block 层级是否超上限 |
| 1770007 | too many children in block | 确认指定 Block 的 Children 数量是否超上限 |
| 1770008 | too big file size | 确认上传的文件尺寸是否超上限 |
| 1770010 | too many table column | 确认表格列数是否超上限 |
| 1770011 | too many table cell | 确认表格单元格数量是否超上限 |
| 1770012 | too many grid column | 确认 Grid 列数量是否超上限 |

### 关联关系错误

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770013 | relation mismatch | 图片、文件等资源的关联关系不正确。需同时上传相关素材至文档块中 |
| 1770014 | parent children relation mismatch | 确认 Block 父子关系是否正确 |
| 1770015 | single edit with multi document | 确认 Block 所属文档与指定的 Document 是否相同 |
| 1770019 | repeated blockID in document | 确认 Document 中的 BlockID 是否有重复 |
| 1770020 | operation denied on copying document | 确认 Document 是否正在创建副本中 |
| 1770021 | too old document | 指定的版本号与文档最新版本号差值不能超过 1000 |
| 1770022 | invalid page token | 确认查询参数中的 page_token 是否合法 |

### 操作不支持

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770025 | operation and block not match | 确认指定 Block 应用对应操作是否合法 |
| 1770026 | row operation over range | 确认行操作下标是否越界 |
| 1770027 | column operation over range | 确认列操作下标是否越界 |
| 1770028 | block not support create children | 确认指定 Block 添加 Children 是否合法 |
| 1770029 | block not support to create | 确认指定 Block 是否支持创建 |
| 1770030 | invalid parent children relation | 确认指定操作其父子关系是否合法 |
| 1770031 | block not support to delete children | 确认指定 Block 是否支持删除 Children |

### 资源限制

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770033 | content size exceed limit | 纯文本内容大小超过 10485760 字符限制 |
| 1770034 | operation count exceed limited | 当前请求中涉及单元格个数过多，拆分请求 |
| 1770035 | resource count exceed limit | 资源数目超限。各类资源上限：ChatCard 200张，File 200个，Image 20张，Sheet 5篇，Bitable 5篇 |

### 权限错误

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770032 | forbidden | 无文档权限。tenant_access_token 需添加应用；user_access_token 需用户获取分享权限 |

### 资源不存在

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1770038 | resource not found | 未查询到插入的资源或资源无权限插入 |

## 服务端错误 (5xx)

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 1771001 | server internal error | 服务器内部错误，重试或咨询技术支持 |
| 1771002 | gateway server internal error | 网关服务内部错误，重试或咨询技术支持 |
| 1771003 | gateway marshal error | 网关服务解析错误，重试或咨询技术支持 |
| 1771004 | gateway unmarshal error | 网关服务反解析错误，重试或咨询技术支持 |
| 1771005 | system under maintenance | 系统服务正在维护中 |
| 1771006 | mount folder failed | 挂载文档到云空间文件夹失败 |

## 频率限制

| 场景 | 限制 |
|------|------|
| 创建块 | 5次/秒 |
| 批量更新块 | 3次/秒 |
| 单篇文档并发编辑 | 3次/秒 |

**触发频率限制**: HTTP 429 或 400，返回 `99991400`

## 通用错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| 99991400 | 触发频率限制 | 使用指数退避重试 |
| 99991401 | IP不在白名单 | 配置IP白名单 |
| 99991679 | 权限不足 | 检查token授权范围 |
