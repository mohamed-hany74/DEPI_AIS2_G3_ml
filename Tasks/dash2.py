"""
Ford GoBike Interactive Dashboard - Advanced Version
Run: pip install dash pandas plotly && python app.py
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import datetime

CSV_PATH = "cleaned_fordgobike.csv"

def generate_dummy(n=2000):
    """Generate realistic dummy bike data"""
    dates = pd.date_range("2020-01-01", periods=365, freq="D")
    start_times = []
    for _ in range(n):
        date = np.random.choice(dates)
        hour = np.random.choice(range(24), p=[0.02]*24)
        start_times.append(date + pd.Timedelta(hours=hour))
    
    stations = ["Market St @ 7th", "Howard St", "Embarcadero", "Mission St", "Van Ness Ave", "Ferry Plaza", "2nd @ Pine"]
    df = pd.DataFrame({
        "trip_id": range(1, n+1),
        "start_time": start_times,
        "end_time": [t + pd.Timedelta(minutes=np.random.exponential(15)) for t in start_times],
        "duration_sec": np.random.exponential(scale=900, size=n).astype(int),
        "start_station_name": np.random.choice(stations, size=n),
        "end_station_name": np.random.choice(stations, size=n),
        "start_station_latitude": np.random.uniform(37.76, 37.80, size=n),
        "start_station_longitude": np.random.uniform(-122.45, -122.39, size=n),
        "end_station_latitude": np.random.uniform(37.76, 37.80, size=n),
        "end_station_longitude": np.random.uniform(-122.45, -122.39, size=n),
        "user_type": np.random.choice(["Subscriber", "Customer"], size=n, p=[0.7, 0.3]),
        "member_gender": np.random.choice(["Male", "Female", "Other"], size=n, p=[0.5, 0.45, 0.05]),
        "member_birth_year": np.random.randint(1950, 2005, size=n)
    })
    
    df["day_of_week"] = df["start_time"].dt.day_name()
    df["month"] = df["start_time"].dt.strftime("%b")
    df["hour"] = df["start_time"].dt.hour
    df["date"] = df["start_time"].dt.date
    df["age"] = 2024 - df["member_birth_year"]
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 50, 100], labels=["Under 25", "25-35", "35-50", "50+"])
    df["trip_duration_min"] = df["duration_sec"] / 60.0
    
    return df

def load_data():
    """Load or generate data"""
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, parse_dates=["start_time", "end_time"])
    else:
        print("[info] Generating demo dataset...")
        df = generate_dummy(2000)
    
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["trip_duration_min"] = df["duration_sec"] / 60.0
    
    if "age_group" not in df.columns:
        df["age"] = 2024 - df.get("member_birth_year", 1980)
        df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 50, 100], labels=["Under 25", "25-35", "35-50", "50+"])
    
    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["start_time"].dt.day_name()
    if "month" not in df.columns:
        df["month"] = df["start_time"].dt.strftime("%b")
    if "hour" not in df.columns:
        df["hour"] = df["start_time"].dt.hour
    
    return df

df = load_data()

# Initialize app
app = Dash(__name__)
app.title = "Ford GoBike Dashboard"

# Filter options
user_types = sorted([x for x in df["user_type"].dropna().unique() if pd.notna(x)])
genders = sorted([x for x in df["member_gender"].dropna().unique() if pd.notna(x)])
age_groups = sorted([x for x in df["age_group"].dropna().unique() if pd.notna(x)])

# Color scheme
colors = {
    "primary": "#00B4D8",
    "secondary": "#0077B6",
    "accent": "#00B4D8",
    "dark": "#1E3A8A",
    "light": "#F0F9FF",
    "text": "#1F2937",
    "border": "#E5E7EB"
}

app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("Ford GoBike Interactive Dashboard", 
                style={"margin": "0", "color": colors["dark"], "fontSize": "28px", "fontWeight": "700"}),
            html.P("Real-time bike-sharing analytics and insights | Feb 2020",
                style={"margin": "5px 0 0 0", "color": "#6B7280", "fontSize": "13px"})
        ], style={"flex": "1"}),
        html.Div("📊 Active Dashboard", 
            style={"padding": "8px 12px", "background": "#DBEAFE", "borderRadius": "6px", "fontSize": "12px", "fontWeight": "600", "color": colors["dark"]})
    ], style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "padding": "25px 30px",
        "borderBottom": f"1px solid {colors['border']}",
        "background": "#F8FAFC"
    }),
    
    # Main container
    html.Div([
        # Sidebar
        html.Div([
            html.Div([
                html.H3("Filters", style={"marginBottom": "20px", "fontSize": "16px", "fontWeight": "700", "color": colors["dark"]}),
                
                # Date range
                html.Label("Date range", style={"fontSize": "12px", "fontWeight": "600", "color": "#6B7280", "display": "block", "marginBottom": "8px"}),
                dcc.DatePickerRange(
                    id="date_range",
                    min_date_allowed=df["start_time"].min().date(),
                    max_date_allowed=df["start_time"].max().date(),
                    start_date=df["start_time"].min().date(),
                    end_date=df["start_time"].max().date(),
                    display_format="YYYY-MM-DD",
                    style={"width": "100%"}
                ),
                html.Br(), html.Br(),
                
                # User type
                html.Label("User Type", style={"fontSize": "12px", "fontWeight": "600", "color": "#6B7280", "display": "block", "marginBottom": "8px"}),
                dcc.Dropdown(
                    id="user_type_filter",
                    options=[{"label": u, "value": u} for u in user_types],
                    value=user_types,
                    multi=True,
                    style={"width": "100%"}
                ),
                html.Br(),
                
                # Gender
                html.Label("Gender", style={"fontSize": "12px", "fontWeight": "600", "color": "#6B7280", "display": "block", "marginBottom": "8px"}),
                dcc.Dropdown(
                    id="gender_filter",
                    options=[{"label": g, "value": g} for g in genders],
                    value=genders,
                    multi=True,
                    style={"width": "100%"}
                ),
                html.Br(),
                
                # Age group
                html.Label("Age Group", style={"fontSize": "12px", "fontWeight": "600", "color": "#6B7280", "display": "block", "marginBottom": "8px"}),
                dcc.Checklist(
                    id="age_group_filter",
                    options=[{"label": f"  {a}", "value": a} for a in age_groups],
                    value=age_groups,
                    style={"lineHeight": "2.2", "fontSize": "13px"}
                ),
                
                html.Hr(style={"margin": "20px 0", "border": "none", "borderTop": f"1px solid {colors['border']}"}),
                html.Div("Tip: use filters to update all charts.", 
                    style={"fontSize": "11px", "color": "#9CA3AF", "fontStyle": "italic"})
            ], style={"padding": "20px"})
        ], style={
            "width": "20%",
            "display": "inline-block",
            "verticalAlign": "top",
            "background": colors["light"],
            "minHeight": "calc(100vh - 80px)",
            "boxSizing": "border-box",
            "borderRight": f"1px solid {colors['border']}"
        }),
        
        # Main content
        html.Div([
            # KPI Section
            html.Div([
                html.H2("Overview KPIs", style={"fontSize": "18px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                html.Div(id="kpi_cards")
            ], style={"padding": "25px"}),
            
            # Charts section
            html.Div([
                # Time analysis
                html.Div([
                    html.H3("Time Analysis", style={"fontSize": "16px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                    html.Div([
                        html.Div(dcc.Graph(id="trips_by_weekday"), style={"width": "48%", "display": "inline-block", "marginRight": "2%"}),
                        html.Div(dcc.Graph(id="trips_by_month"), style={"width": "48%", "display": "inline-block"})
                    ])
                ], style={"padding": "0 25px", "marginBottom": "20px"}),
                
                # User analysis
                html.Div([
                    html.H3("User Type", style={"fontSize": "16px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                    html.Div([
                        html.Div(dcc.Graph(id="user_type_pie"), style={"width": "48%", "display": "inline-block", "marginRight": "2%"}),
                        html.Div(dcc.Graph(id="gender_bar"), style={"width": "48%", "display": "inline-block"})
                    ])
                ], style={"padding": "0 25px", "marginBottom": "20px"}),
                
                # Age analysis
                html.Div([
                    html.H3("User Analysis", style={"fontSize": "16px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                    dcc.Graph(id="age_distribution", style={"width": "100%"})
                ], style={"padding": "0 25px", "marginBottom": "20px"}),
                
                # Station & routes analysis
                html.Div([
                    html.H3("Station & Trip Analysis", style={"fontSize": "16px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                    html.Div([
                        html.Div(dcc.Graph(id="station_map"), style={"width": "60%", "display": "inline-block", "marginRight": "2%"}),
                        html.Div(dcc.Graph(id="top_routes"), style={"width": "38%", "display": "inline-block"})
                    ])
                ], style={"padding": "0 25px", "marginBottom": "20px"}),
                
                # Heatmap
                html.Div([
                    html.H3("Most popular routes", style={"fontSize": "16px", "fontWeight": "700", "color": colors["dark"], "marginBottom": "15px"}),
                    dcc.Graph(id="hourly_heatmap")
                ], style={"padding": "0 25px 25px"})
                
            ])
        ], style={
            "width": "79%",
            "display": "inline-block",
            "boxSizing": "border-box",
            "verticalAlign": "top",
            "background": "#FFFFFF"
        })
    ], style={"display": "flex", "minHeight": "calc(100vh - 80px)"})
], style={"fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", "margin": "0", "padding": "0", "background": "#FFFFFF"})

@app.callback(
    Output("kpi_cards", "children"),
    Output("trips_by_weekday", "figure"),
    Output("trips_by_month", "figure"),
    Output("user_type_pie", "figure"),
    Output("gender_bar", "figure"),
    Output("age_distribution", "figure"),
    Output("station_map", "figure"),
    Output("top_routes", "figure"),
    Output("hourly_heatmap", "figure"),
    [
        Input("date_range", "start_date"),
        Input("date_range", "end_date"),
        Input("user_type_filter", "value"),
        Input("gender_filter", "value"),
        Input("age_group_filter", "value")
    ]
)
def update_dashboard(start_date, end_date, user_type_list, gender_list, age_group_list):
    """Update all dashboard components"""
    try:
        dff = df.copy()
        
        # Apply filters
        if start_date:
            dff = dff[dff["start_time"] >= pd.to_datetime(start_date)]
        if end_date:
            dff = dff[dff["start_time"] <= pd.to_datetime(end_date) + pd.Timedelta(days=1)]
        
        if user_type_list and len(user_type_list) > 0:
            dff = dff[dff["user_type"].isin(user_type_list)]
        
        if gender_list and len(gender_list) > 0:
            dff = dff[dff["member_gender"].isin(gender_list)]
        
        if age_group_list and len(age_group_list) > 0:
            dff = dff[dff["age_group"].isin(age_group_list)]
        
        # KPIs
        total_trips = len(dff)
        avg_duration = dff["trip_duration_min"].mean() if total_trips > 0 else 0
        unique_users = dff["trip_id"].nunique() if total_trips > 0 else 0
        popular_station = dff["start_station_name"].mode().values[0] if len(dff) > 0 and len(dff["start_station_name"].mode()) > 0 else "N/A"
        
        # KPI Cards HTML
        kpi_cards = html.Div([
            html.Div([
                html.Div(f"{total_trips:,}", style={"fontSize": "28px", "fontWeight": "700", "color": colors["primary"]}),
                html.Div("Trips", style={"fontSize": "12px", "color": "#6B7280", "marginTop": "4px"})
            ], style={
                "padding": "20px", "background": "#DBEAFE", "borderRadius": "10px", 
                "textAlign": "center", "flex": "1", "margin": "8px"
            }),
            html.Div([
                html.Div(f"{avg_duration:.1f} mins", style={"fontSize": "28px", "fontWeight": "700", "color": colors["secondary"]}),
                html.Div("Avg duration", style={"fontSize": "12px", "color": "#6B7280", "marginTop": "4px"})
            ], style={
                "padding": "20px", "background": "#E0F2FE", "borderRadius": "10px",
                "textAlign": "center", "flex": "1", "margin": "8px"
            }),
            html.Div([
                html.Div(f"{unique_users:,}", style={"fontSize": "28px", "fontWeight": "700", "color": "#0891B2"}),
                html.Div("Active users", style={"fontSize": "12px", "color": "#6B7280", "marginTop": "4px"})
            ], style={
                "padding": "20px", "background": "#CFFAFE", "borderRadius": "10px",
                "textAlign": "center", "flex": "1", "margin": "8px"
            }),
            html.Div([
                html.Div("📍", style={"fontSize": "24px"}),
                html.Div(popular_station[:20], style={"fontSize": "12px", "fontWeight": "600", "color": colors["dark"], "marginTop": "4px"}),
                html.Div("Most popular station", style={"fontSize": "11px", "color": "#6B7280"})
            ], style={
                "padding": "20px", "background": "#D1FAE5", "borderRadius": "10px",
                "textAlign": "center", "flex": "1", "margin": "8px"
            })
        ], style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap", "marginTop": "10px"})
        
        # Trips by weekday
        trips_wd = dff.groupby("day_of_week").size()
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        trips_wd = trips_wd.reindex(day_order, fill_value=0)
        fig_weekday = go.Figure()
        fig_weekday.add_trace(go.Scatter(x=trips_wd.index, y=trips_wd.values, mode="lines+markers",
            line=dict(color=colors["primary"], width=3), marker=dict(size=8),
            fill="tozeroy", fillcolor="rgba(0, 180, 216, 0.1)", name="Trips"))
        fig_weekday.update_layout(template="plotly_white", showlegend=False, height=300)
        fig_weekday.update_xaxes(title_text="Day of week", tickangle=-45)
        fig_weekday.update_yaxes(title_text="Number of trips")
        
        # Trips by month
        if "month" in dff.columns:
            trips_month = dff.groupby("month").size()
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            trips_month = trips_month.reindex(month_order, fill_value=0)
        else:
            trips_month = dff.groupby(dff["start_time"].dt.strftime("%b")).size().reindex(
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fill_value=0)
        
        fig_month = px.bar(x=trips_month.index, y=trips_month.values, 
            color_discrete_sequence=[colors["secondary"]], height=300)
        fig_month.update_layout(template="plotly_white", showlegend=False)
        fig_month.update_xaxes(title_text="Month")
        fig_month.update_yaxes(title_text="Number of trips")
        
        # User type pie
        user_type_counts = dff["user_type"].value_counts()
        fig_user_type = px.pie(values=user_type_counts.values, names=user_type_counts.index,
            color_discrete_sequence=[colors["primary"], colors["secondary"]], height=300)
        fig_user_type.update_layout(template="plotly_white")
        
        # Gender bar
        gender_counts = dff["member_gender"].value_counts()
        fig_gender = px.bar(x=gender_counts.index, y=gender_counts.values,
            color_discrete_sequence=[colors["accent"]], height=300)
        fig_gender.update_layout(template="plotly_white", showlegend=False)
        fig_gender.update_xaxes(title_text="Gender")
        fig_gender.update_yaxes(title_text="Count")
        
        # Age distribution
        fig_age = px.histogram(dff, x="age", nbins=20, color_discrete_sequence=[colors["primary"]],
            height=400, title="Age Distribution")
        fig_age.update_layout(template="plotly_white", showlegend=False)
        fig_age.update_xaxes(title_text="Age")
        fig_age.update_yaxes(title_text="Frequency")
        
        # Station map
        if not dff.empty and "start_station_latitude" in dff.columns:
            station_data = dff.groupby(["start_station_name", "start_station_latitude", "start_station_longitude"]).size().reset_index(name="trips")
            fig_map = px.scatter_mapbox(station_data, lat="start_station_latitude", lon="start_station_longitude",
                size="trips", hover_name="start_station_name", zoom=11, height=450)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        else:
            fig_map = go.Figure()
        
        # Top routes
        routes = dff.groupby("start_station_name").size().nlargest(10).reset_index(name="trips")
        fig_routes = px.barh(routes, y="start_station_name", x="trips",
            color="trips", color_continuous_scale="Blues", height=450)
        fig_routes.update_layout(template="plotly_white", showlegend=False)
        fig_routes.update_yaxes(title_text="Station")
        fig_routes.update_xaxes(title_text="Number of trips")
        
        # Hourly heatmap
        heatmap_data = dff.groupby(["hour", "day_of_week"]).size().reset_index(name="trips")
        heatmap_pivot = heatmap_data.pivot(index="hour", columns="day_of_week", values="trips").fillna(0)
        day_order_full = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_pivot = heatmap_pivot.reindex(columns=day_order_full, fill_value=0)
        
        fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_pivot.values, x=heatmap_pivot.columns, 
            y=heatmap_pivot.index, colorscale="Blues", colorbar=dict(title="Trips")))
        fig_heatmap.update_layout(height=300, template="plotly_white")
        fig_heatmap.update_xaxes(title_text="Day of week")
        fig_heatmap.update_yaxes(title_text="Hour of day")
        
        return kpi_cards, fig_weekday, fig_month, fig_user_type, fig_gender, fig_age, fig_map, fig_routes, fig_heatmap
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return html.Div("Error"), {}, {}, {}, {}, {}, {}, {}, {}

if __name__ == "__main__":
    print("🚀 Dashboard running on http://localhost:8050")
    app.run(debug=True, port=8050)