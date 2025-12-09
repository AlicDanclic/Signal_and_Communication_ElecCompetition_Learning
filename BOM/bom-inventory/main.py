#!/usr/bin/env python3
"""
BOM表转HTML工具 - 国产型号截断版
将CSV格式的BOM表转换为可交互的HTML页面
"""

import csv
import json
import os
import sys
from datetime import datetime

def truncate_chinese_manufacturer(manufacturer_part, max_length=15):
    """截断国产型号显示"""
    if not manufacturer_part:
        return ""
    
    # 常见国产元器件关键字
    chinese_keywords = ['CL', 'FXL', 'LTST', 'DSHP', 'SK', 'HX', 'ZX', 'GH', 'WAFER']
    
    # 检查是否是国产元件
    is_chinese = any(keyword in manufacturer_part for keyword in chinese_keywords)
    
    if is_chinese and len(manufacturer_part) > max_length:
        # 截断并添加省略号
        return manufacturer_part[:max_length] + '...'
    
    return manufacturer_part

def parse_bom_csv(csv_file_path):
    """
    解析CSV格式的BOM表，按分组处理
    """
    bom_data = []
    total_qty = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # 使用csv模块读取
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                # 获取完整的Reference字符串（不拆分）
                references = row.get('Reference', '')
                
                # 获取数量
                try:
                    qty = int(row.get('Qty', 1))
                except:
                    qty = 1
                
                # 获取其他字段
                value = row.get('Value', '')
                footprint = row.get('Footprint', '')
                manufacturer_part = row.get('Manufacturer Part', '')
                
                # 截断国产型号显示
                truncated_manufacturer = truncate_chinese_manufacturer(manufacturer_part)
                
                # 创建条目（整个分组作为一个条目）
                bom_data.append({
                    'id': f"group_{row_num}",
                    'reference': references,  # 保持完整的Reference字符串
                    'value': value,
                    'footprint': footprint,
                    'manufacturer_part': manufacturer_part,
                    'truncated_manufacturer': truncated_manufacturer,
                    'qty': qty,  # 使用分组的总数量
                    'status': 'unchecked',  # 初始状态：未检查
                    'row_num': row_num  # 原始行号，用于排序
                })
                
                total_qty += qty
                
    except UnicodeDecodeError:
        # 尝试用GBK编码读取
        with open(csv_file_path, 'r', encoding='gbk') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                references = row.get('Reference', '')
                
                try:
                    qty = int(row.get('Qty', 1))
                except:
                    qty = 1
                
                value = row.get('Value', '')
                footprint = row.get('Footprint', '')
                manufacturer_part = row.get('Manufacturer Part', '')
                
                # 截断国产型号显示
                truncated_manufacturer = truncate_chinese_manufacturer(manufacturer_part)
                
                bom_data.append({
                    'id': f"group_{row_num}",
                    'reference': references,
                    'value': value,
                    'footprint': footprint,
                    'manufacturer_part': manufacturer_part,
                    'truncated_manufacturer': truncated_manufacturer,
                    'qty': qty,
                    'status': 'unchecked',
                    'row_num': row_num
                })
                
                total_qty += qty
    except Exception as e:
        print(f"解析CSV文件时出错: {e}")
        return [], 0
    
    return bom_data, total_qty

def generate_html(bom_data, total_qty, output_file, csv_filename):
    """
    生成HTML文件
    """
    # 计算统计信息
    total_groups = len(bom_data)
    
    checked_count = sum(1 for item in bom_data if item['status'] == 'checked')
    missing_count = sum(1 for item in bom_data if item['status'] == 'missing')
    ordered_count = sum(1 for item in bom_data if item['status'] == 'ordered')
    
    checked_percent = int((checked_count / total_groups * 100)) if total_groups > 0 else 0
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOM物料清单检查工具</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .header p {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .header .file-info {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .stat-card h3 {{
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .stat-card .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .stat-card.total {{
            border-top: 5px solid #3498db;
        }}
        
        .stat-card.checked {{
            border-top: 5px solid #2ecc71;
        }}
        
        .stat-card.progress {{
            border-top: 5px solid #f39c12;
        }}
        
        .stat-card.missing {{
            border-top: 5px solid #e74c3c;
        }}
        
        .stat-card.ordered {{
            border-top: 5px solid #9b59b6;
        }}
        
        .progress-bar {{
            height: 10px;
            background: #ecf0f1;
            border-radius: 5px;
            margin-top: 15px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #2ecc71, #27ae60);
            border-radius: 5px;
            transition: width 0.5s ease;
        }}
        
        .table-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #e9ecef;
            position: sticky;
            top: 0;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            color: #495057;
            vertical-align: top;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .status-selector {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .status-btn {{
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s;
            min-width: 70px;
            text-align: center;
        }}
        
        .status-btn.unchecked {{
            background: #ecf0f1;
            color: #7f8c8d;
        }}
        
        .status-btn.unchecked:hover, .status-btn.unchecked.active {{
            background: #bdc3c7;
            color: white;
        }}
        
        .status-btn.checked {{
            background: #d5f4e6;
            color: #27ae60;
        }}
        
        .status-btn.checked:hover, .status-btn.checked.active {{
            background: #27ae60;
            color: white;
        }}
        
        .status-btn.missing {{
            background: #fdedec;
            color: #e74c3c;
        }}
        
        .status-btn.missing:hover, .status-btn.missing.active {{
            background: #e74c3c;
            color: white;
        }}
        
        .status-btn.ordered {{
            background: #f4ecf7;
            color: #9b59b6;
        }}
        
        .status-btn.ordered:hover, .status-btn.ordered.active {{
            background: #9b59b6;
            color: white;
        }}
        
        .qty-badge {{
            background: #3498db;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 5px;
        }}
        
        .reference-cell {{
            font-size: 0.9em;
            line-height: 1.4;
            max-width: 200px;
            word-break: break-word;
        }}
        
        .value-cell {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .manufacturer-tooltip {{
            position: relative;
            cursor: help;
        }}
        
        .manufacturer-tooltip:hover::after {{
            content: attr(data-full);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #2c3e50;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9em;
            white-space: nowrap;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .control-panel {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .control-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: linear-gradient(135deg, #2980b9 0%, #1c6ea4 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(41, 128, 185, 0.4);
        }}
        
        .btn-success {{
            background: linear-gradient(135deg, #27ae60 0%, #219653 100%);
            color: white;
        }}
        
        .btn-success:hover {{
            background: linear-gradient(135deg, #219653 0%, #1e8449 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(33, 150, 83, 0.4);
        }}
        
        .btn-warning {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }}
        
        .btn-warning:hover {{
            background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(230, 126, 34, 0.4);
        }}
        
        .btn-danger {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
        }}
        
        .btn-danger:hover {{
            background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(192, 57, 43, 0.4);
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .legend {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }}
        
        .search-box {{
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .search-box input {{
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }}
        
        .search-box input:focus {{
            border-color: #3498db;
            outline: none;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
        }}
        
        @media (max-width: 768px) {{
            .stats-container {{
                grid-template-columns: 1fr;
            }}
            
            .control-panel {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .control-buttons {{
                flex-wrap: wrap;
                justify-content: center;
            }}
            
            .legend {{
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }}
            
            th, td {{
                padding: 10px 8px;
                font-size: 0.9em;
            }}
            
            .status-btn {{
                min-width: 60px;
                font-size: 12px;
                padding: 6px 8px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .table-container {{
                padding: 15px;
                overflow-x: auto;
            }}
            
            table {{
                font-size: 0.85em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 BOM物料清单检查工具</h1>
            <p>按分组检查物料，单击按钮标记状态</p>
            <div class="file-info">
                <p><strong>数据源:</strong> {csv_filename} | <strong>生成时间:</strong> {current_time}</p>
                <p><strong>分组数量:</strong> {total_groups} | <strong>总需求量:</strong> {total_qty}</p>
            </div>
        </div>
        
        <div class="control-panel">
            <div>
                <h3>状态标记控制</h3>
                <p style="color: #7f8c8d; font-size: 0.9em;">批量标记状态或保存进度</p>
            </div>
            <div class="control-buttons">
                <button class="btn btn-success" onclick="markAll('checked')">
                    <span>✅ 全部已检查</span>
                </button>
                <button class="btn btn-warning" onclick="markAll('unchecked')">
                    <span>🔄 全部未检查</span>
                </button>
                <button class="btn btn-danger" onclick="markAll('missing')">
                    <span>❌ 全部缺货</span>
                </button>
                <button class="btn btn-primary" onclick="markAll('ordered')">
                    <span>📦 全部已订购</span>
                </button>
                <button class="btn btn-primary" onclick="saveProgress()">
                    <span>💾 保存进度</span>
                </button>
            </div>
        </div>
        
        <div class="stats-container">
            <div class="stat-card total">
                <h3>分组数量</h3>
                <div class="stat-value">{total_groups}</div>
                <p>个分组</p>
            </div>
            
            <div class="stat-card checked">
                <h3>已检查</h3>
                <div class="stat-value">{checked_count}</div>
                <p>{checked_percent}% 完成</p>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill" style="width: {checked_percent}%"></div>
                </div>
            </div>
            
            <div class="stat-card missing">
                <h3>缺货</h3>
                <div class="stat-value">{missing_count}</div>
                <p>需要采购</p>
            </div>
            
            <div class="stat-card ordered">
                <h3>已订购</h3>
                <div class="stat-value">{ordered_count}</div>
                <p>已下单</p>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background-color: #bdc3c7;"></div>
                <span>未检查</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #27ae60;"></div>
                <span>已检查</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #e74c3c;"></div>
                <span>缺货</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #9b59b6;"></div>
                <span>已订购</span>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="搜索元件编号、值/型号、封装或制造商型号..." onkeyup="searchItems()">
        </div>
        
        <div class="table-container">
            <table id="bomTable">
                <thead>
                    <tr>
                        <th style="width: 200px;">Reference (元件编号)</th>
                        <th style="width: 120px;">值/型号</th>
                        <th style="width: 150px;">封装</th>
                        <th style="width: 120px;">制造商型号</th>
                        <th style="width: 100px;">需求数量</th>
                        <th style="width: 150px;">状态</th>
                    </tr>
                </thead>
                <tbody id="bomBody">
                    <!-- 动态填充 -->
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>© 2023 BOM物料清单检查工具 | 版本 4.0 | 简化版 - 按分组标记状态</p>
            <p style="font-size: 0.8em; margin-top: 5px;">注意：进度数据保存在浏览器本地存储中，国产型号已自动截断显示</p>
        </div>
    </div>
    
    <script>
        // 数据定义
        const bomData = {json.dumps(bom_data, ensure_ascii=False)};
        
        // 从localStorage加载进度数据
        function loadProgress() {{
            try {{
                const savedProgress = localStorage.getItem('bom_group_progress');
                if (savedProgress) {{
                    const progressData = JSON.parse(savedProgress);
                    
                    // 更新bomData中的状态
                    bomData.forEach(item => {{
                        if (progressData[item.id]) {{
                            item.status = progressData[item.id];
                        }}
                    }});
                    
                    // 更新统计信息
                    updateStats();
                    
                    // 重新渲染表格
                    renderBomTable();
                    
                    console.log('进度数据已加载');
                }}
            }} catch (e) {{
                console.error('加载进度数据失败:', e);
            }}
        }}
        
        // 保存进度数据到localStorage
        function saveProgressToLocalStorage() {{
            try {{
                // 创建进度数据对象
                const progressData = {{}};
                bomData.forEach(item => {{
                    progressData[item.id] = item.status;
                }});
                
                localStorage.setItem('bom_group_progress', JSON.stringify(progressData));
                return true;
            }} catch (e) {{
                console.error('保存进度数据失败:', e);
                return false;
            }}
        }}
        
        // 渲染BOM表格
        function renderBomTable() {{
            const tbody = document.getElementById('bomBody');
            tbody.innerHTML = '';
            
            if (bomData.length === 0) {{
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 40px; color: #7f8c8d;">
                            暂无数据
                        </td>
                    </tr>
                `;
                return;
            }}
            
            // 按原始行号排序
            const sortedData = [...bomData].sort((a, b) => a.row_num - b.row_num);
            
            sortedData.forEach(item => {{
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="reference-cell"><strong>${{item.reference}}</strong></td>
                    <td class="value-cell">${{item.value}}</td>
                    <td>${{item.footprint}}</td>
                    <td>
                        ${{item.truncated_manufacturer ? 
                            `<span class="manufacturer-tooltip" data-full="${{item.manufacturer_part}}">
                                ${{item.truncated_manufacturer}}
                            </span>` : 
                            item.manufacturer_part}}
                    </td>
                    <td><span class="qty-badge">${{item.qty}}个</span></td>
                    <td>
                        <div class="status-selector">
                            <button class="status-btn unchecked ${{item.status === 'unchecked' ? 'active' : ''}}" 
                                    onclick="updateStatus('${{item.id}}', 'unchecked')">
                                🔄 未检查
                            </button>
                            <button class="status-btn checked ${{item.status === 'checked' ? 'active' : ''}}" 
                                    onclick="updateStatus('${{item.id}}', 'checked')">
                                ✅ 已检查
                            </button>
                            <button class="status-btn missing ${{item.status === 'missing' ? 'active' : ''}}" 
                                    onclick="updateStatus('${{item.id}}', 'missing')">
                                ❌ 缺货
                            </button>
                            <button class="status-btn ordered ${{item.status === 'ordered' ? 'active' : ''}}" 
                                    onclick="updateStatus('${{item.id}}', 'ordered')">
                                📦 已订购
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            }});
        }}
        
        // 搜索功能
        function searchItems() {{
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const rows = document.getElementById('bomBody').getElementsByTagName('tr');
            
            for (let i = 0; i < rows.length; i++) {{
                const row = rows[i];
                const reference = row.cells[0].textContent || row.cells[0].innerText;
                const value = row.cells[1].textContent || row.cells[1].innerText;
                const footprint = row.cells[2].textContent || row.cells[2].innerText;
                const manufacturer = row.cells[3].textContent || row.cells[3].innerText;
                
                if (reference.toLowerCase().indexOf(filter) > -1 ||
                    value.toLowerCase().indexOf(filter) > -1 ||
                    footprint.toLowerCase().indexOf(filter) > -1 ||
                    manufacturer.toLowerCase().indexOf(filter) > -1) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }}
        }}
        
        // 更新分组状态
        function updateStatus(id, status) {{
            // 找到并更新分组状态
            const item = bomData.find(item => item.id === id);
            if (item) {{
                item.status = status;
                
                // 更新统计信息
                updateStats();
                
                // 重新渲染当前行
                const rows = document.getElementById('bomBody').getElementsByTagName('tr');
                for (let i = 0; i < rows.length; i++) {{
                    const row = rows[i];
                    const referenceCell = row.cells[0].textContent || row.cells[0].innerText;
                    
                    // 查找对应的行
                    if (referenceCell.includes(item.reference.split(',')[0])) {{
                        // 更新按钮状态
                        const buttons = row.cells[5].getElementsByClassName('status-btn');
                        for (let btn of buttons) {{
                            btn.classList.remove('active');
                            if (btn.classList.contains(status)) {{
                                btn.classList.add('active');
                            }}
                        }}
                        break;
                    }}
                }}
            }}
        }}
        
        // 标记所有分组的状态
        function markAll(status) {{
            if (confirm(`确定要将所有分组标记为"${{getStatusText(status)}}"吗？`)) {{
                bomData.forEach(item => {{
                    item.status = status;
                }});
                
                // 更新统计信息
                updateStats();
                
                // 重新渲染表格
                renderBomTable();
            }}
        }}
        
        // 更新统计信息
        function updateStats() {{
            const totalGroups = bomData.length;
            
            const checkedCount = bomData.filter(item => item.status === 'checked').length;
            const missingCount = bomData.filter(item => item.status === 'missing').length;
            const orderedCount = bomData.filter(item => item.status === 'ordered').length;
            
            const checkedPercent = totalGroups > 0 ? Math.round((checkedCount / totalGroups) * 100) : 0;
            
            // 更新统计卡片
            document.querySelector('.stat-card.total .stat-value').textContent = totalGroups;
            document.querySelector('.stat-card.checked .stat-value').textContent = checkedCount;
            document.querySelector('.stat-card.checked p:nth-child(3)').textContent = checkedPercent + '% 完成';
            document.querySelector('.stat-card.missing .stat-value').textContent = missingCount;
            document.querySelector('.stat-card.ordered .stat-value').textContent = orderedCount;
            
            // 更新进度条
            document.getElementById('progressFill').style.width = checkedPercent + '%';
        }}
        
        // 获取状态文本
        function getStatusText(status) {{
            const statusMap = {{
                'unchecked': '未检查',
                'checked': '已检查',
                'missing': '缺货',
                'ordered': '已订购'
            }};
            return statusMap[status] || status;
        }}
        
        // 保存进度
        function saveProgress() {{
            if (saveProgressToLocalStorage()) {{
                alert('✅ 进度已保存！');
            }} else {{
                alert('❌ 保存失败，请检查浏览器设置');
            }}
        }}
        
        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {{
            loadProgress();
            renderBomTable();
        }});
    </script>
</body>
</html>'''
    
    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"HTML文件已生成: {output_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("BOM表转HTML工具 - 国产型号截断版")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法: python bom_to_html.py <csv文件路径> [输出html文件名]")
        print("示例: python bom_to_html.py QuietLDO.csv bom_checklist.html")
        return
    
    csv_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"错误: 文件 '{csv_file}' 不存在")
        return
    
    # 设置输出文件名
    if len(sys.argv) >= 3:
        html_file = sys.argv[2]
        if not html_file.endswith('.html'):
            html_file += '.html'
    else:
        # 使用CSV文件名作为HTML文件名
        base_name = os.path.splitext(os.path.basename(csv_file))[0]
        html_file = f"{base_name}_checklist.html"
    
    print(f"正在处理文件: {csv_file}")
    
    # 解析CSV文件
    bom_data, total_qty = parse_bom_csv(csv_file)
    
    if not bom_data:
        print("错误: 未能解析到有效的BOM数据")
        return
    
    print(f"成功解析 {len(bom_data)} 个分组，总需求量: {total_qty}")
    
    # 生成HTML文件
    generate_html(bom_data, total_qty, html_file, os.path.basename(csv_file))
    
    print("=" * 60)
    print("完成！")
    print(f"生成的HTML文件: {html_file}")
    print("请直接在浏览器中打开该文件使用")
    print("=" * 60)
    print("功能说明:")
    print("1. 每个CSV行作为一个分组，保持Reference完整")
    print("2. 国产型号自动截断显示（鼠标悬停可查看完整型号）")
    print("3. 需求数量完整显示")
    print("4. 单击按钮标记分组状态：")
    print("   - 🔄 未检查: 尚未确认")
    print("   - ✅ 已检查: 已确认有货")
    print("   - ❌ 缺货: 需要采购")
    print("   - 📦 已订购: 已下单购买")
    print("5. 支持搜索功能")
    print("6. 支持批量标记状态")
    print("7. 点击'保存进度'保存当前状态到浏览器")
    print("=" * 60)

if __name__ == '__main__':
    main()