import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==========================================
# Database Setup (දත්ත ගබඩාව සැකසීම)
# ==========================================
def init_db():
    conn = sqlite3.connect('factory_data.db')
    c = conn.cursor()
    # Create table for daily wages history
    c.execute('''CREATE TABLE IF NOT EXISTS daily_wages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  task_name TEXT,
                  category TEXT,
                  qty INTEGER,
                  rate REAL,
                  total REAL)''')
    conn.commit()
    conn.close()

# Initialize DB
init_db()

# ==========================================
# Page configurations & CSS
# ==========================================
st.set_page_config(page_title="Factory Management System", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title { font-size: 26px !important; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 14px !important; color: #6B7280; margin-bottom: 20px; }
    .stDataFrame { border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🏭 Production & Wage Management System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>කර්මාන්තශාලා නිෂ්පාදන, දෛනික වැටුප් සහ වියදම් කළමනාකරණ පද්ධතිය</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# Initialize Session States (මූලික දත්ත)
# ==========================================
if 'tasks' not in st.session_state:
    raw_tasks = [
        ('මල් කනු හැදීම', 'Making (හැදීම)'), ('මල් කනු ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('මල් කනු වලට කැට ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), ('මල් කනු රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('මල් කනු පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල් කනු හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල් කනු රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල් කනු පාට කිරීම', 'Painting (පාට කිරීම)'),
        ('මල් කනු පාදන් හැදීම', 'Making (හැදීම)'), ('මල් කනු පාදන් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('මල් කනු පාදන් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල් කනු පාදන් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල් කනු පාදන් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල් කනු පාදන් පාට කිරීම', 'Painting (පාට කිරීම)'),
        ('ටයිල් ප්ලේට් හැදීම', 'Making (හැදීම)'), ('ටයිල් ප්ලේට් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('ටයිල් ප්ලේට් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල පොඩි බෝල් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල පොඩි බෝල් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල්වල පොඩි බෝල් ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('වතුර මල්වල පොඩි බෝල් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල ලොකු බෝල් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල ලොකු බෝල් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල්වල ලොකු බෝල් ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('වතුර මල්වල ලොකු බෝල් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල ලොකු කැට හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල ලොකු කැට ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), ('වතුර මල්වල ලොකු කැට වලට මල් ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), 
        ('වතුර මල්වල ලොකු කැට පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල පොඩි කැට හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල පොඩි කැට ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), ('වතුර මල්වල පොඩි කැට වලට මල් ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), 
        ('වතුර මල්වල පොඩි කැට පාට කිරීම', 'Painting (පාට කිරීම)'), ('"බුදුසරනයි" කැට හැදීම', 'Making (හැදීම)'), 
        ('"මල්" කැට හැදීම', 'Making (හැදීම)'), ('"කරඩු ඇතා" කැට හැදීම', 'Making (හැදීම)'), ('"දර්ම චක්‍ර" කැට හැදීම', 'Making (හැදීම)')
    ]
    st.session_state.tasks = pd.DataFrame({
        'Task Name (වැඩ කොටස)': [t[0] for t in raw_tasks],
        'Category (කාණ්ඩය)': [t[1] for t in raw_tasks],
        'Piece Rate / ගෙවන මුදල (Rs)': [150.0] * len(raw_tasks)
    })

if 'materials' not in st.session_state:
    st.session_state.materials = pd.DataFrame({
        'Material Name (අමුද්‍රව්‍ය)': ['Cement (සිමෙන්ති) - Bag', 'Steel Rods (කම්බි) - 1kg', 'Sand (වැලි) - Cube', 'Paint (තීන්ත) - 1L'],
        'Unit Price / මිල (Rs)': [2400.0, 320.0, 14000.0, 1800.0]
    })

if 'products' not in st.session_state:
    st.session_state.products = [
        {'name': 'මල් කනුව (Style 1)', 'price': 5000.0, 'image': None},
        {'name': 'වතුර මල් කනුව (Style 1)', 'price': 8500.0, 'image': None}
    ]

if 'daily_cart' not in st.session_state:
    st.session_state.daily_cart = []

# --- System Alerts ---
if 'price_confirmed' not in st.session_state:
    st.session_state.price_confirmed = False

if not st.session_state.price_confirmed:
    st.warning("⚠️ කරුණාකර අමුද්‍රව්‍ය මිල ගණන් යාවත්කාලීන දැයි පරීක්ෂා කරන්න. (Please verify material prices in Control Panel)")
    if st.button("මිල ගණන් නිවැරදියි (Confirm)"):
        st.session_state.price_confirmed = True
        st.rerun()

# ==========================================
# Navigation Tabs (දැන් Tabs 6ක් ඇත)
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🛍️ භාණ්ඩ හා මාදිලි", 
    "📋 කුලී ලේඛනය", 
    "💰 දෛනික වැටුප", 
    "🗄️ දත්ත ඉතිහාසය", 
    "📊 වියදම්/ලාභ", 
    "⚙️ Control Panel"
])

# ==========================================
# TAB 1: Products & Showcase
# ==========================================
with tab1:
    st.markdown("### 🛍️ Product Styles & Selling Prices")
    if len(st.session_state.products) == 0:
        st.info("දැනට කිසිදු නිෂ්පාදනයක් ඇතුලත් කර නැත. Control Panel එකෙන් ඇතුලත් කරන්න.")
    else:
        cols = st.columns(3)
        for index, prod in enumerate(st.session_state.products):
            with cols[index % 3]:
                st.markdown(f"##### 📦 {prod['name']}")
                if prod['image'] is not None:
                    st.image(prod['image'], use_container_width=True)
                else:
                    st.warning("No image uploaded")
                st.write(f"**Selling Price:** Rs. {prod['price']:,}")
                st.markdown("---")

# ==========================================
# TAB 2: Piece Rates List
# ==========================================
with tab2:
    st.markdown("### 📋 Work Category & Piece Rates")
    categories = ['All (සියල්ල)'] + list(st.session_state.tasks['Category (කාණ්ඩය)'].unique())
    selected_cat = st.selectbox("කාණ්ඩය අනුව පෙරන්න (Filter by Category):", categories)
    
    if selected_cat == 'All (සියල්ල)':
        display_df = st.session_state.tasks
    else:
        display_df = st.session_state.tasks[st.session_state.tasks['Category (කාණ්ඩය)'] == selected_cat]
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ==========================================
# TAB 3: Daily Wage Calculator
# ==========================================
with tab3:
    st.markdown("### 💰 Daily Wage Calculator")
    st.write("සිදුකළ වැඩ කොටස් එකින් එක තෝරා 'Add to List' බොත්තම ඔබන්න.")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        cat_to_filter = st.selectbox("1. වැඩ වර්ගය (Category):", st.session_state.tasks['Category (කාණ්ඩය)'].unique())
    with col2:
        filtered_tasks_options = st.session_state.tasks[st.session_state.tasks['Category (කාණ්ඩය)'] == cat_to_filter]['Task Name (වැඩ කොටස)'].tolist()
        selected_task = st.selectbox("2. වැඩ කොටස (Task):", filtered_tasks_options)
    with col3:
        task_qty = st.number_input("3. ප්‍රමාණය (Qty):", min_value=1, value=1)
        
    if st.button("➕ Add to List (ලැයිස්තුවට එකතු කරන්න)"):
        task_rate = st.session_state.tasks[st.session_state.tasks['Task Name (වැඩ කොටස)'] == selected_task].iloc[0]['Piece Rate / ගෙවන මුදල (Rs)']
        st.session_state.daily_cart.append({
            "වැඩ කොටස (Task)": selected_task,
            "කාණ්ඩය (Category)": cat_to_filter,
            "ප්‍රමාණය (Qty)": task_qty,
            "ඒකක මිල (Rate)": task_rate,
            "එකතුව (Total Rs)": task_rate * task_qty
        })
        st.success(f"{selected_task} ({task_qty}) ලැයිස්තුවට එකතු කළා!")
        st.rerun()

    st.markdown("---")
    
    if len(st.session_state.daily_cart) > 0:
        st.markdown("#### 📝 අද දින සිදුකළ වැඩ ලැයිස්තුව")
        cart_df = pd.DataFrame(st.session_state.daily_cart)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        grand_total = cart_df["එකතුව (Total Rs)"].sum()
        st.markdown(f"### 💵 මුළු දෛනික වැටුප: Rs. {grand_total:,}")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 Save to History (ඉතිහාසයට සේව් කරන්න)", type="primary"):
                conn = sqlite3.connect('factory_data.db')
                c = conn.cursor()
                today = datetime.now().strftime("%Y-%m-%d")
                for item in st.session_state.daily_cart:
                    c.execute("INSERT INTO daily_wages (date, task_name, category, qty, rate, total) VALUES (?, ?, ?, ?, ?, ?)",
                              (today, item['වැඩ කොටස (Task)'], item['කාණ්ඩය (Category)'], item['ප්‍රමාණය (Qty)'], item['ඒකක මිල (Rate)'], item['එකතුව (Total Rs)']))
                conn.commit()
                conn.close()
                st.session_state.daily_cart = []
                st.success("දත්ත සාර්ථකව History එකට සේව් කරන ලදී!")
                st.rerun()
                
        with col_btn2:
            if st.button("🗑️ Clear List (ලැයිස්තුව මකන්න)"):
                st.session_state.daily_cart = []
                st.rerun()
    else:
        st.info("දැනට කිසිදු වැඩක් ලැයිස්තුවට එකතු කර නැත.")

# ==========================================
# TAB 4: History View (අලුත් Tab එක)
# ==========================================
with tab4:
    st.markdown("### 🗄️ Daily Work History (දෛනික වැඩ ඉතිහාසය)")
    st.write("පෙර දිනවල සේව් කරපු දත්ත මෙතනින් බලාගන්න පුළුවන්.")
    
    selected_date = st.date_input("දවස තෝරන්න (Select Date):", datetime.now())
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    
    conn = sqlite3.connect('factory_data.db')
    query = f"SELECT task_name AS 'වැඩ කොටස', category AS 'කාණ්ඩය', qty AS 'ප්‍රමාණය', rate AS 'ඒකක මිල', total AS 'එකතුව (Rs)' FROM daily_wages WHERE date = '{selected_date_str}'"
    history_df = pd.read_sql_query(query, conn)
    conn.close()
    
    if len(history_df) > 0:
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        total_history = history_df['එකතුව (Rs)'].sum()
        st.markdown(f"#### 📅 {selected_date_str} දින මුළු වැටුප: Rs. {total_history:,}")
    else:
        st.info(f"{selected_date_str} දිනට අදාල දත්ත කිසිවක් Database එකේ නොමැත.")

# ==========================================
# TAB 5: Cost & Profit Summary (Smart Calculation)
# ==========================================
with tab5:
    st.markdown("### 📊 Production Cost & Profit Calculation")
    if len(st.session_state.products) == 0:
        st.warning("කරුණාකර ප්‍රථමයෙන් භාණ්ඩයක් ඇතුලත් කරන්න.")
    else:
        product_names = [p['name'] for p in st.session_state.products]
        selected_product_name = st.selectbox("නිෂ්පාදිත භාණ්ඩය තෝරන්න (Select Product):", product_names)
        
        prod_obj = next(p for p in st.session_state.products if p['name'] == selected_product_name)
        selling_price = prod_obj['price']
        st.write(f"**Selling Price (විකුණුම් මිල):** Rs. {selling_price:,}")
        
        c1, c2 = st.columns(2)
        
        # --- Labor Cost Section ---
        with c1:
            st.markdown("##### 🛠️ 1. Labor Costs (වැඩ කුලී)")
            calc_method = st.radio("ගණනය කරන ආකාරය තෝරන්න:", ["📝 අතින් ඇතුලත් කිරීම", "🗄️ ඉතිහාසයෙන් ගැනීම (History)"], horizontal=True)
            
            total_labor_cost = 0.0
            
            if calc_method == "📝 අතින් ඇතුලත් කිරීම":
                cost_tasks = st.multiselect("අදාළ වැඩ කොටස් තෝරන්න:", st.session_state.tasks['Task Name (වැඩ කොටස)'])
                for task in cost_tasks:
                    task_price = st.session_state.tasks[st.session_state.tasks['Task Name (වැඩ කොටස)'] == task].iloc[0]['Piece Rate / ගෙවන මුදල (Rs)']
                    qty = st.number_input(f"කෑලි ගණන ({task})", min_value=1, value=1, key=f"cost_{task}")
                    total_labor_cost += (task_price * qty)
            else:
                hist_date = st.date_input("වියදම් බැලීමට අදාළ දවස තෝරන්න:", datetime.now(), key="hist_date")
                conn = sqlite3.connect('factory_data.db')
                hist_total = pd.read_sql_query(f"SELECT SUM(total) as sum_total FROM daily_wages WHERE date = '{hist_date.strftime('%Y-%m-%d')}'", conn).iloc[0]['sum_total']
                conn.close()
                total_labor_cost = float(hist_total) if pd.notna(hist_total) else 0.0
                st.info(f"👉 තෝරාගත් දිනට මුළු වැඩ කුලිය: Rs. {total_labor_cost:,}")
                
        # --- Material Cost Section ---
        with c2:
            st.markdown("##### 🧱 2. Material Costs (අමුද්‍රව්‍ය)")
            selected_materials = st.multiselect("භාවිතා කල අමුද්‍රව්‍ය තෝරන්න:", st.session_state.materials['Material Name (අමුද්‍රව්‍ය)'].tolist())
            total_material_cost = 0
            for mat in selected_materials:
                mat_price = st.session_state.materials[st.session_state.materials['Material Name (අමුද්‍රව්‍ය)'] == mat].iloc[0]['Unit Price / මිල (Rs)']
                mat_qty = st.number_input(f"ප්‍රමාණය ({mat})", min_value=0.0, value=1.0, step=0.1, key=f"mat_{mat}")
                total_material_cost += (mat_price * mat_qty)
                
        total_production_cost = total_labor_cost + total_material_cost
        profit = selling_price - total_production_cost
        
        st.markdown("---")
        st.table(pd.DataFrame({
            "විස්තරය (Description)": ["විකුණුම් මිල", "මුළු වැඩ කුලිය", "මුළු අමුද්‍රව්‍ය වියදම", "සම්පූර්ණ නිෂ්පාදන වියදම"],
            "මුදල (Rs)": [selling_price, total_labor_cost, total_material_cost, total_production_cost]
        }))
        
        if profit >= 0:
            st.success(f"📈 Net Profit (ශුද්ධ ලාභය): Rs. {profit:,}")
        else:
            st.error(f"📉 Net Loss (අලාභය): Rs. {profit:,}")

# ==========================================
# TAB 6: Control Panel
# ==========================================
with tab6:
    st.markdown("### ⚙️ Factory Data Control Panel")
    
    st.markdown("#### 📸 Manage Product Styles & Photos")
    if len(st.session_state.products) > 0:
        for i, p in enumerate(st.session_state.products):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1: st.write(f"**{p['name']}** - Rs. {p['price']:,}")
            with c2: st.caption("✅ Photo Loaded" if p['image'] is not None else "❌ No Photo")
            with c3:
                if st.button("Delete", key=f"del_prod_{i}"):
                    st.session_state.products.pop(i)
                    st.rerun()
                    
    with st.form("add_product_form", clear_on_submit=True):
        st.write("**➕ Add New Style / Product Model**")
        new_name = st.text_input("Product Name (නිෂ්පාදනයේ නම):")
        new_price = st.number_input("Selling Price (විකුණුම් මිල රු.):", min_value=0.0, value=1000.0)
        uploaded_file = st.file_uploader("Upload Photo from Gallery:", type=["jpg", "png", "jpeg"])
        
        if st.form_submit_button("Save New Product Style"):
            if new_name:
                st.session_state.products.append({
                    'name': new_name,
                    'price': new_price,
                    'image': uploaded_file.read() if uploaded_file else None
                })
                st.success("සාර්ථකව එකතු කරන ලදී!")
                st.rerun()
            else:
                st.error("නමක් ඇතුලත් කරන්න.")

    st.markdown("---")

    st.markdown("#### 📋 Update Piece Rates (කාණ්ඩ අනුව මිල ගණන්)")
    unique_categories = st.session_state.tasks['Category (කාණ්ඩය)'].unique()
    edited_task_dfs = []
    
    with st.form("piece_rates_form"):
        for cat in unique_categories:
            st.markdown(f"**🔹 {cat}**")
            df_cat = st.session_state.tasks[st.session_state.tasks['Category (කාණ්ඩය)'] == cat].copy()
            edited_df_cat = st.data_editor(df_cat, num_rows="dynamic", use_container_width=True, key=f"editor_{cat}")
            edited_df_cat['Category (කාණ්ඩය)'] = cat 
            edited_task_dfs.append(edited_df_cat)
            
        if st.form_submit_button("Save All Piece Rates (සේව් කරන්න)"):
            st.session_state.tasks = pd.concat(edited_task_dfs, ignore_index=True)
            st.success("වැඩ කුලී මිල ගණන් සාර්ථකව යාවත්කාලීන කරන ලදී!")
            st.rerun()

    st.markdown("---")

    st.markdown("#### 🧱 Update Material Prices (අමුද්‍රව්‍ය මිල ගණන්)")
    edited_materials = st.data_editor(st.session_state.materials, num_rows="dynamic", use_container_width=True)
    if st.button("Save Material Prices (සේව් කරන්න)"):
        st.session_state.materials = edited_materials
        st.session_state.price_confirmed = True 
        st.success("අමුද්‍රව්‍ය මිල ගණන් සාර්ථකව යාවත්කාලීන කරන ලදී!")
        st.rerun()
