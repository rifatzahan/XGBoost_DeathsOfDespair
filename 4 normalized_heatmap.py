import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Load your dataset
df = pd.read_csv(r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Suicide Opioid Alcohol\US_Mortality_2019_2023_deaths_of_despair_only_recoded.csv", low_memory=False)

# Helper: Generate normalized heatmap
def generate_heatmap_figure(df, row_var, col_var, title):
    heatmap_data = df.groupby([row_var, col_var]).size().unstack(fill_value=0)
    heatmap_percent = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_percent.values,
        x=heatmap_percent.columns.astype(str),
        y=heatmap_percent.index.astype(str),
        colorscale='YlGnBu',
        text=heatmap_percent.round(1).astype(str) + '%',
        hoverinfo='text',
        showscale=True
    ))

    fig.update_layout(
        title=title,
        xaxis_title=col_var,
        yaxis_title=row_var,
        autosize=False,
        width=800,  # 📏 Smaller plot size
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(size=12),
    )
    return fig

def generate_stacked_bar_plot(df, row_var, col_var, title):
    count_df = df.groupby([row_var, col_var]).size().reset_index(name='count')
    total_per_row = count_df.groupby(row_var)['count'].transform('sum')
    count_df['percent'] = count_df['count'] / total_per_row * 100

    fig = px.bar(
        count_df, x=row_var, y='percent', color=col_var,
        barmode='stack', text=count_df['percent'].round(1).astype(str) + '%',
        title=title,
        opacity=0.85,  # 🎨 Slight transparency
        color_discrete_sequence=px.colors.qualitative.Pastel  # 🟣 Soft palette
    )

    fig.update_layout(
        yaxis_title='Percentage',
        xaxis_title=row_var,
        legend_title=col_var,
        width=800,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        yaxis=dict(ticksuffix='%'),
        font=dict(size=12),
    )

    return fig

def generate_monthly_trend_plot(df, year_col='Data Year', month_col='Month_Of_Death', cause_col='Cause of Death'):
    # Step 1: Map month names to numbers
    month_map = {
        'January': '01', 'February': '02', 'March': '03',
        'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09',
        'October': '10', 'November': '11', 'December': '12'
    }

    # Step 2: Apply mapping
    df[month_col] = df[month_col].astype(str).str.strip().map(month_map)
    df[year_col] = df[year_col].astype(str).str.strip()

    # Step 3: Combine and convert to datetime
    df['Year_Month'] = pd.to_datetime(df[year_col] + '-' + df[month_col], format='%Y-%m', errors='coerce')
    df = df[df['Year_Month'].notna()]

    # Step 4: Group and plot
    trend_data = df.groupby(['Year_Month', cause_col]).size().reset_index(name='Deaths')

    fig = px.line(
        trend_data, x='Year_Month', y='Deaths', color=cause_col,
        title="Monthly Trend of Deaths by Case of Death",
        markers=True
    )

    fig.update_layout(
        xaxis_title='Year-Month',
        yaxis_title='Number of Deaths',
        width=900,
        height=500,
        font=dict(size=12),
        margin=dict(l=40, r=40, t=40, b=40),
        legend_title=cause_col
    )

    return fig



# List of plots to generate
plot_specs = [
    ('Age Group', 'Sex', 'Deaths by Age Group and Sex'),
    ('Education', 'Sex', 'Deaths by Education Level and Sex'),
    ('Occupation', 'Cause of Death', 'Deaths by Occupation and Cause'),
    ('Marital Status', 'Cause of Death', 'Deaths by Marital Status and Cause'),
    ('Age Group', 'Cause of Death', 'Deaths by Age Group and Cause'),
    ('Education', 'Cause of Death', 'Deaths by Education and Cause'),
    ('Sex', 'Marital Status', 'Deaths by Sex and Marital Status'),
    ('Race', 'Cause of Death', 'Deaths by Race and Cause')
]

# Generate all figures (heatmaps + bar plots)
all_figures = []
for row, col, title in plot_specs:
    heatmap_title = f"{title} (%)"
    bar_title = f"{title} (Stacked Bar)"
    all_figures.append(generate_heatmap_figure(df, row, col, heatmap_title))
    all_figures.append(generate_stacked_bar_plot(df, row, col, bar_title))

# Add monthly trend plot at the end
trend_fig = generate_monthly_trend_plot(df)
all_figures.append(trend_fig)



# Save all plots to a single HTML
html_output_path = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Suicide Opioid Alcohol\visualization_deathsOfDespair.html"

with open(html_output_path, 'w') as f:
    for fig in all_figures:
        f.write(pio.to_html(fig, include_plotlyjs='cdn', full_html=False))


print(f"✅ All interactive heatmaps and stacked bar plots saved to:\n{html_output_path}")
