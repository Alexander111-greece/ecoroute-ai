import plotly.graph_objects as go
import plotly.express as px

import streamlit as st
import pandas as pd

# Your other imports
from carbon import calculate_carbonimport plotly.graph_objects as go
import plotly.express as px

import streamlit as st
import pandas as pd

# Your other imports
from carbon import calculate_carbon, calculate_fuel_cost, calculate_carbon_saved, get_carbon_score
from routes import get_route_legs, get_distance

# Rest of your code...

# Rest of your code starts here...

st.set_page_config(page_title="EcoRoute AI", page_icon="🌱", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: radial-gradient(ellipse at top, #0d1f14 0%, #0f1117 50%, #0a0e1a 100%); }
.block-container { padding-top: 2rem !important; }
.hero-banner {
    background: linear-gradient(135deg, #0d6e3f 0%, #1a9e5c 50%, #0d6e3f 100%);
    border-radius: 16px; padding: 40px; margin-bottom: 30px;
    text-align: center; box-shadow: 0 8px 32px rgba(26,158,92,0.3);
}
.hero-banner h1 { font-size: 2.8rem; font-weight: 700; color: white; margin: 0; }
.hero-banner p { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 8px; }
.section-header {
    font-size: 1.3rem; font-weight: 600; color: #e8eaf0;
    border-left: 4px solid #1a9e5c; padding-left: 12px; margin: 24px 0 16px 0;
}
.insight-box {
    background: linear-gradient(135deg, #0d2b1a, #0f3d24);
    border: 1px solid #1a9e5c; border-radius: 12px; padding: 20px 24px; margin-top: 20px;
}
.insight-box p { color: #7effc0; font-size: 1rem; margin: 0; }
.badge {
    display: inline-block; background: #0d2b1a; color: #1a9e5c;
    border: 1px solid #1a9e5c; border-radius: 20px;
    padding: 4px 14px; font-size: 0.8rem; font-weight: 600; margin: 2px;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #1e2130; padding: 8px; border-radius: 12px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 20px; font-weight: 500; color: #8b95a8; }
.stTabs [aria-selected="true"] { background: #1a9e5c !important; color: white !important; }
div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #1a9e5c !important; font-weight: 700 !important; }
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1a1f2e, #1e2535);
    border: 1px solid #2d3348; border-radius: 12px; padding: 16px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1a9e5c, #0d6e3f); color: white;
    border: none; border-radius: 10px; padding: 14px 28px;
    font-size: 1rem; font-weight: 600; width: 100%;
    box-shadow: 0 4px 15px rgba(26,158,92,0.4);
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🌍 EcoRoute AI")
    st.markdown("---")
    st.markdown("**Platform Stats**")
    st.metric("🚛 Routes Analyzed", "1,284")
    st.metric("💨 CO₂ Saved (tons)", "48.6")
    st.metric("🌳 Trees Equivalent", "2,314")
    st.metric("🏙️ Cities Covered", "24")
    st.markdown("---")
    st.markdown("**Supported Vehicles**")
    st.success("✅ Electric Vehicle")
    st.warning("⚠️ CNG Truck")
    st.error("🔴 Diesel Truck")
    st.markdown("---")
    st.markdown("**SDG Alignment**")
    st.markdown("🎯 SDG 13 — Climate Action")
    st.markdown("🏙️ SDG 11 — Sustainable Cities")
    st.markdown("⚙️ SDG 9 — Industry & Innovation")
    st.markdown("---")
    st.info("💡 Switch to EV to reduce emissions by up to 87%")

# HERO
st.markdown("""
<div class="hero-banner">
    <h1>🌱 EcoRoute AI</h1>
    <p>Sustainable Logistics Route Optimization & Carbon Reduction Platform</p>
    <div style="margin-top:14px">
        <span class="badge">🎯 Climate Action</span>
        <span class="badge">📦 SCM Optimized</span>
        <span class="badge">🌍 SDG 13 Aligned</span>
        <span class="badge">⚡ Real-time Analysis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["🚚  Single Route Analyzer", "📦  Multi-Stop SCM Route", "📊  Vehicle Comparison"])

# ── TAB 1 ──────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Route Input</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        origin = st.text_input("🏭 Origin — Warehouse / Factory", placeholder="e.g. Mumbai")
        stop1 = st.text_input("📍 Delivery Stop 1", placeholder="e.g. Pune")
        stop2 = st.text_input("📍 Delivery Stop 2 (optional)", placeholder="e.g. Nashik")

    with col2:
        vehicle_type = st.selectbox("🚛 Vehicle Type", [
            "Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"
        ])
        load_weight = st.slider("⚖️ Load Weight (tons)", 1, 30, 5)
        priority = st.radio("🎯 Optimization Priority", [
            "Minimize Carbon Emissions", "Balance Carbon + Time", "Minimize Time"
        ])

    st.markdown("")
    if st.button("⚡ Calculate EcoRoute", key="single"):
        dist1 = get_distance(origin, stop1) if origin and stop1 else 200
        dist2 = get_distance(stop1, stop2) if stop2 else 0
        total_distance = dist1 + dist2

        total_co2 = calculate_carbon(total_distance, vehicle_type, load_weight)
        total_cost = calculate_fuel_cost(total_distance, vehicle_type)
        co2_saved = calculate_carbon_saved(total_distance, vehicle_type, load_weight)
        score = get_carbon_score(total_co2, total_distance)
        trees = round(co2_saved / 21, 1)

        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📏 Total Distance", f"{total_distance} km")
        with c2:
            st.metric("💨 CO₂ Emitted", f"{total_co2} kg")
        with c3:
            st.metric("🌱 CO₂ Saved", f"{co2_saved} kg")
        with c4:
            st.metric("💰 Fuel Cost", f"₹{total_cost}")

        # Vehicle comparison chart
        st.markdown('<div class="section-header">Vehicle Carbon Comparison</div>', unsafe_allow_html=True)
        vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
        co2_values = [calculate_carbon(total_distance, v, load_weight) for v in vehicles]
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#1a9e5c"]

        fig = go.Figure(go.Bar(
            x=vehicles, y=co2_values, marker_color=colors,
            text=[f"{v} kg" for v in co2_values],
            textposition="outside", textfont=dict(color="white", size=13),
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            xaxis=dict(showgrid=False, tickfont=dict(size=12)),
            yaxis=dict(showgrid=True, gridcolor="#2d3348", title="CO₂ Emitted (kg)"),
            margin=dict(t=20, b=20), height=380, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, key="chart_single")
        # AI Recommendation
        st.markdown('<div class="section-header">🤖 AI Recommendation</div>', unsafe_allow_html=True)
        rec_col1, rec_col2 = st.columns(2)

        all_vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
        all_co2 = {v: calculate_carbon(total_distance, v, load_weight) for v in all_vehicles}
        best_vehicle = min(all_co2, key=all_co2.get)
        best_co2 = all_co2[best_vehicle]

        with rec_col1:
            if vehicle_type == best_vehicle:
                st.success(f"✅ You already chose the best option! **{best_vehicle}** emits the least CO₂ on this route.")
            else:
                potential_saving = round(total_co2 - best_co2, 2)
                st.warning(f"💡 Switching to **{best_vehicle}** would save an additional **{potential_saving} kg CO₂** on this route.")

        with rec_col2:
            carbon_credits = round(co2_saved / 1000, 4)
            credit_value = round(carbon_credits * 1500, 2)
            st.info(f"💰 Carbon Credits Earned: **{carbon_credits} credits**\n\nEstimated Value: **₹{credit_value}**")

        st.markdown(f"""
        <div class="insight-box">
            <p>🌳 By choosing <strong>{vehicle_type}</strong> on this {total_distance} km route,
            you saved <strong>{co2_saved} kg of CO₂</strong> — equivalent to planting
            <strong>{trees} trees</strong>. Carbon Score: {"⭐" * score}</p>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 2 ──────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Supply Chain Route Planner</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        warehouse = st.text_input("🏭 Warehouse (Origin)", placeholder="e.g. Mumbai")
        dest1 = st.text_input("📍 Stop 1 — Distributor", placeholder="e.g. Pune")
        dest2 = st.text_input("📍 Stop 2 — Retailer A", placeholder="e.g. Nashik")
        dest3 = st.text_input("📍 Stop 3 — Retailer B (optional)", placeholder="e.g. Aurangabad")
        dest4 = st.text_input("📍 Stop 4 — Retailer C (optional)", placeholder="e.g. Nagpur")

    with col_b:
        scm_vehicle = st.selectbox("🚛 Fleet Vehicle Type", [
            "Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"
        ], key="scm_v")
        scm_load = st.slider("⚖️ Load Weight (tons)", 1, 30, 10, key="scm_l")
        num_trucks = st.number_input("🚛 Fleet Size", 1, 50, 3)

    st.markdown("")
    if st.button("⚡ Optimize SCM Route", use_container_width=True, key="scm"):
        all_stops = [warehouse, dest1, dest2, dest3, dest4]
        stops = [s.strip().title() for s in all_stops if s.strip()]

        if len(stops) < 2:
            st.error("Please enter at least a warehouse and one delivery stop.")
        else:
            legs = get_route_legs(stops)
            leg_data = []
            total_dist = 0
            total_co2_scm = 0
            total_cost_scm = 0

            for i, leg in enumerate(legs):
                co2 = calculate_carbon(leg["distance_km"], scm_vehicle, scm_load)
                cost = calculate_fuel_cost(leg["distance_km"], scm_vehicle)
                score = get_carbon_score(co2, leg["distance_km"])
                total_dist += leg["distance_km"]
                total_co2_scm += co2
                total_cost_scm += cost
                leg_data.append({
                    "Leg": f"Leg {i+1}",
                    "From": leg["from"],
                    "To": leg["to"],
                    "Distance (km)": leg["distance_km"],
                    "CO₂ Emitted (kg)": co2,
                    "Fuel Cost (₹)": cost,
                    "Carbon Score": "⭐" * score
                })

            df = pd.DataFrame(leg_data)
            st.markdown('<div class="section-header">Route Leg Breakdown</div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

            fig2 = px.bar(
                df, x="Leg", y="CO₂ Emitted (kg)",
                color="CO₂ Emitted (kg)",
                color_continuous_scale=["#1a9e5c", "#f1c40f", "#e74c3c"],
                text="CO₂ Emitted (kg)"
            )
            fig2.update_traces(textposition="outside", textfont=dict(color="white"))
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#2d3348"),
                margin=dict(t=20, b=20), height=320,
                showlegend=False, coloraxis_showscale=False
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Fleet Summary
            st.markdown('<div class="section-header">Fleet Summary</div>', unsafe_allow_html=True)
            fleet_co2 = round(total_co2_scm * num_trucks, 2)
            fleet_cost = round(total_cost_scm * num_trucks, 2)
            fleet_saved = round(calculate_carbon_saved(total_dist, scm_vehicle, scm_load) * num_trucks, 2)
            trees_fleet = round(fleet_saved / 21, 1)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("📏 Total Distance", f"{total_dist} km")
            with m2:
                st.metric("💨 Fleet CO₂", f"{fleet_co2} kg")
            with m3:
                st.metric("🌱 CO₂ Saved", f"{fleet_saved} kg")
            with m4:
                st.metric("🌳 Trees Equivalent", f"{trees_fleet}")

            # Load Consolidation
            st.markdown('<div class="section-header">📦 Load Consolidation Suggestion</div>', unsafe_allow_html=True)
            cons_col1, cons_col2 = st.columns(2)

            with cons_col1:
                if num_trucks > 1:
                    consolidated_trucks = max(1, num_trucks - 1)
                    saved_trips_co2 = round(total_co2_scm * (num_trucks - consolidated_trucks), 2)
                    saved_trips_cost = round(total_cost_scm * (num_trucks - consolidated_trucks), 2)
                    st.success(f"💡 Consolidating **{num_trucks} → {consolidated_trucks} trucks** saves:\n\n"
                               f"**{saved_trips_co2} kg CO₂** and **₹{saved_trips_cost}** in fuel per trip cycle.")
                else:
                    st.info("✅ Already running a single truck — fully consolidated!")

            with cons_col2:
                fleet_credits = round(fleet_saved / 1000, 4)
                fleet_credit_value = round(fleet_credits * 1500, 2)
                st.info(f"💰 Fleet Carbon Credits: **{fleet_credits} credits**\n\nEstimated Value: **₹{fleet_credit_value}**")

            st.markdown(f"""
            <div class="insight-box">
                <p>🚛 Your <strong>{num_trucks}-truck fleet</strong> covers <strong>{total_dist} km</strong>
                across {len(legs)} supply chain legs. Using <strong>{scm_vehicle}</strong>,
                you save <strong>{fleet_saved} kg CO₂</strong> — like planting <strong>{trees_fleet} trees</strong> per trip cycle.</p>
            </div>
            """, unsafe_allow_html=True)

# ── TAB 3 ──────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Compare All Vehicle Types</div>', unsafe_allow_html=True)
    cc1, cc2 = st.columns(2)
    with cc1:
        comp_distance = st.slider("📏 Route Distance (km)", 50, 1000, 300, key="comp_d")
    with cc2:
        comp_load = st.slider("⚖️ Load Weight (tons)", 1, 30, 10, key="comp_l")

    vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
    colors = ["#e74c3c", "#e67e22", "#f1c40f", "#1a9e5c"]
    co2_vals = [calculate_carbon(comp_distance, v, comp_load) for v in vehicles]
    cost_vals = [calculate_fuel_cost(comp_distance, v) for v in vehicles]

    st.markdown('<div class="section-header">CO₂ Emissions by Vehicle</div>', unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(
        x=vehicles, y=co2_vals, marker_color=colors,
        text=[f"{v} kg" for v in co2_vals],
        textposition="outside", textfont=dict(color="white", size=13),
    ))
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        xaxis=dict(showgrid=False, tickfont=dict(color="white", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#2d3348", title="CO₂ Emitted (kg)"),
        margin=dict(t=30, b=20), height=380,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Fuel Cost Comparison (₹)</div>', unsafe_allow_html=True)
    fig4 = go.Figure(go.Bar(
        x=vehicles, y=cost_vals, marker_color=colors,
        text=[f"₹{v}" for v in cost_vals],
        textposition="outside", textfont=dict(color="white", size=13),
    ))
    fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        xaxis=dict(showgrid=False, tickfont=dict(color="white", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#2d3348", title="Fuel Cost (₹)"),
        margin=dict(t=30, b=20), height=380,
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Side-by-Side Summary</div>', unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "Vehicle Type": vehicles,
        "CO₂ Emitted (kg)": co2_vals,
        "Fuel Cost (₹)": cost_vals,
        "CO₂ Saved vs Diesel (kg)": [round(co2_vals[0] - c, 2) for c in co2_vals],
        "Carbon Score": ["⭐" * get_carbon_score(c, comp_distance) for c in co2_vals]
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True), calculate_fuel_cost, calculate_carbon_saved, get_carbon_score
from routes import get_route_legs, get_distance

# Rest of your code...

# Rest of your code starts here...

st.set_page_config(page_title="EcoRoute AI", page_icon="🌱", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: radial-gradient(ellipse at top, #0d1f14 0%, #0f1117 50%, #0a0e1a 100%); }
.block-container { padding-top: 2rem !important; }
.hero-banner {
    background: linear-gradient(135deg, #0d6e3f 0%, #1a9e5c 50%, #0d6e3f 100%);
    border-radius: 16px; padding: 40px; margin-bottom: 30px;
    text-align: center; box-shadow: 0 8px 32px rgba(26,158,92,0.3);
}
.hero-banner h1 { font-size: 2.8rem; font-weight: 700; color: white; margin: 0; }
.hero-banner p { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 8px; }
.section-header {
    font-size: 1.3rem; font-weight: 600; color: #e8eaf0;
    border-left: 4px solid #1a9e5c; padding-left: 12px; margin: 24px 0 16px 0;
}
.insight-box {
    background: linear-gradient(135deg, #0d2b1a, #0f3d24);
    border: 1px solid #1a9e5c; border-radius: 12px; padding: 20px 24px; margin-top: 20px;
}
.insight-box p { color: #7effc0; font-size: 1rem; margin: 0; }
.badge {
    display: inline-block; background: #0d2b1a; color: #1a9e5c;
    border: 1px solid #1a9e5c; border-radius: 20px;
    padding: 4px 14px; font-size: 0.8rem; font-weight: 600; margin: 2px;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #1e2130; padding: 8px; border-radius: 12px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 20px; font-weight: 500; color: #8b95a8; }
.stTabs [aria-selected="true"] { background: #1a9e5c !important; color: white !important; }
div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #1a9e5c !important; font-weight: 700 !important; }
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1a1f2e, #1e2535);
    border: 1px solid #2d3348; border-radius: 12px; padding: 16px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1a9e5c, #0d6e3f); color: white;
    border: none; border-radius: 10px; padding: 14px 28px;
    font-size: 1rem; font-weight: 600; width: 100%;
    box-shadow: 0 4px 15px rgba(26,158,92,0.4);
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🌍 EcoRoute AI")
    st.markdown("---")
    st.markdown("**Platform Stats**")
    st.metric("🚛 Routes Analyzed", "1,284")
    st.metric("💨 CO₂ Saved (tons)", "48.6")
    st.metric("🌳 Trees Equivalent", "2,314")
    st.metric("🏙️ Cities Covered", "24")
    st.markdown("---")
    st.markdown("**Supported Vehicles**")
    st.success("✅ Electric Vehicle")
    st.warning("⚠️ CNG Truck")
    st.error("🔴 Diesel Truck")
    st.markdown("---")
    st.markdown("**SDG Alignment**")
    st.markdown("🎯 SDG 13 — Climate Action")
    st.markdown("🏙️ SDG 11 — Sustainable Cities")
    st.markdown("⚙️ SDG 9 — Industry & Innovation")
    st.markdown("---")
    st.info("💡 Switch to EV to reduce emissions by up to 87%")

# HERO
st.markdown("""
<div class="hero-banner">
    <h1>🌱 EcoRoute AI</h1>
    <p>Sustainable Logistics Route Optimization & Carbon Reduction Platform</p>
    <div style="margin-top:14px">
        <span class="badge">🎯 Climate Action</span>
        <span class="badge">📦 SCM Optimized</span>
        <span class="badge">🌍 SDG 13 Aligned</span>
        <span class="badge">⚡ Real-time Analysis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["🚚  Single Route Analyzer", "📦  Multi-Stop SCM Route", "📊  Vehicle Comparison"])

# ── TAB 1 ──────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Route Input</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        origin = st.text_input("🏭 Origin — Warehouse / Factory", placeholder="e.g. Mumbai")
        stop1 = st.text_input("📍 Delivery Stop 1", placeholder="e.g. Pune")
        stop2 = st.text_input("📍 Delivery Stop 2 (optional)", placeholder="e.g. Nashik")

    with col2:
        vehicle_type = st.selectbox("🚛 Vehicle Type", [
            "Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"
        ])
        load_weight = st.slider("⚖️ Load Weight (tons)", 1, 30, 5)
        priority = st.radio("🎯 Optimization Priority", [
            "Minimize Carbon Emissions", "Balance Carbon + Time", "Minimize Time"
        ])

    st.markdown("")
    if st.button("⚡ Calculate EcoRoute", key="single"):
        dist1 = get_distance(origin, stop1) if origin and stop1 else 200
        dist2 = get_distance(stop1, stop2) if stop2 else 0
        total_distance = dist1 + dist2

        total_co2 = calculate_carbon(total_distance, vehicle_type, load_weight)
        total_cost = calculate_fuel_cost(total_distance, vehicle_type)
        co2_saved = calculate_carbon_saved(total_distance, vehicle_type, load_weight)
        score = get_carbon_score(total_co2, total_distance)
        trees = round(co2_saved / 21, 1)

        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📏 Total Distance", f"{total_distance} km")
        with c2:
            st.metric("💨 CO₂ Emitted", f"{total_co2} kg")
        with c3:
            st.metric("🌱 CO₂ Saved", f"{co2_saved} kg")
        with c4:
            st.metric("💰 Fuel Cost", f"₹{total_cost}")

        # Vehicle comparison chart
        st.markdown('<div class="section-header">Vehicle Carbon Comparison</div>', unsafe_allow_html=True)
        vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
        co2_values = [calculate_carbon(total_distance, v, load_weight) for v in vehicles]
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#1a9e5c"]

        fig = go.Figure(go.Bar(
            x=vehicles, y=co2_values, marker_color=colors,
            text=[f"{v} kg" for v in co2_values],
            textposition="outside", textfont=dict(color="white", size=13),
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            xaxis=dict(showgrid=False, tickfont=dict(size=12)),
            yaxis=dict(showgrid=True, gridcolor="#2d3348", title="CO₂ Emitted (kg)"),
            margin=dict(t=20, b=20), height=380, showlegend=False,
        )
        st.plotly_chart(fig, width="stretch")
        st.plotly_chart(fig, width="stretch")
        # AI Recommendation
        st.markdown('<div class="section-header">🤖 AI Recommendation</div>', unsafe_allow_html=True)
        rec_col1, rec_col2 = st.columns(2)

        all_vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
        all_co2 = {v: calculate_carbon(total_distance, v, load_weight) for v in all_vehicles}
        best_vehicle = min(all_co2, key=all_co2.get)
        best_co2 = all_co2[best_vehicle]

        with rec_col1:
            if vehicle_type == best_vehicle:
                st.success(f"✅ You already chose the best option! **{best_vehicle}** emits the least CO₂ on this route.")
            else:
                potential_saving = round(total_co2 - best_co2, 2)
                st.warning(f"💡 Switching to **{best_vehicle}** would save an additional **{potential_saving} kg CO₂** on this route.")

        with rec_col2:
            carbon_credits = round(co2_saved / 1000, 4)
            credit_value = round(carbon_credits * 1500, 2)
            st.info(f"💰 Carbon Credits Earned: **{carbon_credits} credits**\n\nEstimated Value: **₹{credit_value}**")

        st.markdown(f"""
        <div class="insight-box">
            <p>🌳 By choosing <strong>{vehicle_type}</strong> on this {total_distance} km route,
            you saved <strong>{co2_saved} kg of CO₂</strong> — equivalent to planting
            <strong>{trees} trees</strong>. Carbon Score: {"⭐" * score}</p>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 2 ──────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Supply Chain Route Planner</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        warehouse = st.text_input("🏭 Warehouse (Origin)", placeholder="e.g. Mumbai")
        dest1 = st.text_input("📍 Stop 1 — Distributor", placeholder="e.g. Pune")
        dest2 = st.text_input("📍 Stop 2 — Retailer A", placeholder="e.g. Nashik")
        dest3 = st.text_input("📍 Stop 3 — Retailer B (optional)", placeholder="e.g. Aurangabad")
        dest4 = st.text_input("📍 Stop 4 — Retailer C (optional)", placeholder="e.g. Nagpur")

    with col_b:
        scm_vehicle = st.selectbox("🚛 Fleet Vehicle Type", [
            "Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"
        ], key="scm_v")
        scm_load = st.slider("⚖️ Load Weight (tons)", 1, 30, 10, key="scm_l")
        num_trucks = st.number_input("🚛 Fleet Size", 1, 50, 3)

    st.markdown("")
    if st.button("⚡ Optimize SCM Route", use_container_width=True, key="scm"):
        all_stops = [warehouse, dest1, dest2, dest3, dest4]
        stops = [s.strip().title() for s in all_stops if s.strip()]

        if len(stops) < 2:
            st.error("Please enter at least a warehouse and one delivery stop.")
        else:
            legs = get_route_legs(stops)
            leg_data = []
            total_dist = 0
            total_co2_scm = 0
            total_cost_scm = 0

            for i, leg in enumerate(legs):
                co2 = calculate_carbon(leg["distance_km"], scm_vehicle, scm_load)
                cost = calculate_fuel_cost(leg["distance_km"], scm_vehicle)
                score = get_carbon_score(co2, leg["distance_km"])
                total_dist += leg["distance_km"]
                total_co2_scm += co2
                total_cost_scm += cost
                leg_data.append({
                    "Leg": f"Leg {i+1}",
                    "From": leg["from"],
                    "To": leg["to"],
                    "Distance (km)": leg["distance_km"],
                    "CO₂ Emitted (kg)": co2,
                    "Fuel Cost (₹)": cost,
                    "Carbon Score": "⭐" * score
                })

            df = pd.DataFrame(leg_data)
            st.markdown('<div class="section-header">Route Leg Breakdown</div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

            fig2 = px.bar(
                df, x="Leg", y="CO₂ Emitted (kg)",
                color="CO₂ Emitted (kg)",
                color_continuous_scale=["#1a9e5c", "#f1c40f", "#e74c3c"],
                text="CO₂ Emitted (kg)"
            )
            fig2.update_traces(textposition="outside", textfont=dict(color="white"))
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#2d3348"),
                margin=dict(t=20, b=20), height=320,
                showlegend=False, coloraxis_showscale=False
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Fleet Summary
            st.markdown('<div class="section-header">Fleet Summary</div>', unsafe_allow_html=True)
            fleet_co2 = round(total_co2_scm * num_trucks, 2)
            fleet_cost = round(total_cost_scm * num_trucks, 2)
            fleet_saved = round(calculate_carbon_saved(total_dist, scm_vehicle, scm_load) * num_trucks, 2)
            trees_fleet = round(fleet_saved / 21, 1)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("📏 Total Distance", f"{total_dist} km")
            with m2:
                st.metric("💨 Fleet CO₂", f"{fleet_co2} kg")
            with m3:
                st.metric("🌱 CO₂ Saved", f"{fleet_saved} kg")
            with m4:
                st.metric("🌳 Trees Equivalent", f"{trees_fleet}")

            # Load Consolidation
            st.markdown('<div class="section-header">📦 Load Consolidation Suggestion</div>', unsafe_allow_html=True)
            cons_col1, cons_col2 = st.columns(2)

            with cons_col1:
                if num_trucks > 1:
                    consolidated_trucks = max(1, num_trucks - 1)
                    saved_trips_co2 = round(total_co2_scm * (num_trucks - consolidated_trucks), 2)
                    saved_trips_cost = round(total_cost_scm * (num_trucks - consolidated_trucks), 2)
                    st.success(f"💡 Consolidating **{num_trucks} → {consolidated_trucks} trucks** saves:\n\n"
                               f"**{saved_trips_co2} kg CO₂** and **₹{saved_trips_cost}** in fuel per trip cycle.")
                else:
                    st.info("✅ Already running a single truck — fully consolidated!")

            with cons_col2:
                fleet_credits = round(fleet_saved / 1000, 4)
                fleet_credit_value = round(fleet_credits * 1500, 2)
                st.info(f"💰 Fleet Carbon Credits: **{fleet_credits} credits**\n\nEstimated Value: **₹{fleet_credit_value}**")

            st.markdown(f"""
            <div class="insight-box">
                <p>🚛 Your <strong>{num_trucks}-truck fleet</strong> covers <strong>{total_dist} km</strong>
                across {len(legs)} supply chain legs. Using <strong>{scm_vehicle}</strong>,
                you save <strong>{fleet_saved} kg CO₂</strong> — like planting <strong>{trees_fleet} trees</strong> per trip cycle.</p>
            </div>
            """, unsafe_allow_html=True)

# ── TAB 3 ──────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Compare All Vehicle Types</div>', unsafe_allow_html=True)
    cc1, cc2 = st.columns(2)
    with cc1:
        comp_distance = st.slider("📏 Route Distance (km)", 50, 1000, 300, key="comp_d")
    with cc2:
        comp_load = st.slider("⚖️ Load Weight (tons)", 1, 30, 10, key="comp_l")

    vehicles = ["Diesel Truck (Heavy)", "Diesel Truck (Light)", "CNG Truck", "Electric Vehicle"]
    colors = ["#e74c3c", "#e67e22", "#f1c40f", "#1a9e5c"]
    co2_vals = [calculate_carbon(comp_distance, v, comp_load) for v in vehicles]
    cost_vals = [calculate_fuel_cost(comp_distance, v) for v in vehicles]

    st.markdown('<div class="section-header">CO₂ Emissions by Vehicle</div>', unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(
        x=vehicles, y=co2_vals, marker_color=colors,
        text=[f"{v} kg" for v in co2_vals],
        textposition="outside", textfont=dict(color="white", size=13),
    ))
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        xaxis=dict(showgrid=False, tickfont=dict(color="white", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#2d3348", title="CO₂ Emitted (kg)"),
        margin=dict(t=30, b=20), height=380,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Fuel Cost Comparison (₹)</div>', unsafe_allow_html=True)
    fig4 = go.Figure(go.Bar(
        x=vehicles, y=cost_vals, marker_color=colors,
        text=[f"₹{v}" for v in cost_vals],
        textposition="outside", textfont=dict(color="white", size=13),
    ))
    fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        xaxis=dict(showgrid=False, tickfont=dict(color="white", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#2d3348", title="Fuel Cost (₹)"),
        margin=dict(t=30, b=20), height=380,
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Side-by-Side Summary</div>', unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "Vehicle Type": vehicles,
        "CO₂ Emitted (kg)": co2_vals,
        "Fuel Cost (₹)": cost_vals,
        "CO₂ Saved vs Diesel (kg)": [round(co2_vals[0] - c, 2) for c in co2_vals],
        "Carbon Score": ["⭐" * get_carbon_score(c, comp_distance) for c in co2_vals]
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
