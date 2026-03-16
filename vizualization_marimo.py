import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import altair as alt
    import pandas as pd
    import polars as pl

    return alt, np, pd, pl


@app.cell
def _(pd, pl):
    df: pd.DataFrame = pl.read_excel("student_performance/student_performance.xlsx").to_pandas()
    df.info()
    return (df,)


@app.cell
def _(df: "pd.DataFrame", np):
    # Get numeric columns with missing values
    columns = df.select_dtypes(include=[np.number]).isnull().sum().where(lambda x: x > 0).dropna().index.tolist()
    print("Numeric columns with missing values:", columns)

    for col in columns:
        df[col] = df[col].fillna(df[col].median())

    # Get categorical columns with missing values
    cat_columns = df.select_dtypes(include=['str']).isnull().sum().where(lambda x: x > 0).dropna().index.tolist()
    for col in cat_columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    return


@app.cell
def _(df: "pd.DataFrame"):
    df.G3.describe()
    return


@app.cell
def _(df: "pd.DataFrame"):
    df.G2.describe()
    return


@app.cell
def _(alt, df: "pd.DataFrame", pd):
    """
    Student Grade Explorer — Interactive Altair Dashboard
    ======================================================
    Assumes:  `df`  is a cleaned pandas DataFrame with the student dataset.

    Filtering is done via CLICKABLE LEGENDS (no external HTML widgets):
      • Click a Sex legend symbol   → show only that sex   (multi-select with shift)
      • Click a School legend symbol→ show only that school (multi-select with shift)
      • Drag on the histogram       → filter by grade range

    Run in Jupyter:  dashboard
    Save to HTML:    dashboard.save("grade_explorer.html")
    """


    # ── 1. Theme ──────────────────────────────────────────────────────────────────
    def _grade_theme():
        FONT = "IBM Plex Mono"
        BG   = "#0d0f18"
        GRID = "#1a1e2e"
        AXIS = "#3d4260"
        LBL  = "#7b82a8"
        TTL  = "#c8ceeb"
        return {
            "config": {
                "background": BG,
                "view": {"stroke": AXIS, "strokeWidth": 1, "fill": "#10131f"},
                "axis": {
                    "domainColor": AXIS, "gridColor": GRID, "gridOpacity": 0.8,
                    "tickColor": AXIS, "labelColor": LBL, "titleColor": TTL,
                    "labelFont": FONT, "titleFont": FONT,
                    "labelFontSize": 10, "titleFontSize": 11,
                    "titleFontWeight": "normal", "labelPadding": 6,
                },
                "legend": {
                    "labelColor": LBL, "titleColor": TTL,
                    "labelFont": FONT, "titleFont": FONT,
                    "labelFontSize": 11, "titleFontSize": 11,
                    "padding": 10, "rowPadding": 6,
                    "symbolStrokeWidth": 0, "symbolSize": 120,
                    "orient": "right",
                },
                "title": {
                    "color": "#e8ecff", "font": FONT,
                    "fontSize": 11, "fontWeight": "normal",
                    "anchor": "start", "offset": 10,
                    "subtitleColor": LBL, "subtitleFont": FONT,
                    "subtitleFontSize": 10,
                },
                "header": {"labelColor": LBL, "titleColor": TTL, "labelFont": FONT},
                "mark": {"tooltip": True},
            }
        }

    alt.themes.register("grade_theme", _grade_theme)
    alt.themes.enable("grade_theme")


    # ── 2. Palettes ────────────────────────────────────────────────────────────────
    SEX_DOMAIN    = ["F", "M"]
    SEX_RANGE     = ["#6366f1", "#f43f5e"]
    SCHOOL_DOMAIN = ["GP", "MS"]
    SCHOOL_RANGE  = ["#22d3ee", "#fb923c"]
    ST_RANGE      = ["#312e81", "#4338ca", "#6366f1", "#a5b4fc"]


    # ── 3. Selections (legend-bound, not HTML widgets) ────────────────────────────
    sel_sex = alt.selection_point(
        name="sel_sex",
        fields=["sex"],
        bind="legend",
        toggle="event.shiftKey",   # shift-click for multi-select
    )

    sel_school = alt.selection_point(
        name="sel_school",
        fields=["school"],
        bind="legend",
        toggle="event.shiftKey",
    )

    # Grade-range brush on histogram x-axis
    brush = alt.selection_interval(name="brush", encodings=["x"], empty=True)

    ALL_SEL = [sel_sex, sel_school]


    # ── 4. Opacity condition (dim non-selected instead of hiding) ─────────────────
    def filtered_opacity(*selections):
        """Return an opacity condition: 0.85 if in all selections, else 0.07."""
        cond = selections[0]
        for s in selections[1:]:
            cond = cond & s
        return alt.condition(cond, alt.value(0.85), alt.value(0.07))


    # ── 5. Shared encodings ────────────────────────────────────────────────────────
    SEX_COLOR = alt.Color(
        "sex:N",
        scale=alt.Scale(domain=SEX_DOMAIN, range=SEX_RANGE),
        legend=alt.Legend(
            title="SEX  (click to filter)",
            symbolType="circle",
            symbolSize=150,
        ),
    )

    SCHOOL_COLOR = alt.Color(
        "school:N",
        scale=alt.Scale(domain=SCHOOL_DOMAIN, range=SCHOOL_RANGE),
        legend=alt.Legend(
            title="SCHOOL  (click to filter)",
            symbolType="square",
            symbolSize=150,
        ),
    )

    TOOLTIP = [
        alt.Tooltip("school:N",    title="School"),
        alt.Tooltip("sex:N",       title="Sex"),
        alt.Tooltip("age:Q",       title="Age"),
        alt.Tooltip("studytime:O", title="Study time"),
        alt.Tooltip("failures:O",  title="Failures"),
        alt.Tooltip("absences:Q",  title="Absences"),
        alt.Tooltip("G1:Q",        title="Grade P1"),
        alt.Tooltip("G2:Q",        title="Grade P2"),
        alt.Tooltip("G3:Q",        title="Final grade"),
    ]


    # ─────────────────────────────────────────────────────────────────────────────
    # 6. CHARTS
    # ─────────────────────────────────────────────────────────────────────────────

    # ── A. MAIN: Grade Distribution histogram (brush source) ──────────────────────
    # Layer 1 — faint ghost bars (full data, always visible)
    hist_bg = (
        alt.Chart(df)
        .mark_bar(opacity=0.12, binSpacing=2,
                  cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#3d4260")
        .encode(
            x=alt.X("G3:Q", bin=alt.Bin(maxbins=21), title="Final Grade",
                    axis=alt.Axis(tickCount=11)),
            y=alt.Y("count():Q", title="Students", stack=True),
        )
    )

    # Layer 2 — coloured bars (filtered by legend selections)
    hist_fg = (
        alt.Chart(df)
        .mark_bar(binSpacing=2, cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("G3:Q", bin=alt.Bin(maxbins=21), title="Final Grade",
                    axis=alt.Axis(tickCount=11)),
            y=alt.Y("count():Q", title="Students", stack=True),
            color=SEX_COLOR,
            opacity=filtered_opacity(sel_sex, sel_school),
            tooltip=[
                alt.Tooltip("G3:Q",      bin=True, title="Grade range"),
                alt.Tooltip("sex:N",     title="Sex"),
                alt.Tooltip("count():Q", title="Count"),
            ],
        )
    )

    # Layer 3 — invisible wide bars just to carry the school legend
    school_legend_layer = (
        alt.Chart(df)
        .mark_point(opacity=0, size=0)   # invisible — legend only
        .encode(color=SCHOOL_COLOR)
    )

    hist_g3 = (
        (hist_bg + hist_fg + school_legend_layer)
        .add_params(*ALL_SEL, brush)
        .properties(
            title=alt.TitleParams(
                "Grade Distribution  —  Main Panel",
                subtitle=(
                    "Drag to select a grade range  ·  "
                    "Click legend to filter by sex or school  ·  "
                    "Shift-click for multi-select"
                ),
            ),
            width=640,
            height=230,
        )
    )


    # ── B. G2 → G3 Scatter ────────────────────────────────────────────────────────
    ref_line = (
        alt.Chart(pd.DataFrame({"v": [0, 20]}))
        .mark_line(color="#3d4260", strokeDash=[4, 4], strokeWidth=1.5)
        .encode(x="v:Q", y="v:Q")
    )

    scatter_g2_g3 = (
        alt.Chart(df)
        .mark_circle(size=50, strokeWidth=0)
        .encode(
            x=alt.X("G2:Q", title="Period 2 Grade",
                    scale=alt.Scale(domain=[-0.5, 20.5]),
                    axis=alt.Axis(tickCount=11)),
            y=alt.Y("G3:Q", title="Final Grade",
                    scale=alt.Scale(domain=[-0.5, 20.5]),
                    axis=alt.Axis(tickCount=11)),
            color=alt.Color("sex:N",
                            scale=alt.Scale(domain=SEX_DOMAIN, range=SEX_RANGE),
                            legend=None),
            opacity=filtered_opacity(sel_sex, sel_school, brush),
            tooltip=TOOLTIP,
        )
        .transform_filter(brush)
        .properties(title="G2 → G3 Progression", width=265, height=250)
    )

    scatter_g2_g3 = ref_line + scatter_g2_g3


    # ── C. Absences → G3 Scatter ──────────────────────────────────────────────────
    scatter_abs = (
        alt.Chart(df)
        .mark_circle(size=50, strokeWidth=0)
        .encode(
            x=alt.X("absences:Q", title="Absences",
                    scale=alt.Scale(domain=[-1, 94])),
            y=alt.Y("G3:Q", title="Final Grade",
                    scale=alt.Scale(domain=[-0.5, 20.5]),
                    axis=alt.Axis(tickCount=11)),
            color=alt.Color("sex:N",
                            scale=alt.Scale(domain=SEX_DOMAIN, range=SEX_RANGE),
                            legend=None),
            opacity=filtered_opacity(sel_sex, sel_school, brush),
            tooltip=TOOLTIP,
        )
        .transform_filter(brush)
        .properties(title="Absences vs Final Grade", width=265, height=250)
    )


    # ── D. G3 Box Plots by Study Time ─────────────────────────────────────────────
    box_study = (
        alt.Chart(df)
        .mark_boxplot(extent="min-max", size=26,
                      outliers=alt.MarkConfig(size=18, opacity=0.45))
        .encode(
            x=alt.X("studytime:O", title="Study Time",
                    axis=alt.Axis(
                        labelExpr=(
                            "datum.value == 1 ? '< 2h' : "
                            "datum.value == 2 ? '2-5h' : "
                            "datum.value == 3 ? '5-10h' : '> 10h'"
                        )
                    )),
            y=alt.Y("G3:Q", title="Final Grade",
                    scale=alt.Scale(domain=[-0.5, 20.5])),
            color=alt.Color("studytime:O",
                            scale=alt.Scale(range=ST_RANGE), legend=None),
            opacity=filtered_opacity(sel_sex, sel_school, brush),
        )
        .transform_filter(brush)
        .properties(title="Grade by Study Time", width=265, height=250)
    )


    # ── E. Mean G3 by Past Failures ───────────────────────────────────────────────
    bar_failures = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("failures:O", title="Past Failures"),
            y=alt.Y("mean(G3):Q", title="Mean Final Grade",
                    scale=alt.Scale(domain=[0, 20])),
            color=alt.Color("mean(G3):Q",
                            scale=alt.Scale(scheme="reds", domainMin=5, domainMax=15),
                            legend=None),
            opacity=filtered_opacity(sel_sex, sel_school, brush),
            tooltip=[
                alt.Tooltip("failures:O",  title="Failures"),
                alt.Tooltip("mean(G3):Q",  title="Mean grade", format=".2f"),
                alt.Tooltip("count():Q",   title="n"),
            ],
        )
        .transform_filter(brush)
        .properties(title="Mean Grade by Past Failures", width=265, height=250)
    )


    # ── F. Alcohol Heatmap ────────────────────────────────────────────────────────
    heatmap_alc = (
        alt.Chart(df)
        .mark_rect(stroke="#0d0f18", strokeWidth=1)
        .encode(
            x=alt.X("Dalc:O", title="Workday Alcohol (1-5)"),
            y=alt.Y("Walc:O", title="Weekend Alcohol"),
            color=alt.Color("mean(G3):Q",
                            scale=alt.Scale(scheme="blueorange", domainMid=10),
                            legend=alt.Legend(title="Mean Grade")),
            opacity=filtered_opacity(sel_sex, sel_school, brush),
            tooltip=[
                alt.Tooltip("Dalc:O",      title="Workday alcohol"),
                alt.Tooltip("Walc:O",      title="Weekend alcohol"),
                alt.Tooltip("mean(G3):Q",  title="Mean grade", format=".2f"),
                alt.Tooltip("count():Q",   title="n"),
            ],
        )
        .transform_filter(brush)
        .properties(title="Mean Grade by Alcohol", width=240, height=250)
    )


    # ── 7. Layout ─────────────────────────────────────────────────────────────────
    bottom_row = scatter_g2_g3 | scatter_abs | box_study | bar_failures | heatmap_alc

    dashboard = (
        alt.vconcat(hist_g3, bottom_row, spacing=30)
        .properties(
            title=alt.TitleParams(
                text="Student Grade Explorer",
                subtitle="All interactions live inside the chart — no external widgets",
                fontSize=20,
                fontWeight="normal",
                subtitleFontSize=11,
                subtitleColor="#5b6285",
                anchor="start",
                offset=16,
            )
        )
        .configure_concat(spacing=18)
        .configure_view(strokeWidth=1, stroke="#1a1e2e")
        .configure_legend(
            orient="right",
            direction="vertical",
            padding=12,
            titleFontSize=10,
            labelFontSize=10,
            rowPadding=6,
        )
    )

    # In Jupyter:
    dashboard

    # To save:
    # dashboard.save("grade_explorer.html")
    return (dashboard,)


@app.cell
def _(dashboard):
    dashboard
    return


if __name__ == "__main__":
    app.run()
