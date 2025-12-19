#!/usr/bin/env python3
"""
基于DXF文件的钢网生成器 - 增强版
从Edge_Cuts.dxf和Paste.dxf直接生成3D打印钢网
支持更多DXF实体类型和更好的错误诊断
"""

import re
import sys
import argparse
import numpy as np
from pathlib import Path
import struct
import math
import time
from typing import List, Tuple, Dict, Any
import ezdxf
from ezdxf import recover
from ezdxf.document import Drawing

class ProgressBar:
    """简单的进度条显示"""
    
    def __init__(self, total=100, prefix='', suffix='', length=50, fill='█'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.start_time = time.time()
        self.current = 0
    
    def update(self, progress):
        """更新进度条"""
        self.current = progress
        percent = f"{100 * (progress / float(self.total)):.1f}"
        filled_length = int(self.length * progress // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # 计算已用时间和预计剩余时间
        elapsed_time = time.time() - self.start_time
        if progress > 0:
            eta = elapsed_time * (self.total - progress) / progress
            eta_str = f"ETA: {self._format_time(eta)}"
        else:
            eta_str = "ETA: --:--"
        
        elapsed_str = f"用时: {self._format_time(elapsed_time)}"
        
        # 打印进度条
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% ({progress}/{self.total}) {self.suffix} [{elapsed_str}, {eta_str}]')
        sys.stdout.flush()
    
    def complete(self):
        """完成进度条"""
        elapsed_time = time.time() - self.start_time
        filled_length = self.length
        bar = self.fill * filled_length
        sys.stdout.write(f'\r{self.prefix} |{bar}| 100.0% ({self.total}/{self.total}) {self.suffix} [用时: {self._format_time(elapsed_time)}]     \n')
        sys.stdout.flush()
    
    def _format_time(self, seconds):
        """格式化时间显示"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"

class DXFStencilGenerator:
    """基于DXF文件的钢网生成器"""
    
    def __init__(self):
        self.board_outline = []  # 板框轮廓点
        self.pads = []           # 焊盘信息
        self.progress_callback = None
        self.debug_info = []     # 调试信息
    
    def add_debug_info(self, message):
        """添加调试信息"""
        self.debug_info.append(message)
        if len(self.debug_info) > 100:  # 限制调试信息数量
            self.debug_info = self.debug_info[-100:]
    
    def print_debug_info(self):
        """打印调试信息"""
        print("\n调试信息:")
        for i, info in enumerate(self.debug_info[-20:]):  # 显示最后20条
            print(f"  {i+1}. {info}")
    
    def parse_dxf_file(self, filename: str, file_type: str) -> bool:
        """通用DXF文件解析函数"""
        try:
            print(f"正在解析{file_type}文件: {filename}")
            self.add_debug_info(f"开始解析{file_type}文件: {filename}")
            
            # 检查文件是否存在
            if not Path(filename).exists():
                print(f"错误: 文件不存在 - {filename}")
                self.add_debug_info(f"文件不存在: {filename}")
                return False
            
            # 检查文件大小
            file_size = Path(filename).stat().st_size
            print(f"文件大小: {file_size} 字节")
            self.add_debug_info(f"文件大小: {file_size} 字节")
            
            if file_size == 0:
                print("错误: 文件为空")
                self.add_debug_info("文件为空")
                return False
            
            # 尝试读取文件内容的前几行来检查格式
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    first_lines = [f.readline() for _ in range(5)]
                print(f"文件前几行: {first_lines}")
                self.add_debug_info(f"文件前几行: {first_lines}")
            except:
                pass
            
            # 使用恢复模式加载DXF文件，更宽容
            try:
                doc, auditor = recover.readfile(filename)
            except Exception as e:
                print(f"使用恢复模式加载失败: {e}")
                print("尝试使用标准模式加载...")
                try:
                    doc = ezdxf.readfile(filename)
                    auditor = doc.audit()
                except Exception as e2:
                    print(f"标准模式加载也失败: {e2}")
                    self.add_debug_info(f"加载DXF文件失败: {e}")
                    self.add_debug_info(f"标准模式也失败: {e2}")
                    return False
            
            # 检查审计结果
            if auditor.has_errors:
                print("警告: DXF文件有错误，但将继续解析")
                for error in auditor.errors:
                    print(f"  DXF错误: {error}")
                    self.add_debug_info(f"DXF错误: {error}")
            
            if auditor.has_fixes:
                print("信息: DXF文件已修复")
                for fix in auditor.fixes:
                    print(f"  DXF修复: {fix}")
                    self.add_debug_info(f"DXF修复: {fix}")
            
            # 获取所有实体
            msp = doc.modelspace()
            all_entities = list(msp)
            
            print(f"找到实体数量: {len(all_entities)}")
            self.add_debug_info(f"找到实体数量: {len(all_entities)}")
            
            # 按类型统计实体
            entity_counts = {}
            for entity in all_entities:
                entity_type = entity.dxftype()
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
            
            print("实体类型统计:")
            for entity_type, count in entity_counts.items():
                print(f"  {entity_type}: {count}个")
                self.add_debug_info(f"实体类型: {entity_type} = {count}个")
            
            # 尝试从块中获取实体
            blocks_entities = []
            for block in doc.blocks:
                blocks_entities.extend(list(block))
            
            if blocks_entities:
                print(f"从块中找到实体数量: {len(blocks_entities)}")
                self.add_debug_info(f"块中实体数量: {len(blocks_entities)}")
                all_entities.extend(blocks_entities)
            
            # 尝试从布局中获取实体
            layout_entities = []
            for layout in doc.layouts:
                if layout.name not in ['Model', '*Model_Space']:
                    layout_entities.extend(list(layout))
            
            if layout_entities:
                print(f"从布局中找到实体数量: {len(layout_entities)}")
                self.add_debug_info(f"布局中实体数量: {len(layout_entities)}")
                all_entities.extend(layout_entities)
            
            total_entities = len(all_entities)
            print(f"总实体数量: {total_entities}")
            self.add_debug_info(f"总实体数量: {total_entities}")
            
            if total_entities == 0:
                print("警告: 未找到任何几何实体")
                self.add_debug_info("未找到任何几何实体")
                # 尝试检查文件是否是ASCII格式
                self._check_file_format(filename)
                return False
            
            # 根据文件类型调用相应的处理函数
            if file_type == "Edge_Cuts":
                return self._process_edge_cuts_entities(all_entities)
            elif file_type == "Paste":
                return self._process_paste_entities(all_entities)
            else:
                print(f"错误: 未知的文件类型: {file_type}")
                return False
            
        except Exception as e:
            print(f"解析{file_type}文件失败: {e}")
            import traceback
            traceback.print_exc()
            self.add_debug_info(f"解析失败: {e}")
            return False
    
    def _check_file_format(self, filename):
        """检查文件格式"""
        try:
            with open(filename, 'rb') as f:
                content = f.read(100)  # 读取前100字节
            
            # 检查是否是ASCII DXF文件
            try:
                text = content.decode('ascii', errors='ignore')
                if 'SECTION' in text or 'HEADER' in text or 'ENTITIES' in text:
                    print("文件似乎是ASCII DXF格式")
                    self.add_debug_info("文件是ASCII DXF格式")
                else:
                    print("文件不是标准的ASCII DXF格式")
                    self.add_debug_info("文件不是标准ASCII DXF格式")
            except:
                print("文件不是ASCII格式，可能是二进制DXF")
                self.add_debug_info("文件是二进制DXF格式")
            
            # 检查文件头
            print(f"文件头(hex): {content[:20].hex()}")
            self.add_debug_info(f"文件头: {content[:20].hex()}")
            
        except Exception as e:
            print(f"检查文件格式失败: {e}")
            self.add_debug_info(f"检查格式失败: {e}")
    
    def _process_edge_cuts_entities(self, entities):
        """处理Edge_Cuts实体"""
        print("正在处理Edge_Cuts实体...")
        self.board_outline = []
        
        for i, entity in enumerate(entities):
            entity_type = entity.dxftype()
            
            if entity_type == 'LWPOLYLINE':
                print(f"  处理LWPOLYLINE实体 #{i}")
                self.add_debug_info(f"处理LWPOLYLINE实体 #{i}")
                try:
                    with entity.points() as points:
                        for point in points:
                            self.board_outline.append((point[0], point[1]))
                    print(f"    添加了{len(list(entity.points()))}个点")
                except Exception as e:
                    print(f"    处理LWPOLYLINE失败: {e}")
                    self.add_debug_info(f"LWPOLYLINE处理失败: {e}")
            
            elif entity_type == 'LINE':
                print(f"  处理LINE实体 #{i}")
                self.add_debug_info(f"处理LINE实体 #{i}")
                try:
                    start = entity.dxf.start
                    end = entity.dxf.end
                    self.board_outline.append((start[0], start[1]))
                    self.board_outline.append((end[0], end[1]))
                    print(f"    添加了2个点: ({start[0]:.2f},{start[1]:.2f}) 到 ({end[0]:.2f},{end[1]:.2f})")
                except Exception as e:
                    print(f"    处理LINE失败: {e}")
                    self.add_debug_info(f"LINE处理失败: {e}")
            
            elif entity_type == 'CIRCLE':
                print(f"  处理CIRCLE实体 #{i}")
                self.add_debug_info(f"处理CIRCLE实体 #{i}")
                try:
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    # 将圆形近似为多边形
                    num_segments = 32
                    for j in range(num_segments):
                        angle = 2 * math.pi * j / num_segments
                        x = center[0] + radius * math.cos(angle)
                        y = center[1] + radius * math.sin(angle)
                        self.board_outline.append((x, y))
                    print(f"    添加了{num_segments}个点，中心({center[0]:.2f},{center[1]:.2f})，半径{radius:.2f}")
                except Exception as e:
                    print(f"    处理CIRCLE失败: {e}")
                    self.add_debug_info(f"CIRCLE处理失败: {e}")
            
            elif entity_type == 'ARC':
                print(f"  处理ARC实体 #{i}")
                self.add_debug_info(f"处理ARC实体 #{i}")
                try:
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    start_angle = math.radians(entity.dxf.start_angle)
                    end_angle = math.radians(entity.dxf.end_angle)
                    
                    # 确保角度顺序正确
                    if end_angle < start_angle:
                        end_angle += 2 * math.pi
                    
                    # 将圆弧近似为多边形段
                    num_segments = max(8, int((end_angle - start_angle) * radius))
                    for j in range(num_segments + 1):
                        angle = start_angle + (end_angle - start_angle) * j / num_segments
                        x = center[0] + radius * math.cos(angle)
                        y = center[1] + radius * math.sin(angle)
                        self.board_outline.append((x, y))
                    print(f"    添加了{num_segments+1}个点，圆弧角度:{start_angle:.2f}到{end_angle:.2f}")
                except Exception as e:
                    print(f"    处理ARC失败: {e}")
                    self.add_debug_info(f"ARC处理失败: {e}")
            
            elif entity_type in ['POLYLINE', 'POLYLINE2D', 'POLYLINE3D']:
                print(f"  处理{entity_type}实体 #{i}")
                self.add_debug_info(f"处理{entity_type}实体 #{i}")
                try:
                    points = list(entity.points())
                    for point in points:
                        self.board_outline.append((point[0], point[1]))
                    print(f"    添加了{len(points)}个点")
                except Exception as e:
                    print(f"    处理{entity_type}失败: {e}")
                    self.add_debug_info(f"{entity_type}处理失败: {e}")
            
            elif entity_type == 'SPLINE':
                print(f"  处理SPLINE实体 #{i}（近似为线段）")
                self.add_debug_info(f"处理SPLINE实体 #{i}")
                try:
                    # 将样条曲线近似为多段线
                    flattener = entity.flattening(0.01)  # 公差
                    points = list(flattener)
                    for point in points:
                        self.board_outline.append((point[0], point[1]))
                    print(f"    添加了{len(points)}个点（样条近似）")
                except Exception as e:
                    print(f"    处理SPLINE失败: {e}")
                    self.add_debug_info(f"SPLINE处理失败: {e}")
            
            elif entity_type == 'ELLIPSE':
                print(f"  处理ELLIPSE实体 #{i}（近似为多边形）")
                self.add_debug_info(f"处理ELLIPSE实体 #{i}")
                try:
                    # 将椭圆近似为多边形
                    center = entity.dxf.center
                    major_axis = entity.dxf.major_axis
                    ratio = entity.dxf.ratio
                    
                    num_segments = 32
                    for j in range(num_segments):
                        angle = 2 * math.pi * j / num_segments
                        # 参数方程
                        x = center[0] + major_axis[0] * math.cos(angle) + major_axis[1] * math.sin(angle) * ratio
                        y = center[1] + major_axis[0] * math.sin(angle) - major_axis[1] * math.cos(angle) * ratio
                        self.board_outline.append((x, y))
                    print(f"    添加了{num_segments}个点")
                except Exception as e:
                    print(f"    处理ELLIPSE失败: {e}")
                    self.add_debug_info(f"ELLIPSE处理失败: {e}")
            
            else:
                print(f"  跳过未处理的实体类型: {entity_type} #{i}")
                self.add_debug_info(f"跳过实体类型: {entity_type}")
        
        # 去重和优化板框点
        if self.board_outline:
            unique_points = []
            seen = set()
            for point in self.board_outline:
                point_key = (round(point[0], 4), round(point[1], 4))
                if point_key not in seen:
                    seen.add(point_key)
                    unique_points.append(point)
            self.board_outline = unique_points
        
        print(f"Edge_Cuts处理完成: 找到{len(self.board_outline)}个轮廓点")
        self.add_debug_info(f"Edge_Cuts处理完成: {len(self.board_outline)}个点")
        
        # 如果板框点太少，尝试从边界计算
        if len(self.board_outline) < 3:
            print("警告: 板框点太少，尝试从实体边界计算...")
            self._calculate_bounds_from_entities(entities)
        
        return True
    
    def _process_paste_entities(self, entities):
        """处理Paste实体"""
        print("正在处理Paste实体...")
        self.pads = []
        
        for i, entity in enumerate(entities):
            entity_type = entity.dxftype()
            pad_info = {}
            
            if entity_type == 'LWPOLYLINE':
                print(f"  处理LWPOLYLINE焊盘实体 #{i}")
                self.add_debug_info(f"处理LWPOLYLINE焊盘实体 #{i}")
                try:
                    with entity.points() as points:
                        point_list = list(points)
                        if len(point_list) >= 4:  # 至少需要4个点形成闭合多边形
                            # 计算边界框
                            x_coords = [p[0] for p in point_list]
                            y_coords = [p[1] for p in point_list]
                            min_x, max_x = min(x_coords), max(x_coords)
                            min_y, max_y = min(y_coords), max(y_coords)
                            
                            width = max_x - min_x
                            height = max_y - min_y
                            center_x = (min_x + max_x) / 2
                            center_y = (min_y + max_y) / 2
                            
                            # 检查是否是圆形（通过点的分布判断）
                            if len(point_list) > 8:  # 多边形边数多，可能是圆形近似
                                # 计算点到中心的距离
                                distances = [math.sqrt((p[0]-center_x)**2 + (p[1]-center_y)**2) for p in point_list]
                                avg_distance = sum(distances) / len(distances)
                                variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
                                
                                if variance / (avg_distance**2) < 0.1:  # 低方差，接近圆形
                                    shape = 'circle'
                                    width = height = avg_distance * 2
                                else:
                                    shape = 'rect'
                            else:
                                shape = 'rect'
                            
                            pad_info = {
                                'name': f'Pad_{len(self.pads)+1}',
                                'type': 'LWPOLYLINE',
                                'x': center_x,
                                'y': center_y,
                                'width': width,
                                'height': height,
                                'shape': shape,
                                'points': point_list
                            }
                            self.pads.append(pad_info)
                            print(f"    添加焊盘: {center_x:.2f},{center_y:.2f} 尺寸:{width:.2f}x{height:.2f} 形状:{shape}")
                except Exception as e:
                    print(f"    处理LWPOLYLINE焊盘失败: {e}")
                    self.add_debug_info(f"LWPOLYLINE焊盘处理失败: {e}")
            
            elif entity_type == 'CIRCLE':
                print(f"  处理CIRCLE焊盘实体 #{i}")
                self.add_debug_info(f"处理CIRCLE焊盘实体 #{i}")
                try:
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    
                    pad_info = {
                        'name': f'Pad_{len(self.pads)+1}',
                        'type': 'CIRCLE',
                        'x': center[0],
                        'y': center[1],
                        'width': radius * 2,
                        'height': radius * 2,
                        'shape': 'circle',
                        'radius': radius
                    }
                    self.pads.append(pad_info)
                    print(f"    添加圆形焊盘: {center[0]:.2f},{center[1]:.2f} 半径:{radius:.2f}")
                except Exception as e:
                    print(f"    处理CIRCLE焊盘失败: {e}")
                    self.add_debug_info(f"CIRCLE焊盘处理失败: {e}")
            
            elif entity_type == 'LINE':
                print(f"  处理LINE焊盘实体 #{i}")
                self.add_debug_info(f"处理LINE焊盘实体 #{i}")
                try:
                    start = entity.dxf.start
                    end = entity.dxf.end
                    
                    # 计算直线的长度和角度
                    dx = end[0] - start[0]
                    dy = end[1] - start[1]
                    length = math.sqrt(dx*dx + dy*dy)
                    angle = math.atan2(dy, dx)
                    
                    # 假设焊盘宽度为长度的1/10
                    width = length
                    height = length * 0.1
                    
                    # 计算中心点
                    center_x = (start[0] + end[0]) / 2
                    center_y = (start[1] + end[1]) / 2
                    
                    pad_info = {
                        'name': f'Pad_{len(self.pads)+1}',
                        'type': 'LINE',
                        'x': center_x,
                        'y': center_y,
                        'width': width,
                        'height': height,
                        'angle': math.degrees(angle),
                        'shape': 'rect',
                        'length': length
                    }
                    self.pads.append(pad_info)
                    print(f"    添加线状焊盘: {center_x:.2f},{center_y:.2f} 长度:{length:.2f}")
                except Exception as e:
                    print(f"    处理LINE焊盘失败: {e}")
                    self.add_debug_info(f"LINE焊盘处理失败: {e}")
            
            elif entity_type == 'ARC':
                print(f"  处理ARC焊盘实体 #{i}")
                self.add_debug_info(f"处理ARC焊盘实体 #{i}")
                try:
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    
                    pad_info = {
                        'name': f'Pad_{len(self.pads)+1}',
                        'type': 'ARC',
                        'x': center[0],
                        'y': center[1],
                        'width': radius * 2,
                        'height': radius * 2,
                        'shape': 'circle',
                        'radius': radius
                    }
                    self.pads.append(pad_info)
                    print(f"    添加圆弧焊盘: {center[0]:.2f},{center[1]:.2f} 半径:{radius:.2f}")
                except Exception as e:
                    print(f"    处理ARC焊盘失败: {e}")
                    self.add_debug_info(f"ARC焊盘处理失败: {e}")
            
            elif entity_type in ['POLYLINE', 'POLYLINE2D', 'POLYLINE3D']:
                print(f"  处理{entity_type}焊盘实体 #{i}")
                self.add_debug_info(f"处理{entity_type}焊盘实体 #{i}")
                try:
                    points = list(entity.points())
                    if len(points) >= 4:
                        # 计算边界框
                        x_coords = [p[0] for p in points]
                        y_coords = [p[1] for p in points]
                        min_x, max_x = min(x_coords), max(x_coords)
                        min_y, max_y = min(y_coords), max(y_coords)
                        
                        width = max_x - min_x
                        height = max_y - min_y
                        center_x = (min_x + max_x) / 2
                        center_y = (min_y + max_y) / 2
                        
                        pad_info = {
                            'name': f'Pad_{len(self.pads)+1}',
                            'type': entity_type,
                            'x': center_x,
                            'y': center_y,
                            'width': width,
                            'height': height,
                            'shape': 'rect',
                            'points': points
                        }
                        self.pads.append(pad_info)
                        print(f"    添加多边形焊盘: {center_x:.2f},{center_y:.2f} 尺寸:{width:.2f}x{height:.2f}")
                except Exception as e:
                    print(f"    处理{entity_type}焊盘失败: {e}")
                    self.add_debug_info(f"{entity_type}焊盘处理失败: {e}")
            
            elif entity_type == 'ELLIPSE':
                print(f"  处理ELLIPSE焊盘实体 #{i}")
                self.add_debug_info(f"处理ELLIPSE焊盘实体 #{i}")
                try:
                    center = entity.dxf.center
                    major_axis = entity.dxf.major_axis
                    ratio = entity.dxf.ratio
                    
                    # 计算椭圆尺寸
                    width = abs(major_axis[0]) * 2
                    height = abs(major_axis[1]) * 2 * ratio
                    
                    pad_info = {
                        'name': f'Pad_{len(self.pads)+1}',
                        'type': 'ELLIPSE',
                        'x': center[0],
                        'y': center[1],
                        'width': width,
                        'height': height,
                        'shape': 'ellipse',
                        'major_axis': major_axis,
                        'ratio': ratio
                    }
                    self.pads.append(pad_info)
                    print(f"    添加椭圆焊盘: {center[0]:.2f},{center[1]:.2f} 尺寸:{width:.2f}x{height:.2f}")
                except Exception as e:
                    print(f"    处理ELLIPSE焊盘失败: {e}")
                    self.add_debug_info(f"ELLIPSE焊盘处理失败: {e}")
            
            else:
                print(f"  跳过未处理的焊盘实体类型: {entity_type} #{i}")
                self.add_debug_info(f"跳过焊盘实体类型: {entity_type}")
        
        # 去重焊盘（位置非常接近的焊盘）
        if len(self.pads) > 0:
            unique_pads = []
            seen_positions = set()
            
            for pad in self.pads:
                position_key = (round(pad['x'], 3), round(pad['y'], 3))
                if position_key not in seen_positions:
                    seen_positions.add(position_key)
                    unique_pads.append(pad)
            
            removed_count = len(self.pads) - len(unique_pads)
            if removed_count > 0:
                print(f"去重: 移除了{removed_count}个重复焊盘")
                self.add_debug_info(f"去重移除: {removed_count}个焊盘")
                self.pads = unique_pads
        
        print(f"Paste处理完成: 找到{len(self.pads)}个焊盘")
        self.add_debug_info(f"Paste处理完成: {len(self.pads)}个焊盘")
        
        return True
    
    def _calculate_bounds_from_entities(self, entities):
        """从实体计算边界"""
        all_points = []
        
        for entity in entities:
            entity_type = entity.dxftype()
            
            if entity_type == 'LWPOLYLINE':
                try:
                    with entity.points() as points:
                        all_points.extend(points)
                except:
                    pass
            elif entity_type == 'LINE':
                try:
                    all_points.append(entity.dxf.start)
                    all_points.append(entity.dxf.end)
                except:
                    pass
            elif entity_type == 'CIRCLE':
                try:
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    # 添加圆形的四个边界点
                    all_points.append((center[0] - radius, center[1] - radius))
                    all_points.append((center[0] + radius, center[1] - radius))
                    all_points.append((center[0] + radius, center[1] + radius))
                    all_points.append((center[0] - radius, center[1] + radius))
                except:
                    pass
        
        if all_points:
            # 计算边界框
            points_array = np.array(all_points)
            min_x, min_y = points_array.min(axis=0)
            max_x, max_y = points_array.max(axis=0)
            
            # 创建矩形板框
            self.board_outline = [
                (min_x, min_y),
                (max_x, min_y),
                (max_x, max_y),
                (min_x, max_y)
            ]
            print(f"从边界计算板框: {min_x:.2f},{min_y:.2f} 到 {max_x:.2f},{max_y:.2f}")
            self.add_debug_info(f"计算板框边界: {min_x:.2f},{min_y:.2f} 到 {max_x:.2f},{max_y:.2f}")
        else:
            print("无法从实体计算边界")
            self.add_debug_info("无法计算边界")
    
    def parse_edge_cuts_dxf(self, filename: str) -> bool:
        """解析Edge_Cuts.dxf文件（板框轮廓）"""
        return self.parse_dxf_file(filename, "Edge_Cuts")
    
    def parse_paste_dxf(self, filename: str) -> bool:
        """解析Paste.dxf文件（焊盘信息）"""
        return self.parse_dxf_file(filename, "Paste")
    
    def generate_stencil_stl(self, output_file: str, thickness: float = 0.1, 
                            margin: float = 5.0, aperture_clearance: float = 0.05) -> bool:
        """生成STL格式的钢网"""
        try:
            print("正在生成STL文件...")
            
            # 计算板框边界
            if self.board_outline:
                coords = np.array(self.board_outline)
                min_x, min_y = coords.min(axis=0)
                max_x, max_y = coords.max(axis=0)
            else:
                # 如果没有板框，使用焊盘边界计算
                if self.pads:
                    pad_coords = np.array([(p['x'], p['y']) for p in self.pads])
                    min_x, min_y = pad_coords.min(axis=0)
                    max_x, max_y = pad_coords.max(axis=0)
                    # 扩展边界
                    min_x -= 10
                    max_x += 10
                    min_y -= 10
                    max_y += 10
                else:
                    # 默认大小
                    min_x, min_y = -50, -50
                    max_x, max_y = 50, 50
            
            # 添加边距
            min_x -= margin
            max_x += margin
            min_y -= margin
            max_y += margin
            
            width = max_x - min_x
            height = max_y - min_y
            
            # 创建STL文件（二进制格式）
            with open(output_file, 'wb') as f:
                # 写入80字节的头部
                header = f'KiCad Stencil - Thickness: {thickness}mm'.encode('ascii')
                f.write(header + b'\x00' * (80 - len(header)))
                
                # 计算三角形数量：基板6个面 * 2个三角形 + 每个焊孔4个面 * 2个三角形
                num_triangles = 12 + len(self.pads) * 8
                f.write(struct.pack('<I', num_triangles))
                
                # 写入基板的12个三角形（立方体）
                print("正在生成基板...")
                self._write_cube_stl(f, min_x, min_y, 0, width, height, thickness)
                
                # 为每个焊盘写入孔（从基板中减去）
                if len(self.pads) > 0:
                    print(f"正在生成{len(self.pads)}个焊盘开孔...")
                    progress_bar = ProgressBar(total=len(self.pads), prefix='生成开孔:', suffix='完成')
                    
                    for i, pad in enumerate(self.pads):
                        self._write_hole_stl(f, pad, thickness, aperture_clearance)
                        progress_bar.update(i + 1)
                    
                    progress_bar.complete()
                
                # 写入属性字节计数（通常为0）
                f.write(struct.pack('<H', 0))
            
            print(f"STL文件已生成: {output_file}")
            file_size = Path(output_file).stat().st_size
            print(f"文件大小: {file_size / 1024:.2f} KB ({file_size} 字节)")
            
            # 显示统计信息
            print(f"\n钢网统计信息:")
            print(f"- 尺寸: {width:.2f} x {height:.2f} mm")
            print(f"- 厚度: {thickness:.3f} mm")
            print(f"- 焊盘数量: {len(self.pads)}")
            print(f"- 开孔间隙: {aperture_clearance:.3f} mm")
            
            return True
            
        except Exception as e:
            print(f"生成STL失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _write_cube_stl(self, f, x: float, y: float, z: float, 
                       width: float, height: float, depth: float):
        """写入立方体的三角形到STL文件"""
        # 顶点坐标
        vertices = [
            (x, y, z),
            (x + width, y, z),
            (x + width, y + height, z),
            (x, y + height, z),
            (x, y, z + depth),
            (x + width, y, z + depth),
            (x + width, y + height, z + depth),
            (x, y + height, z + depth)
        ]
        
        # 立方体的12个三角形（每个面2个），每个三角形需要正确的法向量
        faces = [
            # 底面 (z=0)
            (0, 2, 1), (0, 3, 2),
            # 顶面 (z=depth)
            (4, 5, 6), (4, 6, 7),
            # 前面 (y=y)
            (0, 1, 5), (0, 5, 4),
            # 后面 (y=y+height)
            (3, 6, 2), (3, 7, 6),
            # 右面 (x=x+width)
            (1, 2, 6), (1, 6, 5),
            # 左面 (x=x)
            (0, 4, 7), (0, 7, 3)
        ]
        
        # 每个面对应的法向量
        normals = [
            (0, 0, -1), (0, 0, -1),     # 底面
            (0, 0, 1), (0, 0, 1),       # 顶面
            (0, -1, 0), (0, -1, 0),     # 前面
            (0, 1, 0), (0, 1, 0),       # 后面
            (1, 0, 0), (1, 0, 0),       # 右面
            (-1, 0, 0), (-1, 0, 0)      # 左面
        ]
        
        for face_idx, face in enumerate(faces):
            normal = normals[face_idx]
            f.write(struct.pack('<fff', *normal))
            for vertex_idx in face:
                vertex = vertices[vertex_idx]
                f.write(struct.pack('<fff', *vertex))
            f.write(struct.pack('<H', 0))
    
    def _write_hole_stl(self, f, pad: Dict[str, Any], thickness: float, clearance: float):
        """写入焊盘孔到STL文件"""
        # 根据焊盘形状计算孔的大小
        if pad.get('shape', 'rect') == 'circle':
            # 圆形焊盘：创建圆柱形孔
            radius = (pad['width'] / 2) + clearance
            center_x, center_y = pad['x'], pad['y']
            
            # 近似圆形为多边形（16边形）
            num_segments = 16
            angles = np.linspace(0, 2*math.pi, num_segments, endpoint=False)
            
            # 生成孔的顶点（上下两层）
            bottom_vertices = []
            top_vertices = []
            
            for angle in angles:
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                bottom_vertices.append((x, y, -0.1))  # 稍微向下延伸
                top_vertices.append((x, y, thickness + 0.1))  # 稍微向上延伸
            
            # 创建侧面三角形（连接上下两层的顶点）
            for i in range(num_segments):
                next_i = (i + 1) % num_segments
                
                # 侧面四边形分解为两个三角形
                # 三角形1
                v0 = bottom_vertices[i]
                v1 = bottom_vertices[next_i]
                v2 = top_vertices[i]
                
                # 计算法向量
                normal = self._calculate_normal(v0, v1, v2)
                f.write(struct.pack('<fff', *normal))
                f.write(struct.pack('<fff', *v0))
                f.write(struct.pack('<fff', *v1))
                f.write(struct.pack('<fff', *v2))
                f.write(struct.pack('<H', 0))
                
                # 三角形2
                v0 = top_vertices[i]
                v1 = bottom_vertices[next_i]
                v2 = top_vertices[next_i]
                
                normal = self._calculate_normal(v0, v1, v2)
                f.write(struct.pack('<fff', *normal))
                f.write(struct.pack('<fff', *v0))
                f.write(struct.pack('<fff', *v1))
                f.write(struct.pack('<fff', *v2))
                f.write(struct.pack('<H', 0))
            
            # 创建底面和顶面（用三角形扇）
            # 底面中心点
            bottom_center = (center_x, center_y, -0.1)
            # 顶面中心点
            top_center = (center_x, center_y, thickness + 0.1)
            
            # 底面三角形扇
            for i in range(num_segments):
                next_i = (i + 1) % num_segments
                
                normal = (0, 0, -1)  # 向下的法向量
                f.write(struct.pack('<fff', *normal))
                f.write(struct.pack('<fff', *bottom_center))
                f.write(struct.pack('<fff', *bottom_vertices[next_i]))
                f.write(struct.pack('<fff', *bottom_vertices[i]))
                f.write(struct.pack('<H', 0))
            
            # 顶面三角形扇
            for i in range(num_segments):
                next_i = (i + 1) % num_segments
                
                normal = (0, 0, 1)  # 向上的法向量
                f.write(struct.pack('<fff', *normal))
                f.write(struct.pack('<fff', *top_center))
                f.write(struct.pack('<fff', *top_vertices[i]))
                f.write(struct.pack('<fff', *top_vertices[next_i]))
                f.write(struct.pack('<H', 0))
        else:
            # 矩形焊盘
            hole_width = pad['width'] + clearance * 2
            hole_height = pad['height'] + clearance * 2
            x = pad['x'] - hole_width / 2
            y = pad['y'] - hole_height / 2
            
            # 孔的8个顶点（立方体孔）
            vertices = [
                (x, y, -0.1),  # 稍微向下延伸以确保穿透
                (x + hole_width, y, -0.1),
                (x + hole_width, y + hole_height, -0.1),
                (x, y + hole_height, -0.1),
                (x, y, thickness + 0.1),  # 稍微向上延伸
                (x + hole_width, y, thickness + 0.1),
                (x + hole_width, y + hole_height, thickness + 0.1),
                (x, y + hole_height, thickness + 0.1)
            ]
            
            # 立方体的12个三角形
            faces = [
                (0, 1, 2), (0, 2, 3),  # 底面
                (4, 6, 5), (4, 7, 6),  # 顶面
                (0, 5, 1), (0, 4, 5),  # 前面
                (1, 6, 2), (1, 5, 6),  # 右面
                (2, 7, 3), (2, 6, 7),  # 后面
                (3, 4, 0), (3, 7, 4)   # 左面
            ]
            
            # 每个面对应的法向量
            normals = [
                (0, 0, -1), (0, 0, -1),   # 底面
                (0, 0, 1), (0, 0, 1),     # 顶面
                (0, -1, 0), (0, -1, 0),   # 前面
                (1, 0, 0), (1, 0, 0),     # 右面
                (0, 1, 0), (0, 1, 0),     # 后面
                (-1, 0, 0), (-1, 0, 0)    # 左面
            ]
            
            for face_idx, face in enumerate(faces):
                normal = normals[face_idx]
                f.write(struct.pack('<fff', *normal))
                for vertex_idx in face:
                    vertex = vertices[vertex_idx]
                    f.write(struct.pack('<fff', *vertex))
                f.write(struct.pack('<H', 0))
    
    def _calculate_normal(self, v0, v1, v2):
        """计算三角形法向量"""
        # 计算两个边向量
        u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
        v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
        
        # 计算叉积
        normal = (
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        )
        
        # 归一化
        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if length > 0:
            normal = (normal[0]/length, normal[1]/length, normal[2]/length)
        
        return normal
    
    def generate_stencil_step(self, output_file: str, thickness: float = 0.1,
                             margin: float = 5.0, aperture_clearance: float = 0.05) -> bool:
        """生成STEP格式的钢网"""
        try:
            print("正在生成STEP文件...")
            progress_bar = ProgressBar(total=100, prefix='生成STEP:', suffix='完成')
            
            progress_bar.update(10)
            
            # 计算板框边界
            if self.board_outline:
                coords = np.array(self.board_outline)
                min_x, min_y = coords.min(axis=0)
                max_x, max_y = coords.max(axis=0)
            else:
                # 如果没有板框，使用焊盘边界计算
                if self.pads:
                    pad_coords = np.array([(p['x'], p['y']) for p in self.pads])
                    min_x, min_y = pad_coords.min(axis=0)
                    max_x, max_y = pad_coords.max(axis=0)
                    # 扩展边界
                    min_x -= 10
                    max_x += 10
                    min_y -= 10
                    max_y += 10
                else:
                    # 默认大小
                    min_x, min_y = -50, -50
                    max_x, max_y = 50, 50
            
            progress_bar.update(20)
            
            # 添加边距
            min_x -= margin
            max_x += margin
            min_y -= margin
            max_y += margin
            
            width = max_x - min_x
            height = max_y - min_y
            
            progress_bar.update(30)
            
            # 创建STEP文件内容
            step_content = self._create_step_content(
                min_x, min_y, width, height, thickness,
                self.pads, aperture_clearance
            )
            
            progress_bar.update(80)
            
            # 保存STEP文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(step_content)
            
            progress_bar.complete()
            
            print(f"STEP文件已生成: {output_file}")
            file_size = Path(output_file).stat().st_size
            print(f"文件大小: {file_size / 1024:.2f} KB")
            
            # 显示统计信息
            print(f"\n钢网统计信息:")
            print(f"- 尺寸: {width:.2f} x {height:.2f} mm")
            print(f"- 厚度: {thickness:.3f} mm")
            print(f"- 焊盘数量: {len(self.pads)}")
            print(f"- 开孔间隙: {aperture_clearance:.3f} mm")
            
            return True
            
        except Exception as e:
            print(f"生成STEP失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_step_content(self, min_x, min_y, width, height, thickness, pads, clearance):
        """创建STEP文件内容"""
        # 生成简单的STEP文件（不带孔）
        # 这是一个简化的STEP文件，只包含一个立方体
        # 更复杂的STEP文件（带孔）需要更复杂的STEP语法
        
        # 计算立方体的8个顶点
        x1, y1, z1 = min_x, min_y, 0
        x2, y2, z2 = min_x + width, min_y + height, thickness
        
        step_content = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('KiCad Stencil'), '2;1');
FILE_NAME('stencil', '{time.strftime("%Y-%m-%dT%H:%M:%S")}', ('User'), ('Organization'), 'KiCad Stencil Generator', 'v1.0', '');
FILE_SCHEMA(('CONFIG_CONTROL_DESIGN'));
ENDSEC;

DATA;

#10 = CARTESIAN_POINT('', ({x1:.6f}, {y1:.6f}, {z1:.6f}));
#20 = CARTESIAN_POINT('', ({x2:.6f}, {y1:.6f}, {z1:.6f}));
#30 = CARTESIAN_POINT('', ({x2:.6f}, {y2:.6f}, {z1:.6f}));
#40 = CARTESIAN_POINT('', ({x1:.6f}, {y2:.6f}, {z1:.6f}));
#50 = CARTESIAN_POINT('', ({x1:.6f}, {y1:.6f}, {z2:.6f}));
#60 = CARTESIAN_POINT('', ({x2:.6f}, {y1:.6f}, {z2:.6f}));
#70 = CARTESIAN_POINT('', ({x2:.6f}, {y2:.6f}, {z2:.6f}));
#80 = CARTESIAN_POINT('', ({x1:.6f}, {y2:.6f}, {z2:.6f}));

#90 = DIRECTION('', (0.0, 0.0, 1.0));
#100 = DIRECTION('', (1.0, 0.0, 0.0));
#110 = AXIS2_PLACEMENT_3D('', #10, #90, #100);

#120 = VERTEX_POINT('', #10);
#130 = VERTEX_POINT('', #20);
#140 = VERTEX_POINT('', #30);
#150 = VERTEX_POINT('', #40);
#160 = VERTEX_POINT('', #50);
#170 = VERTEX_POINT('', #60);
#180 = VERTEX_POINT('', #70);
#190 = VERTEX_POINT('', #80);

#200 = LINE('', #10, #100);
#210 = LINE('', #20, #100);
#220 = LINE('', #30, #100);
#230 = LINE('', #40, #100);
#240 = LINE('', #50, #100);
#250 = LINE('', #60, #100);
#260 = LINE('', #70, #100);
#270 = LINE('', #80, #100);

#280 = EDGE_CURVE('', #120, #130, #200, .T.);
#290 = EDGE_CURVE('', #130, #140, #210, .T.);
#300 = EDGE_CURVE('', #140, #150, #220, .T.);
#310 = EDGE_CURVE('', #150, #120, #230, .T.);
#320 = EDGE_CURVE('', #160, #170, #240, .T.);
#330 = EDGE_CURVE('', #170, #180, #250, .T.);
#340 = EDGE_CURVE('', #180, #190, #260, .T.);
#350 = EDGE_CURVE('', #190, #160, #270, .T.);
#360 = EDGE_CURVE('', #120, #160, #200, .T.);
#370 = EDGE_CURVE('', #130, #170, #210, .T.);
#380 = EDGE_CURVE('', #140, #180, #220, .T.);
#390 = EDGE_CURVE('', #150, #190, #230, .T.);

#400 = ORIENTED_EDGE('', *, *, #280, .T.);
#410 = ORIENTED_EDGE('', *, *, #290, .T.);
#420 = ORIENTED_EDGE('', *, *, #300, .T.);
#430 = ORIENTED_EDGE('', *, *, #310, .T.);
#440 = ORIENTED_EDGE('', *, *, #320, .T.);
#450 = ORIENTED_EDGE('', *, *, #330, .T.);
#460 = ORIENTED_EDGE('', *, *, #340, .T.);
#470 = ORIENTED_EDGE('', *, *, #350, .T.);
#480 = ORIENTED_EDGE('', *, *, #360, .T.);
#490 = ORIENTED_EDGE('', *, *, #370, .T.);
#500 = ORIENTED_EDGE('', *, *, #380, .T.);
#510 = ORIENTED_EDGE('', *, *, #390, .T.);

#520 = EDGE_LOOP('', (#400, #410, #420, #430));
#530 = EDGE_LOOP('', (#440, #450, #460, #470));
#540 = EDGE_LOOP('', (#400, #480, #440, #490));
#550 = EDGE_LOOP('', (#410, #490, #450, #500));
#560 = EDGE_LOOP('', (#420, #500, #460, #510));
#570 = EDGE_LOOP('', (#430, #510, #470, #480));

#580 = FACE_OUTER_BOUND('', #520, .T.);
#590 = FACE_OUTER_BOUND('', #530, .T.);
#600 = FACE_OUTER_BOUND('', #540, .T.);
#610 = FACE_OUTER_BOUND('', #550, .T.);
#620 = FACE_OUTER_BOUND('', #560, .T.);
#630 = FACE_OUTER_BOUND('', #570, .T.);

#640 = PLANE('', #110);
#650 = ADVANCED_FACE('', (#580,), #640, .T.);
#660 = ADVANCED_FACE('', (#590,), #640, .T.);
#670 = ADVANCED_FACE('', (#600,), #640, .T.);
#680 = ADVANCED_FACE('', (#610,), #640, .T.);
#690 = ADVANCED_FACE('', (#620,), #640, .T.);
#700 = ADVANCED_FACE('', (#630,), #640, .T.);

#710 = CLOSED_SHELL('', (#650, #660, #670, #680, #690, #700));
#720 = MANIFOLD_SOLID_BREP('', #710);
#730 = SHAPE_REPRESENTATION('', (#720,), #10);
#740 = PRODUCT_DEFINITION_CONTEXT('', 'part', #10);
#750 = PRODUCT_DEFINITION('', 'stencil', #720, #740);
#760 = NEXT_ASSEMBLY_USAGE_OCCURRENCE('', 'stencil_assembly', '', #750, #750);

ENDSEC;
END-ISO-10303-21;
"""
        
        # 添加注释信息
        comment = f"\n/*\n钢网信息:\n"
        comment += f"尺寸: {width:.2f} x {height:.2f} x {thickness:.2f} mm\n"
        comment += f"焊盘数量: {len(pads)}\n"
        comment += f"开孔间隙: {clearance:.3f} mm\n"
        comment += f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        comment += f"*/\n"
        
        return comment + step_content
    
    def generate_2d_svg(self, output_file: str, margin: float = 5.0, 
                       aperture_clearance: float = 0.05) -> bool:
        """生成2D SVG文件（用于激光切割）"""
        try:
            print("正在生成SVG文件...")
            progress_bar = ProgressBar(total=100, prefix='生成SVG:', suffix='完成')
            
            progress_bar.update(10)
            
            # 计算板框边界
            if self.board_outline:
                coords = np.array(self.board_outline)
                min_x, min_y = coords.min(axis=0)
                max_x, max_y = coords.max(axis=0)
            else:
                # 如果没有板框，使用焊盘边界
                if self.pads:
                    pad_coords = np.array([(p['x'], p['y']) for p in self.pads])
                    min_x, min_y = pad_coords.min(axis=0)
                    max_x, max_y = pad_coords.max(axis=0)
                    # 扩展边界
                    min_x -= 10
                    max_x += 10
                    min_y -= 10
                    max_y += 10
                else:
                    min_x, min_y = -50, -50
                    max_x, max_y = 50, 50
            
            progress_bar.update(20)
            
            # 添加边距
            min_x -= margin
            max_x += margin
            min_y -= margin
            max_y += margin
            
            width = max_x - min_x
            height = max_y - min_y
            
            progress_bar.update(30)
            
            # 创建SVG
            svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{width}mm" height="{height}mm" viewBox="{min_x} {min_y} {width} {height}"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
    
    <!-- 钢网边框 -->
    <rect x="{min_x}" y="{min_y}" width="{width}" height="{height}" 
          fill="none" stroke="black" stroke-width="0.1"/>
    
    <!-- 板框轮廓 -->
'''
            
            progress_bar.update(40)
            
            # 添加板框轮廓（如果存在）
            if self.board_outline and len(self.board_outline) > 2:
                points_str = ' '.join([f"{x},{y}" for x, y in self.board_outline])
                svg_content += f'    <polygon points="{points_str}" fill="none" stroke="blue" stroke-width="0.05"/>\n'
            
            svg_content += '    <!-- 焊盘开孔 -->\n'
            
            progress_bar.update(50)
            
            if len(self.pads) > 0:
                print(f"正在生成{len(self.pads)}个焊盘开孔...")
            
            # 添加焊盘开孔
            for i, pad in enumerate(self.pads):
                if pad.get('shape', 'rect') == 'circle':
                    # 圆形开孔
                    radius = (pad['width'] / 2) + aperture_clearance
                    svg_content += f'    <circle cx="{pad["x"]}" cy="{pad["y"]}" r="{radius}" fill="black"/>\n'
                else:
                    # 矩形开孔
                    hole_width = pad['width'] + aperture_clearance * 2
                    hole_height = pad['height'] + aperture_clearance * 2
                    x = pad['x'] - hole_width / 2
                    y = pad['y'] - hole_height / 2
                    svg_content += f'    <rect x="{x}" y="{y}" width="{hole_width}" height="{hole_height}" fill="black"/>\n'
                
                # 更新进度
                if i % 100 == 0 and len(self.pads) > 0:
                    progress = 50 + int(40 * (i / len(self.pads)))
                    progress_bar.update(progress)
            
            svg_content += '</svg>'
            
            progress_bar.update(90)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            progress_bar.complete()
            
            print(f"SVG文件已生成: {output_file}")
            file_size = Path(output_file).stat().st_size
            print(f"文件大小: {file_size / 1024:.2f} KB")
            print("SVG文件可用于激光切割或CNC加工")
            
            return True
            
        except Exception as e:
            print(f"生成SVG失败: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='DXF钢网生成器 - 增强版')
    parser.add_argument('edge_cuts', help='Edge_Cuts.dxf文件（板框轮廓）')
    parser.add_argument('paste', help='Paste.dxf文件（焊盘信息）')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-t', '--thickness', type=float, default=0.1,
                       help='钢网厚度(mm)，默认0.1mm')
    parser.add_argument('-m', '--margin', type=float, default=5.0,
                       help='边框距离(mm)，默认5.0mm')
    parser.add_argument('-c', '--clearance', type=float, default=0.05,
                       help='开孔比焊盘扩大的间隙(mm)，默认0.05mm')
    parser.add_argument('--format', choices=['step', 'stl', 'svg', 'all'],
                       default='step', help='输出格式，默认step')
    parser.add_argument('--debug', action='store_true',
                       help='显示详细调试信息')
    parser.add_argument('--list-entities', action='store_true',
                       help='列出DXF文件中的所有实体')
    parser.add_argument('--test', action='store_true',
                       help='测试模式，只解析不生成')
    
    args = parser.parse_args()
    
    # 检查输入文件
    edge_cuts_path = Path(args.edge_cuts)
    paste_path = Path(args.paste)
    
    if not edge_cuts_path.exists():
        print(f"错误: Edge_Cuts.dxf文件不存在 - {args.edge_cuts}")
        return 1
    
    if not paste_path.exists():
        print(f"错误: Paste.dxf文件不存在 - {args.paste}")
        return 1
    
    print(f"输入文件:")
    print(f"  板框: {args.edge_cuts} ({edge_cuts_path.stat().st_size} 字节)")
    print(f"  焊盘: {args.paste} ({paste_path.stat().st_size} 字节)")
    
    # 创建生成器
    generator = DXFStencilGenerator()
    
    # 解析Edge_Cuts.dxf
    print("\n" + "="*60)
    print("解析Edge_Cuts.dxf文件")
    print("="*60)
    
    if not generator.parse_edge_cuts_dxf(args.edge_cuts):
        print("解析Edge_Cuts.dxf失败")
        if args.debug:
            generator.print_debug_info()
        return 1
    
    # 解析Paste.dxf
    print("\n" + "="*60)
    print("解析Paste.dxf文件")
    print("="*60)
    
    if not generator.parse_paste_dxf(args.paste):
        print("解析Paste.dxf失败")
        if args.debug:
            generator.print_debug_info()
        return 1
    
    # 打印解析结果
    print(f"\n解析结果:")
    print(f"  板框轮廓点: {len(generator.board_outline)}个")
    print(f"  焊盘数量: {len(generator.pads)}个")
    
    if len(generator.pads) == 0:
        print("警告: 未找到焊盘信息，生成的钢网将没有开孔")
    
    if args.debug:
        generator.print_debug_info()
    
    if args.test:
        print("\n测试模式完成，不生成文件")
        return 0
    
    # 设置输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        base_name = edge_cuts_path.stem.replace('Edge_Cuts', 'Stencil')
        if args.format == 'step':
            output_path = Path(f"{base_name}.step")
        elif args.format == 'stl':
            output_path = Path(f"{base_name}.stl")
        elif args.format == 'svg':
            output_path = Path(f"{base_name}.svg")
        else:
            output_path = Path(f"{base_name}.step")
    
    # 生成文件
    print("\n" + "="*60)
    print(f"开始生成{args.format.upper()}格式文件")
    print("="*60)
    
    success = False
    
    if args.format == 'step' or args.format == 'all':
        step_file = output_path.with_suffix('.step') if args.format == 'all' else output_path
        print(f"输出STEP文件: {step_file}")
        print(f"参数: 厚度={args.thickness}mm, 边距={args.margin}mm, 间隙={args.clearance}mm")
        
        if generator.generate_stencil_step(str(step_file), args.thickness, 
                                         args.margin, args.clearance):
            success = True
    
    if args.format == 'stl' or args.format == 'all':
        stl_file = output_path.with_suffix('.stl') if args.format == 'all' else output_path
        print(f"输出STL文件: {stl_file}")
        print(f"参数: 厚度={args.thickness}mm, 边距={args.margin}mm, 间隙={args.clearance}mm")
        
        if generator.generate_stencil_stl(str(stl_file), args.thickness, 
                                         args.margin, args.clearance):
            success = True
    
    if args.format == 'svg' or args.format == 'all':
        svg_file = output_path.with_suffix('.svg') if args.format == 'all' else output_path
        print(f"输出SVG文件: {svg_file}")
        
        if generator.generate_2d_svg(str(svg_file), args.margin, args.clearance):
            success = True
    
    if success:
        print("\n" + "="*60)
        print("生成完成！")
        print("="*60)
        print("\n使用建议:")
        if args.format == 'step' or args.format == 'all':
            print("1. STEP文件可用于3D CAD软件（如FreeCAD、Fusion 360、SolidWorks）")
        if args.format == 'stl' or args.format == 'all':
            print("2. STL文件可用于3D打印（建议使用SLA/DLP打印机）")
        if args.format == 'svg' or args.format == 'all':
            print("3. SVG文件可用于激光切割或CNC加工")
        print("\n3D打印参数建议:")
        print(f"  层高: {args.thickness/4:.3f}mm 或更小")
        print("  填充: 100%（实心）")
        print("  支撑: 不需要（钢网是平的）")
        print("  材料: 树脂（SLA）或精细PLA（FDM）")
        return 0
    else:
        print("\n生成失败，请检查错误信息")
        return 1

if __name__ == '__main__':
    # 检查ezdxf是否已安装
    try:
        import ezdxf
        print(f"ezdxf版本: {ezdxf.__version__}")
    except ImportError:
        print("错误: 需要安装ezdxf库")
        print("请运行: pip install ezdxf")
        sys.exit(1)
    
    sys.exit(main())