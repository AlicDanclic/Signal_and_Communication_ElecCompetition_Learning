from manim import *
import numpy as np

class ConformalMapping(ThreeDScene):
    def construct(self):
        # 标题移动到左上角
        title = Text("共形映射可视化", font_size=36, color=BLUE)
        title.to_corner(UL, buff=0.5)
        subtitle = Text("Conformal Mapping", font_size=24, color=WHITE)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)
        
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # 第一部分：复数平面基础
        self.show_complex_plane(title, subtitle)
        
        # 第二部分：共形映射示例
        self.show_conformal_mapping_examples(title, subtitle)
        
        # 第三部分：双线性变换
        self.show_bilinear_transform(title, subtitle)
    
    def show_complex_plane(self, title, subtitle):
        """显示复数平面"""
        # 更新标题
        new_title = Text("复数平面", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        new_subtitle = Text("Complex Plane", font_size=20, color=WHITE)
        new_subtitle.next_to(new_title, DOWN, aligned_edge=LEFT)
        
        self.play(
            Transform(title, new_title),
            Transform(subtitle, new_subtitle)
        )
        self.wait(0.5)
        
        # 创建复数平面
        complex_plane = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).shift(DOWN*0.5)
        
        # 坐标轴标签
        x_label = MathTex("\\text{Re}(z)", font_size=24)
        y_label = MathTex("\\text{Im}(z)", font_size=24)
        x_label.next_to(complex_plane.x_axis, RIGHT)
        y_label.next_to(complex_plane.y_axis, UP)
        
        # 添加网格点
        grid_lines = VGroup()
        for x in np.arange(-4, 4.1, 0.5):
            for y in np.arange(-4, 4.1, 0.5):
                point = complex_plane.coords_to_point(x, y)
                grid_lines.add(Dot(point, color=GRAY, radius=0.02))
        
        # 几个示例点
        points_data = [
            (1, 1, "1+i", RED),
            (-2, 1, "-2+i", GREEN),
            (0, 3, "3i", BLUE),
            (2, -2, "2-2i", YELLOW),
        ]
        
        points_group = VGroup()
        for x, y, label, color in points_data:
            point = complex_plane.coords_to_point(x, y)
            dot = Dot(point, color=color, radius=0.08)
            label_text = MathTex(label, font_size=20, color=color)
            label_text.next_to(point, UR, buff=0.1)
            points_group.add(VGroup(dot, label_text))
        
        self.play(
            Create(complex_plane),
            Write(x_label),
            Write(y_label),
            FadeIn(grid_lines, lag_ratio=0.1)
        )
        self.wait()
        
        # 展示点
        for point_group in points_group:
            self.play(FadeIn(point_group))
            self.wait(0.5)
        
        self.wait(2)
        
        # 清理
        self.play(
            FadeOut(complex_plane),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(grid_lines),
            FadeOut(points_group)
        )
    
    def show_conformal_mapping_examples(self, title, subtitle):
        """显示共形映射示例"""
        # 更新标题
        new_title = Text("共形映射示例", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        new_subtitle = MathTex("w = f(z)", font_size=24, color=GREEN)
        new_subtitle.next_to(new_title, DOWN, aligned_edge=LEFT)
        
        self.play(
            Transform(title, new_title),
            Transform(subtitle, new_subtitle)
        )
        self.wait(0.5)
        
        # 创建两个复数平面
        z_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.3
            }
        ).to_edge(LEFT).shift(DOWN*0.5)
        
        w_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": RED_E,
                "stroke_opacity": 0.3
            }
        ).to_edge(RIGHT).shift(DOWN*0.5)
        
        z_label = MathTex("z\\text{-plane}", font_size=20, color=BLUE)
        w_label = MathTex("w\\text{-plane}", font_size=20, color=RED)
        z_label.next_to(z_plane, DOWN)
        w_label.next_to(w_plane, DOWN)
        
        # 映射箭头
        arrow = Arrow(z_plane.get_right(), w_plane.get_left(), 
                     color=GREEN, buff=0.5)
        
        self.play(
            Create(z_plane),
            Create(w_plane),
            Write(z_label),
            Write(w_label),
            GrowArrow(arrow)
        )
        self.wait()
        
        # 示例1：w = z^2
        example1_title = MathTex("w = z^2", font_size=24, color=PURPLE)
        example1_title.to_corner(UL, buff=0.5).shift(DOWN*1.2)
        self.play(Write(example1_title))
        
        # 在z平面创建网格
        z_grid = self.create_complex_grid(z_plane)
        
        # 动画展示映射 w = z^2
        self.animate_mapping(z_plane, w_plane, z_grid, 
                           lambda z: z**2, "w = z^2", color=RED)
        
        self.wait(2)
        
        # 清理示例1
        self.play(FadeOut(example1_title))
        
        # 示例2：w = e^z
        example2_title = MathTex("w = e^z", font_size=24, color=PURPLE)
        example2_title.to_corner(UL, buff=0.5).shift(DOWN*1.2)
        self.play(Write(example2_title))
        
        # 重新创建网格
        z_grid2 = self.create_complex_grid(z_plane, range_limit=(-2, 2, -2, 2))
        
        # 动画展示映射 w = e^z
        self.animate_mapping(z_plane, w_plane, z_grid2,
                           lambda z: np.exp(z), "w = e^z", color=BLUE)
        
        self.wait(2)
        
        # 清理
        self.play(
            FadeOut(example2_title),
            FadeOut(z_plane),
            FadeOut(w_plane),
            FadeOut(z_label),
            FadeOut(w_label),
            FadeOut(arrow)
        )
    
    def create_complex_grid(self, plane, range_limit=None):
        """创建复数网格"""
        grid = VGroup()
        
        if range_limit is None:
            x_min, x_max, y_min, y_max = -2, 2, -2, 2
        else:
            x_min, x_max, y_min, y_max = range_limit
        
        # 垂直线
        for x in np.linspace(x_min, x_max, 9):
            line_points = []
            for y in np.linspace(y_min, y_max, 50):
                point = plane.coords_to_point(x, y)
                line_points.append(point)
            
            if len(line_points) > 1:
                line = VMobject()
                line.set_points_smoothly(line_points)
                line.set_stroke(color=GRAY, width=1, opacity=0.8)
                grid.add(line)
        
        # 水平线
        for y in np.linspace(y_min, y_max, 9):
            line_points = []
            for x in np.linspace(x_min, x_max, 50):
                point = plane.coords_to_point(x, y)
                line_points.append(point)
            
            if len(line_points) > 1:
                line = VMobject()
                line.set_points_smoothly(line_points)
                line.set_stroke(color=GRAY, width=1, opacity=0.8)
                grid.add(line)
        
        return grid
    
    def animate_mapping(self, z_plane, w_plane, z_grid, func, 
                       func_text, color=RED):
        """动画展示映射过程"""
        # 在z平面显示网格
        self.play(Create(z_grid, run_time=2))
        self.wait()
        
        # 计算映射后的点
        w_points = []
        for mobj in z_grid:
            if isinstance(mobj, VMobject):
                points = mobj.get_points()
                mapped_points = []
                for point in points:
                    # 将点坐标转换为复数
                    z_coords = z_plane.point_to_coords(point)
                    if z_coords is not None:
                        x, y = z_coords
                        z = complex(x, y)
                        # 应用映射
                        w = func(z)
                        # 将结果映射回w平面
                        w_point = w_plane.coords_to_point(w.real, w.imag)
                        mapped_points.append(w_point)
                
                # 创建映射后的线
                if len(mapped_points) > 1:
                    mapped_line = VMobject()
                    mapped_line.set_points_smoothly(mapped_points)
                    mapped_line.set_stroke(color=color, width=2, opacity=0.8)
                    w_points.append(mapped_line)
        
        w_grid_mapped = VGroup(*w_points)
        
        # 显示映射后的网格
        self.play(Create(w_grid_mapped, run_time=3))
        
        # 强调几个关键点
        test_points = [
            (1, 0, "1"),
            (0, 1, "i"),
            (-1, 0, "-1"),
            (0, -1, "-i"),
        ]
        
        for x, y, label in test_points:
            # z平面点
            z_point = z_plane.coords_to_point(x, y)
            z_dot = Dot(z_point, color=YELLOW, radius=0.08)
            z_label = MathTex(label, font_size=18, color=YELLOW)
            z_label.next_to(z_point, UR, buff=0.1)
            
            # w平面点
            w = func(complex(x, y))
            w_point = w_plane.coords_to_point(w.real, w.imag)
            w_dot = Dot(w_point, color=ORANGE, radius=0.08)
            w_label = MathTex(f"{w.real:.1f}+{w.imag:.1f}i", font_size=18, color=ORANGE)
            w_label.next_to(w_point, UR, buff=0.1)
            
            self.play(
                FadeIn(z_dot), Write(z_label),
                FadeIn(w_dot), Write(w_label)
            )
            self.wait(0.5)
            self.play(FadeOut(z_dot), FadeOut(z_label),
                     FadeOut(w_dot), FadeOut(w_label))
        
        self.wait(2)
        
        # 清理
        self.play(
            FadeOut(z_grid),
            FadeOut(w_grid_mapped)
        )
    
    def show_bilinear_transform(self, title, subtitle):
        """显示双线性变换"""
        # 更新标题
        new_title = Text("双线性变换", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        new_subtitle = Text("Bilinear Transform", font_size=20, color=WHITE)
        new_subtitle.next_to(new_title, DOWN, aligned_edge=LEFT)
        
        self.play(
            Transform(title, new_title),
            Transform(subtitle, new_subtitle)
        )
        self.wait(0.5)
        
        # 双线性变换公式
        formula = MathTex(
            "s = \\frac{2}{T} \\cdot \\frac{1 - z^{-1}}{1 + z^{-1}}",
            font_size=28, color=GREEN
        )
        formula.next_to(subtitle, DOWN, aligned_edge=LEFT)
        self.play(Write(formula))
        
        # 创建两个平面：s平面（连续），z平面（离散）
        s_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.3
            }
        ).to_edge(LEFT).shift(DOWN*1)
        
        z_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": RED_E,
                "stroke_opacity": 0.3
            }
        ).to_edge(RIGHT).shift(DOWN*1)
        
        s_label = MathTex("s\\text{-plane}", font_size=20, color=BLUE)
        z_label = MathTex("z\\text{-plane}", font_size=20, color=RED)
        s_label.next_to(s_plane, DOWN)
        z_label.next_to(z_plane, DOWN)
        
        # 映射说明
        mapping_info = VGroup(
            Text("映射关系：", font_size=18, color=WHITE),
            Text("s左半平面 → z单位圆内", font_size=16, color=BLUE),
            Text("s虚轴 → z单位圆", font_size=16, color=YELLOW),
            Text("s右半平面 → z单位圆外", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        mapping_info.to_corner(UR, buff=0.5)
        
        self.play(
            Create(s_plane),
            Create(z_plane),
            Write(s_label),
            Write(z_label),
            Write(mapping_info)
        )
        self.wait()
        
        # 在s平面绘制左半平面
        left_half = Polygon(
            s_plane.coords_to_point(-3, -3),
            s_plane.coords_to_point(0, -3),
            s_plane.coords_to_point(0, 3),
            s_plane.coords_to_point(-3, 3),
            color=BLUE, fill_opacity=0.2, stroke_width=0
        )
        
        # 在z平面绘制单位圆
        unit_circle = Circle(
            radius=z_plane.coords_to_point(1, 0)[0] - z_plane.coords_to_point(0, 0)[0],
            color=RED, stroke_width=3
        )
        unit_circle.move_to(z_plane.coords_to_point(0, 0))
        unit_circle_interior = Circle(
            radius=z_plane.coords_to_point(1, 0)[0] - z_plane.coords_to_point(0, 0)[0],
            color=RED, fill_opacity=0.2, stroke_width=0
        )
        unit_circle_interior.move_to(z_plane.coords_to_point(0, 0))
        
        self.play(FadeIn(left_half))
        self.play(Create(unit_circle), FadeIn(unit_circle_interior))
        
        self.wait(1)
        
        # 示例点映射动画
        example_points = [
            (-1, 0, "稳定极点", BLUE),
            (-2, 1, "复极点", GREEN),
            (0, 2, "虚轴上", YELLOW),
            (1.5, 0, "不稳定极点", RED),
        ]
        
        for sx, sy, label, color in example_points:
            # s平面点
            s_point = s_plane.coords_to_point(sx, sy)
            s_dot = Dot(s_point, color=color, radius=0.07)
            s_label = MathTex(f"{sx}{'+' if sy>=0 else ''}{sy}i", font_size=16, color=color)
            s_label.next_to(s_point, UR, buff=0.1)
            
            # 计算z平面对应点（简化映射，假设T=2）
            s = complex(sx, sy)
            
            # 避免除零
            if abs(1 - s) > 1e-10:
                z = (1 + s) / (1 - s)
            else:
                continue
            
            if abs(z) < 10:  # 避免过大点
                # z平面点
                z_point = z_plane.coords_to_point(z.real, z.imag)
                z_dot = Dot(z_point, color=color, radius=0.07)
                z_label = MathTex(f"{z.real:.1f}{'+' if z.imag>=0 else ''}{z.imag:.1f}i", 
                                font_size=16, color=color)
                z_label.next_to(z_point, UR, buff=0.1)
                
                # 动画
                self.play(FadeIn(s_dot), Write(s_label))
                self.wait(0.3)
                
                # 创建连接线
                if sx < 0:  # 左半平面点
                    trace_line = DashedLine(s_point, z_point, color=color, stroke_width=2)
                    self.play(Create(trace_line), 
                            FadeIn(z_dot), Write(z_label))
                else:
                    self.play(FadeIn(z_dot), Write(z_label))
                
                self.wait(0.5)
                self.play(FadeOut(s_dot), FadeOut(s_label),
                         FadeOut(z_dot), FadeOut(z_label))
                if 'trace_line' in locals():
                    self.play(FadeOut(trace_line))
        
        self.wait(3)
        
        # 清理
        self.play(
            FadeOut(s_plane), FadeOut(z_plane),
            FadeOut(s_label), FadeOut(z_label),
            FadeOut(left_half), FadeOut(unit_circle), 
            FadeOut(unit_circle_interior),
            FadeOut(mapping_info),
            FadeOut(formula)
        )

# 简化版本，如果上面版本有问题，可以使用这个
class ConformalMappingSimple(Scene):
    def construct(self):
        # 标题固定在左上角
        title = Text("共形映射可视化", font_size=36, color=BLUE)
        title.to_corner(UL, buff=0.5)
        
        self.play(Write(title))
        self.wait(0.5)
        
        # 1. 复数平面介绍
        self.show_complex_plane_simple(title)
        self.wait(1)
        
        # 2. 共形映射示例
        self.show_mapping_examples_simple(title)
        self.wait(1)
        
        # 3. 双线性变换
        self.show_bilinear_simple(title)
        
        # 结束
        self.play(FadeOut(title))
        self.wait(1)
    
    def show_complex_plane_simple(self, title):
        """简化版：显示复数平面"""
        # 更新标题
        new_title = Text("复数平面", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        self.play(Transform(title, new_title))
        
        # 创建复数平面
        plane = ComplexPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=5
        )
        
        # 说明文本
        info = VGroup(
            Text("复数：z = a + bi", font_size=24, color=WHITE),
            Text("实部：Re(z) = a", font_size=20, color=GRAY),
            Text("虚部：Im(z) = b", font_size=20, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        info.to_corner(UR, buff=0.5)
        
        self.play(Create(plane), Write(info))
        self.wait(2)
        self.play(FadeOut(plane), FadeOut(info))
    
    def show_mapping_examples_simple(self, title):
        """简化版：显示映射示例"""
        # 更新标题
        new_title = Text("共形映射", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        self.play(Transform(title, new_title))
        
        # 映射公式
        formula1 = MathTex("w = z^2", font_size=32, color=RED)
        formula2 = MathTex("w = e^z", font_size=32, color=BLUE)
        
        formula1.to_edge(UP).shift(DOWN*1)
        formula2.next_to(formula1, DOWN, buff=0.5)
        
        # 说明文本
        info = VGroup(
            Text("共形映射特性：", font_size=24, color=WHITE),
            Text("1. 保角性", font_size=20, color=GRAY),
            Text("2. 局部相似", font_size=20, color=GRAY),
            Text("3. 保持小形状", font_size=20, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        info.to_corner(UR, buff=0.5)
        
        self.play(Write(formula1), Write(formula2), Write(info))
        self.wait(3)
        self.play(FadeOut(formula1), FadeOut(formula2), FadeOut(info))
    
    def show_bilinear_simple(self, title):
        """简化版：显示双线性变换"""
        # 更新标题
        new_title = Text("双线性变换", font_size=32, color=YELLOW)
        new_title.to_corner(UL, buff=0.5)
        self.play(Transform(title, new_title))
        
        # 双线性变换公式
        formula = MathTex(
            "s = \\frac{2}{T} \\cdot \\frac{1 - z^{-1}}{1 + z^{-1}}",
            font_size=28, color=GREEN
        )
        formula.to_edge(UP).shift(DOWN*1)
        
        # 映射关系说明
        mapping_info = VGroup(
            Text("模拟滤波器 ↔ 数字滤波器", font_size=24, color=WHITE),
            Text("s平面 ↔ z平面", font_size=20, color=GRAY),
            Text("左半平面 ↔ 单位圆内", font_size=20, color=BLUE),
            Text("虚轴 ↔ 单位圆", font_size=20, color=YELLOW),
            Text("右半平面 ↔ 单位圆外", font_size=20, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        mapping_info.to_corner(UR, buff=0.5)
        
        self.play(Write(formula), Write(mapping_info))
        self.wait(3)
        
        # 应用领域
        applications = VGroup(
            Text("应用领域：", font_size=24, color=WHITE),
            Text("• 数字滤波器设计", font_size=20, color=GRAY),
            Text("• 控制系统", font_size=20, color=GRAY),
            Text("• 信号处理", font_size=20, color=GRAY),
            Text("• 图像处理", font_size=20, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        applications.to_edge(DOWN).shift(UP*0.5)
        
        self.play(Write(applications))
        self.wait(3)
        
        self.play(FadeOut(formula), FadeOut(mapping_info), FadeOut(applications))