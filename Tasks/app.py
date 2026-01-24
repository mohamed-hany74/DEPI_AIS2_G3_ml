"""
Ford GoBike Interactive Dashboard - Simple Working Version
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
df = pd.read_csv("fordgobike-tripdataFor201902.csv")

print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Clean data
df.columns = df.columns.str.lower().str.strip()

# Parse dates correctly - handle the weird format
# First, let's check what the actual format is
print("Sample start_time values:")
print(df['start_time'].head(10))

# The format seems to be something like "32:10.1" which is invalid
# Let's try to parse it differently
df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce', format='%Y-%m-%d %H:%M.%S')

# If that didn't work, try another format
if df['start_time'].isna().sum() > len(df) * 0.9:
    print("Trying alternative date format...")
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')

# Remove rows with invalid dates
df = df.dropna(subset=['start_time'])

# Create required columns
df['day_of_week'] = df['start_time'].dt.day_name()
df['month'] = df['start_time'].dt.strftime('%b')
df['hour'] = df['start_time'].dt.hour
df['trip_duration_min'] = df['duration_sec'] / 60.0

# Create age from birth year
df['age'] = 2019 - df['member_birth_year']
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], 
                         labels=['Under 25', '25-35', '35-50', '50+'])

print(f"Date range: {df['start_time'].min()} to {df['start_time'].max()}")
print(f"User types: {df['user_type'].unique().tolist()}")
print(f"Genders: {df['member_gender'].unique().tolist()}")
print(f"Age groups: {df['age_group'].unique().tolist()}")

# Initialize app
app = Dash(__name__)
app.title = "Ford GoBike Dashboard"

# Get filter options
user_types = sorted(df['user_type'].dropna().unique().tolist())
genders = sorted(df['member_gender'].dropna().unique().tolist())
age_groups = sorted(df['age_group'].dropna().unique().tolist())

# Color scheme
colors = {
    "primary": "#00B4D8",
    "secondary": "#0077B6",
}

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Ford GoBike Dashboard", style={"color": "#1E3A8A", "marginBottom": "5px"}),
        html.P("Trip data analysis - February 2019", style={"color": "#666", "margin": "0"})
    ], style={"padding": "25px 30px", "background": "#F8FAFC", "borderBottom": "1px solid #E5E7EB"}),
    
    # Main container
    html.Div([
        # Sidebar
        html.Div([
            html.H3("Filters", style={"marginBottom": "20px"}),
            
            html.Label("User Type:", style={"fontWeight": "bold", "marginTop": "15px"}),
            dcc.Dropdown(
                id="user_type_filter",
                options=[{"label": u, "value": u} for u in user_types],
                value=user_types,
                multi=True
            ),
            
            html.Label("Gender:", style={"fontWeight": "bold", "marginTop": "15px"}),
            dcc.Dropdown(
                id="gender_filter",
                options=[{"label": g, "value": g} for g in genders],
                value=genders,
                multi=True
            ),
            
            html.Label("Age Group:", style={"fontWeight": "bold", "marginTop": "15px"}),
            dcc.Checklist(
                id="age_group_filter",
                options=[{"label": f"  {a}", "value": a} for a in age_groups],
                value=age_groups,
                style={"lineHeight": "2"}
            ),
        ], style={
            "width": "20%",
            "display": "inline-block",
            "verticalAlign": "top",
            "background": "#F0F9FF",
            "padding": "20px",
            "boxSizing": "border-box",
            "minHeight": "calc(100vh - 80px)",
            "borderRight": "1px solid #E5E7EB"
        }),
        
        # Main content
        html.Div([
            # KPI Section
            html.Div([
                html.H2("Overview KPIs", style={"fontSize": "18px", "marginBottom": "15px", "color": "#1E3A8A"}),
                html.Div(id="kpi_cards")
            ], style={"padding": "20px 25px", "background": "white"}),
            
            # Charts
            html.Div([
                html.Div([
                    html.Div(dcc.Graph(id="trips_weekday"), style={"width": "48%", "display": "inline-block"}),
                    html.Div(dcc.Graph(id="trips_month"), style={"width": "48%", "display": "inline-block", "float": "right"})
                ]),
                
                html.Div([
                    html.Div(dcc.Graph(id="user_type_pie"), style={"width": "48%", "display": "inline-block"}),
                    html.Div(dcc.Graph(id="gender_bar"), style={"width": "48%", "display": "inline-block", "float": "right"})
                ]),
                
                html.Div(dcc.Graph(id="age_dist"), style={"width": "100%"}),
                
                html.Div(dcc.Graph(id="top_stations"), style={"width": "100%"}),
            ], style={"padding": "0 25px 25px"})
        ], style={
            "width": "79%",
            "display": "inline-block",
            "verticalAlign": "top",
            "boxSizing": "border-box"
        })
    ], style={"display": "flex"})
], style={"fontFamily": "Arial, sans-serif", "margin": "0", "padding": "0", "background": "#FFFFFF"})

@app.callback(
    Output("kpi_cards", "children"),
    Output("trips_weekday", "figure"),
    Output("trips_month", "figure"),
    Output("user_type_pie", "figure"),
    Output("gender_bar", "figure"),
    Output("age_dist", "figure"),
    Output("top_stations", "figure"),
    Input("user_type_filter", "value"),
    Input("gender_filter", "value"),
    Input("age_group_filter", "value")
)
def update_charts(user_types_sel, genders_sel, age_groups_sel):
    # Filter data
    dff = df.copy()
    
    if user_types_sel:
        dff = dff[dff["user_type"].isin(user_types_sel)]
    
    if genders_sel:
        dff = dff[dff["member_gender"].isin(genders_sel)]
    
    if age_groups_sel:
        dff = dff[dff["age_group"].isin(age_groups_sel)]
    
    print(f"Filtered data: {len(dff)} rows")
    
    # KPIs
    total_trips = len(dff)
    avg_dur = dff["trip_duration_min"].mean()
    total_users = dff["bike_id"].nunique()
    pop_station = dff["start_station_name"].mode()[0] if len(dff) > 0 else "N/A"
    
    kpi_html = html.Div([
        html.Div([html.Div(f"{total_trips:,}", style={"fontSize": "28px", "fontWeight": "700"}), html.Div("Total Trips")], 
                style={"padding": "20px", "background": "#DBEAFE", "borderRadius": "8px", "textAlign": "center", "flex": "1", "margin": "5px"}),
        html.Div([html.Div(f"{avg_dur:.1f}", style={"fontSize": "28px", "fontWeight": "700"}), html.Div("Avg Duration (min)")], 
                style={"padding": "20px", "background": "#E0F2FE", "borderRadius": "8px", "textAlign": "center", "flex": "1", "margin": "5px"}),
        html.Div([html.Div(f"{total_users:,}", style={"fontSize": "28px", "fontWeight": "700"}), html.Div("Active Bikes")], 
                style={"padding": "20px", "background": "#CFFAFE", "borderRadius": "8px", "textAlign": "center", "flex": "1", "margin": "5px"}),
        html.Div([html.Div(pop_station[:20], style={"fontSize": "16px", "fontWeight": "700"}), html.Div("Popular Station")], 
                style={"padding": "20px", "background": "#D1FAE5", "borderRadius": "8px", "textAlign": "center", "flex": "1", "margin": "5px"})
    ], style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap", "marginTop": "10px"})
    
    # Chart 1: Trips by weekday
    trips_wd = dff.groupby("day_of_week").size()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    trips_wd = trips_wd.reindex(day_order, fill_value=0)
    fig1 = px.line(x=trips_wd.index, y=trips_wd.values, markers=True, title="Trips per Day of Week", height=300)
    fig1.update_layout(template="plotly_white", showlegend=False)
    
    # Chart 2: Trips by month
    trips_m = dff.groupby("month").size()
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    trips_m = trips_m.reindex(month_order, fill_value=0)
    fig2 = px.bar(x=trips_m.index, y=trips_m.values, color_discrete_sequence=[colors["secondary"]], title="Trips by Month", height=300)
    fig2.update_layout(template="plotly_white", showlegend=False)
    
    # Chart 3: User type pie
    user_counts = dff["user_type"].value_counts()
    fig3 = px.pie(values=user_counts.values, names=user_counts.index, title="User Type Distribution", height=300)
    fig3.update_layout(template="plotly_white")
    
    # Chart 4: Gender bar
    gender_counts = dff["member_gender"].value_counts()
    fig4 = px.bar(x=gender_counts.index, y=gender_counts.values, color_discrete_sequence=[colors["primary"]], title="Gender Distribution", height=300)
    fig4.update_layout(template="plotly_white", showlegend=False)
    
    # Chart 5: Age distribution
    fig5 = px.histogram(dff, x="age", nbins=20, color_discrete_sequence=[colors["primary"]], title="Age Distribution", height=350)
    fig5.update_layout(template="plotly_white", showlegend=False)
    
    # Chart 6: Top stations
    top_st = dff.groupby("start_station_name").size().nlargest(10).reset_index(name="trips")
    fig6 = px.barh(top_st, y="start_station_name", x="trips", color="trips", color_continuous_scale="Blues", title="Top 10 Start Stations", height=400)
    fig6.update_layout(template="plotly_white", showlegend=False)
    
    return kpi_html, fig1, fig2, fig3, fig4, fig5, fig6

if __name__ == "__main__":
    print("🚀 Running on http://localhost:8050")
    app.run(debug=True, port=8050)