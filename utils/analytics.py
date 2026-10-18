import plotly.graph_objects as go


def create_skill_chart(matched, missing):

    labels = ["Matched Skills", "Missing Skills"]

    values = [matched, missing]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                text=values,
                textposition="auto"
            )
        ]
    )

    fig.update_layout(
        title="Skill Match Analysis",
        xaxis_title="Skill Type",
        yaxis_title="Number of Skills",
        height=400
    )

    return fig


def create_score_chart(job_score, skill_score):

    labels = [
        "Job Similarity",
        "Skill Match"
    ]

    values = [
        job_score,
        skill_score
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                text=values,
                texttemplate="%{text}%",
                textposition="auto"
            )
        ]
    )

    fig.update_layout(
        title="Resume Performance",
        yaxis_title="Score (%)",
        yaxis=dict(
            range=[0, 100]
        ),
        height=400
    )

    return fig