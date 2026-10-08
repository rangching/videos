from manim_imports_ext import *


# 用 Manim 做課程影片：AI 協作工作流（約 5 分鐘）
# Narration and timing live in script.md; each scene below is one chapter.
# Render all: manimgl main.py Intro Pipeline DivisionOfLabor ParallelAgents IterationLoop Pitfalls Outro -w

CJK_FONT = "Noto Sans CJK TC"
MONO_FONT = "DejaVu Sans Mono"

HUMAN_COLOR = YELLOW
AI_COLOR = BLUE
LOOP_COLOR = TEAL

STAGES = [
    ("企劃", "Plan", "學習目標"),
    ("腳本", "Script", "旁白稿 .md"),
    ("分鏡", "Storyboard", "Scene 清單"),
    ("程式", "Code", "scenes .py"),
    ("算圖審片", "Render & Review", "預覽 .mp4"),
    ("配音剪輯", "Voice & Edit", "成片"),
]

# Share of each stage led by the human (the rest is led by AI)
HUMAN_SHARES = [0.9, 0.6, 0.5, 0.15, 0.6, 0.85]

CODE_KEYWORDS = {
    "class ": RED,
    "def ": RED,
    "self": ORANGE,
    "InteractiveScene": GREEN,
    "Square": BLUE_B,
    "Circle": BLUE_B,
    "ShowCreation": BLUE_B,
    "ReplacementTransform": BLUE_B,
    "Write": BLUE_B,
    "Text": BLUE_B,
}


def zh(text, font_size=48, color=WHITE, **kwargs):
    return Text(text, font=CJK_FONT, font_size=font_size, **kwargs).set_color(color)


def get_code(code, font_size=28):
    return Text(
        code,
        font=MONO_FONT,
        font_size=font_size,
        alignment="LEFT",
        t2c=CODE_KEYWORDS,
    )


def get_card(mobject, color=GREY_B, buff=0.25, fill_opacity=0.15):
    card = SurroundingRectangle(mobject, buff=buff)
    card.round_corners(0.15)
    card.set_stroke(color, 2)
    card.set_fill(color, fill_opacity)
    return VGroup(card, mobject)


def get_chapter_title(text):
    title = zh(text, font_size=60)
    title.to_edge(UP, buff=0.35)
    underline = Line(LEFT, RIGHT).match_width(title).scale(1.1)
    underline.next_to(title, DOWN, buff=0.15)
    underline.set_stroke(GREY_B, 2)
    return VGroup(title, underline)


def get_bracket(mobject, buff=0.1, tick=0.15, color=GREY_B):
    # Plain-line brace, so the video renders without a LaTeX install
    left = mobject.get_corner(DL) + buff * DOWN
    right = mobject.get_corner(DR) + buff * DOWN
    bracket = VMobject()
    bracket.set_points_as_corners([
        left + tick * UP, left, right, right + tick * UP
    ])
    bracket.set_stroke(color, 2)
    return bracket


def get_stage_box(zh_name, en_name, width=2.0, height=1.6, color=GREY_B):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15)
    box.set_stroke(color, 2)
    box.set_fill(color, 0.1)
    name = zh(zh_name, font_size=40)
    name.set_max_width(width - 0.2)
    en = Text(en_name, font_size=22).set_color(GREY_B)
    en.set_max_width(width - 0.2)
    label = VGroup(name, en).arrange(DOWN, buff=0.2)
    label.move_to(box)
    return VGroup(box, label)


def get_pipeline(width=2.0, buff=0.3):
    boxes = VGroup(
        get_stage_box(zh_name, en_name, width=width)
        for zh_name, en_name, _ in STAGES
    )
    boxes.arrange(RIGHT, buff=buff)
    arrows = VGroup(
        Arrow(b1.get_right(), b2.get_left(), buff=0.03, thickness=3)
        for b1, b2 in zip(boxes, boxes[1:])
    )
    arrows.set_color(GREY_B)
    return boxes, arrows


class Intro(InteractiveScene):
    def construct(self):
        # Questions people keep asking
        questions = VGroup(
            zh("這種動畫是怎麼做的？", font_size=60),
            zh("一定要很會寫程式嗎？", font_size=60),
            zh("AI 到底能幫上什麼忙？", font_size=60),
        )
        bubbles = VGroup(get_card(q, color=GREY_B, buff=0.3) for q in questions)
        bubbles[0].move_to(2.8 * LEFT + 2.0 * UP)
        bubbles[1].move_to(2.6 * RIGHT + 0.2 * UP)
        bubbles[2].move_to(1.8 * LEFT + 1.9 * DOWN)

        self.play(LaggedStart(
            (FadeIn(bubble, scale=0.8) for bubble in bubbles),
            lag_ratio=0.6,
            run_time=3,
        ))
        self.wait(4)

        # A small showcase of what Manim does
        self.play(FadeOut(bubbles, lag_ratio=0.1))

        axes = Axes((-3, 3), (-1.5, 1.5), width=7, height=3.5)
        axes.to_edge(LEFT, buff=0.8)
        graph = axes.get_graph(np.sin, color=BLUE)
        dot = GlowDot(color=YELLOW)
        dot.move_to(graph.get_start())

        square = Square(side_length=2.8).set_stroke(YELLOW, 5)
        square.to_edge(RIGHT, buff=1.2)
        circle = Circle(radius=1.6).set_stroke(TEAL, 5)
        circle.move_to(square)

        self.play(ShowCreation(axes), ShowCreation(square))
        self.play(
            ShowCreation(graph),
            MoveAlongPath(dot, graph),
            ReplacementTransform(square, circle),
            run_time=3,
        )
        self.wait(2)

        # Title
        showcase = Group(axes, graph, dot, circle)
        title = zh("用 Manim 做課程影片", font_size=90)
        subtitle = zh("AI 協作工作流 AI Collaboration Workflow", font_size=44, color=GREY_B)
        VGroup(title, subtitle).arrange(DOWN, buff=0.4).move_to(1.2 * UP)

        self.play(
            showcase.animate.scale(0.5).set_opacity(0.3).to_edge(DOWN),
            Write(title, run_time=2),
        )
        self.play(FadeIn(subtitle, shift=0.25 * UP))
        self.wait(3)

        # Three keywords for this video
        keywords = VGroup(
            zh("manim-pipeline 流水線", font_size=40, color=WHITE),
            zh("分工模式 Division of labor", font_size=40, color=HUMAN_COLOR),
            zh("迭代 Iteration", font_size=40, color=LOOP_COLOR),
        )
        keywords.arrange(RIGHT, buff=0.7)
        keywords.set_max_width(13)
        keywords.next_to(subtitle, DOWN, buff=0.9)

        self.play(
            FadeOut(showcase),
            LaggedStart(
                (FadeIn(word, shift=0.25 * UP) for word in keywords),
                lag_ratio=0.5,
                run_time=2,
            )
        )
        self.wait(4)

        meta = zh("（這支影片本身，就是用這套流程做出來的）", font_size=36, color=GREY_B)
        meta.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(meta))
        self.wait(7)


class Pipeline(InteractiveScene):
    def construct(self):
        title = get_chapter_title("manim-pipeline：六個站")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        # Stages appear one at a time
        boxes, arrows = get_pipeline()
        boxes.move_to(0.2 * UP)
        arrows.match_y(boxes)

        for n, box in enumerate(boxes):
            anims = [FadeIn(box, shift=0.25 * RIGHT)]
            if n > 0:
                anims.append(GrowArrow(arrows[n - 1]))
            self.play(*anims, run_time=0.8)
            self.wait(1.2)
        self.wait(2)

        # Each stage leaves a deliverable behind
        deliverables = VGroup(
            zh(name, font_size=30, color=GREY_A)
            for _, _, name in STAGES
        )
        for deliverable, box in zip(deliverables, boxes):
            deliverable.set_max_width(box.get_width())
            deliverable.next_to(box, DOWN, buff=0.35)
        deliverable_label = zh("每一站都留下產出物 Deliverable", font_size=40, color=GREEN)
        deliverable_label.next_to(deliverables, DOWN, buff=0.6)

        self.play(LaggedStart(
            (FadeIn(d, shift=0.2 * DOWN) for d in deliverables),
            lag_ratio=0.2,
        ))
        self.play(Write(deliverable_label))
        self.wait(5)

        # The real work happens in a loop between Code and Review
        loop_arrow = CurvedArrow(
            boxes[4].get_top() + 0.05 * UP,
            boxes[3].get_top() + 0.05 * UP,
            angle=PI / 2,
        )
        loop_arrow.set_color(LOOP_COLOR)
        loop_label = zh("改到滿意為止", font_size=34, color=LOOP_COLOR)
        loop_label.next_to(loop_arrow, UP, buff=0.1)

        self.play(
            ShowCreation(loop_arrow),
            FadeIn(loop_label),
            boxes[3][0].animate.set_stroke(LOOP_COLOR, 4),
            boxes[4][0].animate.set_stroke(LOOP_COLOR, 4),
        )
        for _ in range(2):
            self.play(
                ShowPassingFlash(
                    loop_arrow.copy().set_stroke(WHITE, 6),
                    time_width=0.5,
                    run_time=1.5,
                )
            )
        self.wait(5)

        # Key point
        point = zh("先寫旁白，再寫程式：畫面跟著聲音走", font_size=44, color=YELLOW)
        point.move_to(deliverable_label)
        self.play(
            FadeOut(deliverable_label),
            FlashAround(boxes[1], color=YELLOW),
            boxes[1][0].animate.set_stroke(YELLOW, 4),
            Write(point),
        )
        self.wait(10)


class DivisionOfLabor(InteractiveScene):
    def construct(self):
        title = get_chapter_title("分工模式：誰負責什麼？")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        # One bar per stage, split by who leads
        bar_width = 8.5
        bar_height = 0.6
        rows = VGroup()
        for (zh_name, en_name, _), share in zip(STAGES, HUMAN_SHARES):
            label = zh(zh_name, font_size=38)
            human_bar = Rectangle(width=share * bar_width, height=bar_height)
            human_bar.set_fill(HUMAN_COLOR, 0.85).set_stroke(width=0)
            ai_bar = Rectangle(width=(1 - share) * bar_width, height=bar_height)
            ai_bar.set_fill(AI_COLOR, 0.85).set_stroke(width=0)
            bar = VGroup(human_bar, ai_bar).arrange(RIGHT, buff=0)
            rows.add(VGroup(label, bar))

        rows.arrange(DOWN, buff=0.3)
        for row in rows:
            row[1].set_x(1.2)
            row[0].next_to(row[1], LEFT, buff=0.4)
        rows.set_y(-0.6)
        bars = VGroup(row[1] for row in rows)

        # Column headers, aligned to the ends of the bars
        human_header = zh("人｜導演 Director", font_size=40, color=HUMAN_COLOR)
        ai_header = zh("AI｜動畫師 Animator", font_size=40, color=AI_COLOR)
        human_header.next_to(bars, UP, buff=0.4, aligned_edge=LEFT)
        ai_header.next_to(bars, UP, buff=0.4, aligned_edge=RIGHT)

        self.play(
            FadeIn(human_header, shift=0.25 * RIGHT),
            FadeIn(ai_header, shift=0.25 * LEFT),
        )
        self.wait(2)

        divider = DashedLine(bars.get_top() + 0.1 * UP, bars.get_bottom() + 0.1 * DOWN)
        divider.set_stroke(GREY_B, 1)

        self.play(ShowCreation(divider))
        for row in rows:
            self.play(
                FadeIn(row[0]),
                GrowFromEdge(row[1][0], LEFT),
                GrowFromEdge(row[1][1], RIGHT),
                run_time=0.8,
            )
            self.wait(1.4)
        self.wait(2)

        # Highlight the extremes: Plan is human, Code is AI
        self.play(FlashAround(rows[0], color=HUMAN_COLOR, run_time=2))
        self.wait(3)
        self.play(FlashAround(rows[3], color=AI_COLOR, run_time=2))
        self.wait(4)

        # The one-line rule
        chart = VGroup(human_header, ai_header, rows, divider)
        rule = zh("人決定 What & Why；AI 負責 How", font_size=64)
        rule.set_color_by_text_to_color_map({"人決定 What & Why": HUMAN_COLOR, "AI 負責 How": AI_COLOR})
        rule.move_to(0.3 * UP)
        rule_back = BackgroundRectangle(rule, buff=0.3, fill_opacity=0.85)
        self.play(
            chart.animate.set_opacity(0.2),
            FadeIn(rule_back),
            Write(rule),
        )
        self.wait(5)

        taste = zh("最稀缺的是品味 Taste，不是打字速度", font_size=44, color=GREY_A)
        taste.next_to(rule, DOWN, buff=0.6)
        taste_back = BackgroundRectangle(taste, buff=0.2, fill_opacity=0.85)
        self.play(FadeIn(taste_back), FadeIn(taste, shift=0.2 * UP))
        self.wait(10)


class ParallelAgents(InteractiveScene):
    def construct(self):
        title = get_chapter_title("分工模式進階：一個 Scene 一個 Agent")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        # Storyboard cards
        scene_names = ["引子", "流水線", "分工", "示範", "收尾"]
        colors = [BLUE_C, TEAL_C, GREEN_C, YELLOW_C, RED_C]
        cards = VGroup(
            get_card(
                zh(f"Scene {n + 1}｜{name}", font_size=32),
                color=color,
                buff=0.18,
            )
            for n, (name, color) in enumerate(zip(scene_names, colors))
        )
        for card in cards:
            card[0].set_width(3.2, stretch=True)
        cards.arrange(DOWN, buff=0.22)
        cards.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        storyboard_label = zh("分鏡 Storyboard", font_size=36, color=GREY_A)
        storyboard_label.next_to(cards, UP, buff=0.3)

        self.play(
            FadeIn(storyboard_label),
            LaggedStart((FadeIn(card, shift=0.2 * RIGHT) for card in cards), lag_ratio=0.2),
        )
        self.wait(3)

        # Serial vs parallel timelines
        unit = 1.3
        timeline_left = 1.0 * LEFT

        def get_block(n):
            block = Rectangle(width=unit, height=0.5)
            block.set_fill(colors[n], 0.85).set_stroke(WHITE, 1)
            return block

        serial_label = zh("序列 Serial：一個人從頭做到尾", font_size=34)
        serial_blocks = VGroup(get_block(n) for n in range(5))
        serial_blocks.arrange(RIGHT, buff=0)
        serial_blocks.move_to(timeline_left + 1.5 * UP, aligned_edge=LEFT)
        serial_label.next_to(serial_blocks, UP, buff=0.2, aligned_edge=LEFT)

        self.play(FadeIn(serial_label))
        for block in serial_blocks:
            self.play(GrowFromEdge(block, LEFT), run_time=0.6)
        self.wait(2)

        parallel_label = zh("平行 Parallel：三個 Agent 同時開工", font_size=34)
        lanes = VGroup()
        assignments = [[0, 3], [1, 4], [2]]
        for indices in assignments:
            lane = VGroup(get_block(n) for n in indices)
            lane.arrange(RIGHT, buff=0)
            lanes.add(lane)
        lanes.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        lanes.move_to(timeline_left + 1.1 * DOWN, aligned_edge=LEFT)
        parallel_label.next_to(lanes, UP, buff=0.25, aligned_edge=LEFT)

        agent_labels = VGroup(
            Text(f"Agent {letter}", font_size=26).set_color(AI_COLOR)
            for letter in "ABC"
        )
        for label, lane in zip(agent_labels, lanes):
            label.next_to(lane, LEFT, buff=0.2)

        self.play(FadeIn(parallel_label), FadeIn(agent_labels))
        self.play(
            LaggedStart(
                (GrowFromEdge(lane[0], LEFT) for lane in lanes),
                lag_ratio=0,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                (GrowFromEdge(lane[1], LEFT) for lane in lanes[:2]),
                lag_ratio=0,
            ),
            run_time=0.6,
        )
        self.wait(2)

        # Compare total time
        serial_brace = get_bracket(serial_blocks)
        serial_time = zh("5 份時間", font_size=30).next_to(serial_brace, DOWN, buff=0.1)
        parallel_brace = get_bracket(lanes)
        parallel_time = zh("2 份時間", font_size=30, color=GREEN).next_to(parallel_brace, DOWN, buff=0.1)
        self.play(
            ShowCreation(serial_brace), FadeIn(serial_time),
            ShowCreation(parallel_brace), FadeIn(parallel_time),
        )
        self.wait(5)

        # The catch: shared conventions
        timelines = VGroup(
            serial_label, serial_blocks, serial_brace, serial_time,
            parallel_label, agent_labels, lanes, parallel_brace, parallel_time,
        )
        contract = VGroup(
            zh("共用規範 Shared conventions", font_size=40, color=YELLOW),
            zh("・style.py：顏色、字型", font_size=34),
            zh("・helpers：get_card()、get_code()", font_size=34),
            zh("・CLAUDE.md：寫法規則", font_size=34),
        )
        contract.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        contract_card = get_card(contract, color=YELLOW, buff=0.35, fill_opacity=0.08)
        contract_card.move_to(timelines).shift(0.3 * DOWN)

        warning = zh("沒有規範的平行，只會得到五種畫風", font_size=38, color=RED_B)
        warning.next_to(contract_card, DOWN, buff=0.35)

        self.play(
            FadeOut(timelines, shift=0.5 * UP),
            FadeIn(contract_card, shift=0.5 * UP),
        )
        self.wait(4)
        self.play(Write(warning))
        self.wait(10)


class IterationLoop(InteractiveScene):
    def construct(self):
        title = get_chapter_title("實際走一輪：說 → 寫 → 看 → 改")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        # Prompt
        prompt = zh("你：「畫一個正方形，變成藍色的圓」", font_size=40, color=HUMAN_COLOR)
        prompt_card = get_card(prompt, color=HUMAN_COLOR, buff=0.2, fill_opacity=0.08)
        prompt_card.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(prompt_card, shift=0.2 * DOWN))
        self.wait(2)

        # Code, version 1
        code_v1 = get_code(
            "class Demo(InteractiveScene):\n"
            "    def construct(self):\n"
            "        sq = Square()\n"
            "        circ = Circle(color=BLUE)\n"
            "        self.play(ShowCreation(sq))\n"
            "        self.play(ReplacementTransform(sq, circ))"
        )
        code_width = 6.5
        code_top = 0.8
        code_v1.set_width(code_width * 0.85)
        code_v1.to_edge(LEFT, buff=0.75).set_y(code_top, UP)
        code_box = SurroundingRectangle(code_v1, buff=0.25)
        code_box.set_stroke(AI_COLOR, 2).set_fill(BLACK, 0.5).round_corners(0.1)
        code_label = zh("AI 寫的程式 Code", font_size=32, color=AI_COLOR)
        code_label.next_to(code_box, UP, buff=0.1, aligned_edge=LEFT)

        # Preview window
        preview = ScreenRectangle(height=3.2)
        preview.set_stroke(GREY_B, 2).set_fill(GREY_E, 0.6)
        preview.to_edge(RIGHT, buff=0.5).set_y(code_top + 0.25, UP)
        preview_label = zh("預覽 Preview（-p）", font_size=32, color=GREY_A)
        preview_label.next_to(preview, UP, buff=0.1, aligned_edge=LEFT)

        self.play(
            FadeIn(code_box),
            FadeIn(code_label),
            ShowIncreasingSubsets(code_v1, run_time=3),
        )
        self.play(FadeIn(preview), FadeIn(preview_label))

        round_label = zh("第 1 輪", font_size=34, color=LOOP_COLOR)
        round_label.next_to(preview, UP, buff=0.1, aligned_edge=RIGHT)
        self.play(FadeIn(round_label))
        result = self.play_demo(preview, run_time=1)
        self.wait(3)

        # Feedback
        feedback = zh("你：「太快了，慢一點；再加個標題」", font_size=40, color=HUMAN_COLOR)
        feedback_card = get_card(feedback, color=HUMAN_COLOR, buff=0.2, fill_opacity=0.08)
        feedback_card.move_to(prompt_card)
        self.play(
            FadeOut(prompt_card, shift=0.2 * UP),
            FadeIn(feedback_card, shift=0.2 * UP),
        )
        self.wait(2)

        # Code, version 2
        code_v2 = get_code(
            "class Demo(InteractiveScene):\n"
            "    def construct(self):\n"
            "        title = Text(\"正方形 → 圓\").to_edge(UP)\n"
            "        sq = Square()\n"
            "        circ = Circle(color=BLUE)\n"
            "        self.play(Write(title), ShowCreation(sq))\n"
            "        self.play(ReplacementTransform(sq, circ), run_time=3)"
        )
        code_v2.set_width(code_width)
        code_v2.move_to(code_v1, aligned_edge=UL)
        new_code_box = SurroundingRectangle(code_v2, buff=0.25)
        new_code_box.match_style(code_box).round_corners(0.1)

        self.play(
            FadeOut(result),
            FadeTransform(code_v1, code_v2),
            Transform(code_box, new_code_box),
            run_time=1.5,
        )
        highlights = VGroup(
            SurroundingRectangle(code_v2.select_part("run_time=3"), buff=0.05),
            SurroundingRectangle(code_v2.select_part("title"), buff=0.05),
        )
        highlights.set_stroke(YELLOW, 2)
        self.play(ShowCreation(highlights, lag_ratio=0.5))

        new_round_label = zh("第 2 輪", font_size=34, color=LOOP_COLOR)
        new_round_label.move_to(round_label)
        self.play(FadeTransform(round_label, new_round_label))
        self.play_demo(preview, run_time=3, with_title=True)
        self.wait(2)

        # Tools that make the loop fast
        tips = VGroup(
            zh("manimgl main.py Demo -se 12：停在第 12 行，互動除錯", font_size=28),
            zh("checkpoint_paste()：只重跑改動的段落", font_size=28),
        )
        tips.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tips.to_corner(DL, buff=0.5)
        self.play(
            FadeOut(highlights),
            LaggedStart((FadeIn(tip, shift=0.2 * UP) for tip in tips), lag_ratio=0.5),
        )
        self.wait(4)

        punchline = zh("每輪 1～2 分鐘：小步快跑", font_size=40, color=LOOP_COLOR)
        punchline.next_to(preview, DOWN, buff=0.5)
        punchline.to_edge(RIGHT, buff=0.5)
        self.play(TransformFromCopy(new_round_label, punchline))
        self.wait(10)

    def play_demo(self, preview, run_time=1, with_title=False):
        square = Square(side_length=1.4).set_stroke(WHITE, 4)
        circle = Circle(radius=0.8).set_stroke(BLUE, 4)
        square.move_to(preview).shift(0.2 * DOWN)
        circle.move_to(square)

        anims = [ShowCreation(square)]
        result = VGroup(circle)
        if with_title:
            title = zh("正方形 → 圓", font_size=32)
            title.next_to(preview.get_top(), DOWN, buff=0.25)
            anims.append(Write(title))
            result.add(title)
        self.play(*anims, run_time=1)
        self.play(ReplacementTransform(square, circle), run_time=run_time)
        return result


class Pitfalls(InteractiveScene):
    def construct(self):
        title = get_chapter_title("四個常見的坑 Pitfalls")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        items = [
            ("一個 Scene 塞太多", "一個 Scene 只講一件事，方便平行與重做"),
            ("沒有旁白就開畫", "先定旁白長度，再用 self.wait() 對時間"),
            ("字型、LaTeX 沒先測", "第一天就算一張測試圖，設定問題早爆早好"),
            ("每次都從零開始", "把 prompt 與 helper 存成模板 Template"),
        ]
        rows = VGroup()
        for problem, fix in items:
            problem_text = zh("✗ " + problem, font_size=38, color=RED_B)
            fix_text = zh("✓ " + fix, font_size=34, color=GREEN_B)
            rows.add(VGroup(problem_text, fix_text))

        problem_width = max(row[0].get_width() for row in rows)
        for row in rows:
            row[1].next_to(row[0], RIGHT, buff=0)
            row[1].shift((problem_width - row[0].get_width() + 0.6) * RIGHT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        rows.set_max_width(13)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=1.1)
        rows.next_to(title, DOWN, buff=0.9)

        cards = VGroup()
        for row in rows:
            card = SurroundingRectangle(row, buff=0.22)
            card.set_width(rows.get_width() + 0.5, stretch=True)
            card.match_x(rows)
            card.round_corners(0.15)
            card.set_stroke(GREY_B, 2).set_fill(GREY_B, 0.08)
            cards.add(card)

        for card, (problem_text, fix_text) in zip(cards, rows):
            self.play(FadeIn(card), FadeIn(problem_text, shift=0.2 * RIGHT))
            self.wait(1.5)
            self.play(FadeIn(fix_text, shift=0.2 * RIGHT))
            self.wait(6)
        self.wait(3)


class Outro(InteractiveScene):
    def construct(self):
        title = get_chapter_title("今天就能開始的三步")
        self.play(FadeIn(title, shift=0.25 * DOWN))

        steps = VGroup(
            zh("1. 挑一個 3 分鐘能講完的概念，先寫旁白", font_size=44),
            zh("2. 拆成 3～5 個 Scene，交給 AI 寫第一版", font_size=44),
            zh("3. 你只做一件事：看預覽、給回饋", font_size=44),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.next_to(title, DOWN, buff=0.7)

        for step in steps:
            self.play(FadeIn(step, shift=0.25 * RIGHT))
            self.wait(4)
        self.wait(2)

        # Knowledge management: the pipeline compounds
        boxes, arrows = get_pipeline()
        pipeline = VGroup(boxes, arrows)
        pipeline.set_width(11)
        pipeline.next_to(steps, DOWN, buff=0.7)
        library = zh("模板庫 Template library：越做越快", font_size=38, color=GREEN)
        library.next_to(pipeline, DOWN, buff=0.3)

        self.play(
            LaggedStart((FadeIn(box) for box in boxes), lag_ratio=0.1),
            LaggedStart((GrowArrow(arrow) for arrow in arrows), lag_ratio=0.1),
        )
        self.play(Write(library))
        self.wait(5)

        # Final line
        final = VGroup(
            zh("你當導演，AI 當動畫師", font_size=80),
            zh("You direct, AI animates.", font_size=44, color=GREY_B),
        )
        final.arrange(DOWN, buff=0.4)
        self.play(
            FadeOut(VGroup(title, steps, pipeline, library)),
            FadeIn(final, scale=1.1),
        )
        self.wait(8)
        self.play(FadeOut(final))
