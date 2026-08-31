"""MultiAgentSystem · 智能家居 MCP 服务器

基于 Model Context Protocol (MCP) 的智能家居控制服务。
任何兼容 MCP 的智能体客户端（Claude Desktop、TRAE、Cursor 等）都可以
接入本服务器，从而获得「感知环境 + 控制设备」的能力：

    感知：get_temperature —— 读取房间温度传感器
    执行：control_light   —— 控制房间灯光开关

运行方式：

    # 方式一：官方 CLI（自动发现模块级变量 mcp）
    mcp run smarthome_mcp.py

    # 方式二：直接运行（stdio 传输）
    python smarthome_mcp.py

设备数据当前为模拟实现，接入真实硬件时只需替换函数体，工具接口保持不变。
"""

import sys

from mcp.server import MCPServer

# ---------------------------------------------------------------------------
# 创建 MCP 服务器实例
#
# 变量名必须为 mcp / server / app 之一，`mcp run` 依赖它自动发现服务器对象。
# ---------------------------------------------------------------------------
mcp = MCPServer(
    "smarthome-mcp",
    title="Smart Home MCP Server",
    instructions=(
        "你是一个智能家居控制智能体：先调用 get_temperature 感知环境，"
        "再根据用户意图调用 control_light 执行设备控制。"
    ),
)


# ---------------------------------------------------------------------------
# 工具（Tools）：智能体可调用的能力
#
# @mcp.tool() 会根据函数签名与 docstring 自动生成 JSON Schema，
# 无需手写任何协议层代码。
# ---------------------------------------------------------------------------
@mcp.tool()
def get_temperature(room: str) -> str:
    """获取指定房间的当前温度（传感器数据）

    Args:
        room: 房间标识，例如 'living_room'、'bedroom'
    """
    # 【模拟】读取温度传感器；接入真实设备时替换此处即可
    temp = 24.5 if room == "living_room" else 22.0
    return f"传感器返回: {room} 的当前温度是 {temp}°C"


@mcp.tool()
def control_light(room: str, state: str) -> str:
    """打开或关闭指定房间的灯

    Args:
        room: 房间名，例如 'living_room'
        state: 灯的状态，必须是 'on' 或 'off'
    """
    # 【模拟】发送物理控制指令
    # 注意：stdio 传输下日志必须写入 stderr，否则会污染 JSON-RPC 消息流
    print(f"\n--> [硬件执行] 正在将 {room} 的灯设置为 {state}...\n", file=sys.stderr)
    return f"操作成功: {room} 的灯已切换为 {state} 状态。"


if __name__ == "__main__":
    # 以 stdio 传输启动，供 MCP 客户端通过标准输入/输出通信
    mcp.run("stdio")
