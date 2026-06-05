import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==========================================
# Database Setup
# ==========================================
def init_db():
    conn = sqlite3.connect('factory_data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  phone TEXT)''')
                  
    c.execute("PRAGMA table_info(employees)")
    columns_emp = [col[1] for col in c.fetchall()]
    if 'photo' not in columns_emp:
        c.execute("ALTER TABLE employees ADD COLUMN photo BLOB")
                  
    c.execute('''CREATE TABLE IF NOT EXISTS daily_wages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  task_name TEXT,
                  category TEXT,
                  qty INTEGER,
                  rate REAL,
                  total REAL)''')
                  
    c.execute("PRAGMA table_info(daily_wages)")
    columns_wage = [col[1] for col in c.fetchall()]
    if 'employee_name' not in columns_wage:
        c.execute("ALTER TABLE daily_wages ADD COLUMN employee_name TEXT")

    conn.commit()
    conn.close()

def load_employees():
    conn = sqlite3.connect('factory_data.db')
    df = pd.read_sql_query("SELECT name FROM employees", conn)
    conn.close()
    return df['name'].tolist()

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
st.markdown("<div class='sub-title'>කර්මාන්තශාලා නිෂ්පාදන, සේවක කළමනාකරණය සහ වියදම් පද්ධතිය</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# Initialize Session States (Full 37 Tasks List)
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
        {'name': 'මල් කනුව (Style 1)', 'price': 5000.0, 'image': None}
    ]

if 'daily_cart' not in st.session_state:
    st.session_state.daily_cart = []

if 'price_confirmed' not in st.session_state:
    st.session_state.price_confirmed = False

if not st.session_state.price_confirmed:
    st.warning("⚠️ කරුණාකර Control Panel වෙත ගොස් අමුද්‍රව්‍ය මිල ගණන් නිවැරදි දැයි තහවුරු කරන්න.")
    if st.button("මිල ගණන් නිවැරදියි (Confirm)"):
        st.session_state.price_confirmed = True
        st.rerun()

# ==========================================
# Navigation Tabs
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🛍️ භාණ්ඩ", 
    "📋 කුලී", 
    "👥 සේවකයන්",
    "💰 දෛනික වැටුප", 
    "🧾 පඩිපත",
    "🗄️ ඉතිහාසය", 
    "📊 වියදම්/ලාභ", 
    "⚙️ සැකසුම්"
])

# ==========================================
# TAB 1: Products
# ==========================================
with tab1:
    st.markdown("### 🛍️ Product Styles & Selling Prices")
    if len(st.session_state.products) == 0:
        st.info("දැනට කිසිදු නිෂ්පාදනයක් නැත.")
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
# TAB 2: Piece Rates
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
# TAB 3: Employee Management
# ==========================================
with tab3:
    st.markdown("### 👥 සේවක කළමනාකරණය (Employee Profiles)")
    
    # --- Add New Employee ---
    with st.expander("➕ අලුත් සේවකයෙක් ඇතුලත් කරන්න", expanded=True):
        st.info("💡 ගැලරියෙන් පින්තූරය තෝරා මද වේලාවක් රැඳී සිටින්න.")
        
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            emp_name = st.text_input("සේවකයාගේ නම (Name):", key="new_emp_name")
        with col_n2:
            emp_phone = st.text_input("දුරකථන අංකය (Phone):", key="new_emp_phone")
            
        emp_photo_file = st.file_uploader("පින්තූරය තෝරන්න (Gallery):", type=["jpg", "png", "jpeg"], key="new_emp_file")
        
        if emp_photo_file is not None:
            st.success("✅ පින්තූරය සාර්ථකව ලෝඩ් විය!")
            st.image(emp_photo_file, width=150, caption="Preview")
            
        if st.button("සේවකයා සේව් කරන්න (Save Employee)", type="primary"):
            if emp_name:
                # Get exact image bytes without compression to keep quality high
                photo_bytes = emp_photo_file.getvalue() if emp_photo_file else None
                try:
                    conn = sqlite3.connect('factory_data.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO employees (name, phone, photo) VALUES (?, ?, ?)", (emp_name, emp_phone, photo_bytes))
                    conn.commit()
                    conn.close()
                    # Clear uploader state properly
                    if "new_emp_file" in st.session_state:
                        del st.session_state["new_emp_file"]
                    st.success(f"{emp_name} සාර්ථකව ඇතුලත් කරන ලදී!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("මෙම නම ඇති සේවකයෙක් දැනටමත් සිටී. වෙනත් නමක් ලබා දෙන්න.")
            else:
                st.error("කරුණාකර සේවකයාගේ නම ඇතුලත් කරන්න.")

    st.markdown("---")
    
    # --- Edit Existing Employee ---
    st.markdown("#### ✏️ සේවක විස්තර වෙනස් කිරීම (Edit Profiles)")
    conn = sqlite3.connect('factory_data.db')
    emps_df = pd.read_sql_query("SELECT id, name, phone FROM employees", conn)
    conn.close()
    
    if not emps_df.empty:
        edit_emp_name = st.selectbox("වෙනස් කළ යුතු සේවකයා තෝරන්න:", ["තෝරන්න (Select)"] + emps_df['name'].tolist(), key="edit_emp_sel")
        
        if edit_emp_name != "තෝරන්න (Select)":
            conn = sqlite3.connect('factory_data.db')
            c = conn.cursor()
            c.execute("SELECT id, name, phone, photo FROM employees WHERE name=?", (edit_emp_name,))
            emp_data = c.fetchone()
            conn.close()
            
            emp_id, curr_name, curr_phone, curr_photo = emp_data
            
            st.write(f"**{curr_name} ගේ විස්තර යාවත්කාලීන කරන්න**")
            upd_name = st.text_input("අලුත් නම (New Name):", value=curr_name)
            upd_phone = st.text_input("අලුත් දුරකථන අංකය (New Phone):", value=curr_phone if curr_phone else "")
            
            if curr_photo:
                st.write("**දැනට ඇති පින්තූරය:**")
                st.image(curr_photo, width=100)
            else:
                st.info("දැනට පින්තූරයක් නැත.")
                
            upd_photo_file = st.file_uploader("අලුත් පින්තූරයක් දානවා නම් තෝරන්න:", type=["jpg", "png", "jpeg"], key=f"upd_file_{emp_id}")
                
            if upd_photo_file is not None:
                st.success("✅ අලුත් පින්තූරය සාර්ථකව ලෝඩ් විය!")
                st.image(upd_photo_file, width=150, caption="New Preview")
        
            if st.button("Update (වෙනස්කම් සේව් කරන්න)", key="update_emp_btn", type="primary"):
                # Get exact image bytes
                new_photo_bytes = upd_photo_file.getvalue() if upd_photo_file else curr_photo
                try:
                    conn = sqlite3.connect('factory_data.db')
                    c = conn.cursor()
                    c.execute("UPDATE employees SET name=?, phone=?, photo=? WHERE id=?", (upd_name, upd_phone, new_photo_bytes, emp_id))
                    
                    if upd_name != curr_name:
                        c.execute("UPDATE daily_wages SET employee_name=? WHERE employee_name=?", (upd_name, curr_name))
                    conn.commit()
                    conn.close()
                    # Clear uploader state
                    if f"upd_file_{emp_id}" in st.session_state:
                        del st.session_state[f"upd_file_{emp_id}"]
                    st.success("සාර්ථකව වෙනස් කරන ලදී!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("මෙම නම ඇති වෙනත් සේවකයෙක් දැනටමත් සිටී.")
    else:
        st.info("වෙනස් කිරීමට සේවකයන් කිසිවෙකු නැත.")

    st.markdown("---")
    
    # --- View Employees List (Small Photo 70px) ---
    st.markdown("#### 🧑‍🤝‍🧑 දැනට සිටින සේවක ලැයිස්තුව")
    conn = sqlite3.connect('factory_data.db')
    c = conn.cursor()
    c.execute("SELECT id, name, phone, photo FROM employees")
    emps = c.fetchall()
    conn.close()
    
    if emps:
        for emp in emps:
            c1, c2, c3 = st.columns([1, 4, 1])
            with c1:
                if emp[3]: 
                    st.image(emp[3], width=70) # කුඩා පින්තූරය
                else:
                    st.write("🖼️ නැත")
            with c2:
                st.markdown(f"**{emp[1]}**")
                st.caption(f"📞 {emp[2]}")
            with c3:
                if st.button("🗑️", key=f"del_emp_{emp[0]}"):
                    conn = sqlite3.connect('factory_data.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM employees WHERE id = ?", (emp[0],))
                    conn.commit()
                    conn.close()
                    st.rerun()
            st.markdown("---")
    else:
        st.info("දැනට කිසිදු සේවකයෙක් ඇතුලත් කර නොමැත.")

# ==========================================
# TAB 4: Daily Wage Calculator
# ==========================================
with tab4:
    st.markdown("### 💰 Daily Wage Calculator")
    
    employees_list = load_employees()
    if not employees_list:
        st.warning("⚠️ කරුණාකර ප්‍රථමයෙන් '👥 සේවකයන්' අංශයෙන් සේවකයන් ඇතුලත් කරන්න.")
    else:
        selected_emp_wage = st.selectbox("👷 වැඩ කළ සේවකයා තෝරන්න:", employees_list)
        st.markdown("---")
        
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
                "සේවකයා": selected_emp_wage,
                "වැඩ කොටස": selected_task,
                "කාණ්ඩය": cat_to_filter,
                "ප්‍රමාණය": task_qty,
                "ඒකක මිල": task_rate,
                "එකතුව": task_rate * task_qty
            })
            st.success(f"{selected_task} ({task_qty}) ලැයිස්තුවට එකතු කළා!")
            st.rerun()

        st.markdown("---")
        
        # --- Clean grouped display for Cart ---
        if len(st.session_state.daily_cart) > 0:
            st.markdown("#### 📝 අද දින සිදුකළ වැඩ ලැයිස්තුව")
            cart_df = pd.DataFrame(st.session_state.daily_cart)
            
            unique_cart_emps = cart_df['සේවකයා'].unique()
            for emp in unique_cart_emps:
                st.markdown(f"**👷 {emp} ගේ වැඩ:**")
                emp_cart = cart_df[cart_df['සේවකයා'] == emp].drop(columns=['සේවකයා'])
                st.dataframe(emp_cart, use_container_width=True, hide_index=True)
            
            grand_total = cart_df["එකතුව"].sum()
            st.markdown(f"### 💵 මුළු දෛනික වැටුප: Rs. {grand_total:,}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💾 Save to History (ඉතිහාසයට සේව් කරන්න)", type="primary"):
                    conn = sqlite3.connect('factory_data.db')
                    c = conn.cursor()
                    today = datetime.now().strftime("%Y-%m-%d")
                    for item in st.session_state.daily_cart:
                        c.execute("INSERT INTO daily_wages (date, employee_name, task_name, category, qty, rate, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (today, item['සේවකයා'], item['වැඩ කොටස'], item['කාණ්ඩය'], item['ප්‍රමාණය'], item['ඒකක මිල'], item['එකතුව']))
                    conn.commit()
                    conn.close()
                    st.session_state.daily_cart = []
                    st.success("දත්ත සාර්ථකව History එකට සේව් කරන ලදී!")
                    st.rerun()
                    
            with col_btn2:
                if st.button("🗑️ Clear List (ලැයිස්තුව මකන්න)"):
                    st.session_state.daily_cart = []
                    st.rerun()

# ==========================================
# TAB 5: Monthly Payslip
# ==========================================
with tab5:
    st.markdown("### 🧾 මාසික පඩිපත (Monthly Payslip)")
    employees_list = load_employees()
    if not employees_list:
        st.warning("⚠️ කරුණාකර ප්‍රථමයෙන් සේවකයන් ඇතුලත් කරන්න.")
    else:
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            selected_emp_slip = st.selectbox("සේවකයා තෝරන්න:", employees_list, key="slip_emp")
        with col_p2:
            slip_month = st.selectbox("මාසය:", ["01 - ජනවාරි (Jan)", "02 - පෙබරවාරි (Feb)", "03 - මාර්තු (Mar)", "04 - අප්‍රේල් (Apr)", "05 - මැයි (May)", "06 - ජූනි (Jun)", "07 - ජූලි (Jul)", "08 - අගෝස්තු (Aug)", "09 - සැප්තැම්බර් (Sep)", "10 - ඔක්තෝබර් (Oct)", "11 - නොවැම්බර් (Nov)", "12 - දෙසැම්බර් (Dec)"])
        with col_p3:
            slip_year = st.selectbox("අවුරුද්ද:", [2024, 2025, 2026, 2027], index=2)

        month_num = slip_month.split(" - ")[0]
        target_prefix = f"{slip_year}-{month_num}"

        if st.button("📄 පඩිපත සාදන්න (Generate Payslip)", type="primary"):
            conn = sqlite3.connect('factory_data.db')
            query = f"SELECT date AS 'දිනය', task_name AS 'වැඩ කොටස', qty AS 'ප්‍රමාණය', rate AS 'ඒකක මිල (Rs)', total AS 'එකතුව (Rs)' FROM daily_wages WHERE employee_name = '{selected_emp_slip}' AND date LIKE '{target_prefix}%'"
            slip_df = pd.read_sql_query(query, conn)
            conn.close()

            if len(slip_df) > 0:
                st.markdown("---")
                st.markdown(f"## 🏭 මාසික පඩිපත - {slip_month.split(' - ')[1]} {slip_year}")
                st.markdown(f"**සේවකයාගේ නම:** {selected_emp_slip}")
                st.dataframe(slip_df, use_container_width=True, hide_index=True)

                total_salary = slip_df['එකතුව (Rs)'].sum()
                st.success(f"### 💵 ගෙවිය යුතු මුළු මාසික වැටුප: Rs. {total_salary:,}")
                st.info("💡 Print කිරීමට: Ctl + P (හෝ බ්‍රව්සරයේ තිත් 3 ඔබා Print මෙනුව) භාවිතා කරන්න.")
            else:
                st.warning("මෙම මාසය සඳහා අදාළ සේවකයාට දත්ත කිසිවක් නොමැත.")

# ==========================================
# TAB 6: History View
# ==========================================
with tab6:
    st.markdown("### 🗄️ Daily Work History (දෛනික වැඩ ඉතිහාසය)")
    
    col_hist1, col_hist2 = st.columns(2)
    with col_hist1:
        selected_date = st.date_input("දවස තෝරන්න (Select Date):", datetime.now())
        selected_date_str = selected_date.strftime("%Y-%m-%d")
    with col_hist2:
        all_emps = ["All (සියල්ල)"] + load_employees()
        filter_emp = st.selectbox("සේවකයා අනුව පෙරන්න:", all_emps)
    
    conn = sqlite3.connect('factory_data.db')
    if filter_emp == "All (සියල්ල)":
        query = f"SELECT id AS 'ID', employee_name AS 'සේවකයා', task_name AS 'වැඩ කොටස', category AS 'කාණ්ඩය', qty AS 'ප්‍රමාණය', rate AS 'ඒකක මිල', total AS 'එකතුව (Rs)' FROM daily_wages WHERE date = '{selected_date_str}'"
    else:
        query = f"SELECT id AS 'ID', employee_name AS 'සේවකයා', task_name AS 'වැඩ කොටස', category AS 'කාණ්ඩය', qty AS 'ප්‍රමාණය', rate AS 'ඒකක මිල', total AS 'එකතුව (Rs)' FROM daily_wages WHERE date = '{selected_date_str}' AND employee_name = '{filter_emp}'"
        
    history_df = pd.read_sql_query(query, conn)
    conn.close()
    
    if len(history_df) > 0:
        unique_emps = history_df['සේවකයා'].unique()
        
        for emp in unique_emps:
            emp_df = history_df[history_df['සේවකයා'] == emp]
            st.markdown(f"#### 👷 සේවකයා: {emp}")
            
            display_df = emp_df.drop(columns=['සේවකයා'])
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            emp_total = emp_df['එකතුව (Rs)'].sum()
            st.markdown(f"**{emp} ගේ දෛනික වැටුප: Rs. {emp_total:,}**")
            st.markdown("---")
            
        grand_total = history_df['එකතුව (Rs)'].sum()
        if filter_emp == "All (සියල්ල)":
            st.success(f"### 💵 {selected_date_str} දින මුළු වැටුප (සියලුම සේවක): Rs. {grand_total:,}")
        else:
            st.success(f"### 💵 {filter_emp} සඳහා මුළු වැටුප: Rs. {grand_total:,}")
            
        st.markdown("#### 🗑️ වැරදි වාර්තා මකා දැමීම (Delete Record)")
        col_del1, col_del2 = st.columns([2, 1])
        with col_del1:
            del_id = st.number_input("මකන්න අවශ්‍ය වාර්තාවේ ID අංකය (ඉහත වගුවෙන් බලන්න):", min_value=0, step=1)
        with col_del2:
            st.write("") 
            st.write("") 
            if st.button("🗑️ වාර්තාව මකන්න (Delete)"):
                if del_id > 0:
                    conn = sqlite3.connect('factory_data.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM daily_wages WHERE id = ?", (del_id,))
                    conn.commit()
                    conn.close()
                    st.success("වාර්තාව සාර්ථකව මකා දමන ලදී!")
                    st.rerun()
                else:
                    st.error("කරුණාකර නිවැරදි ID අංකයක් ලබා දෙන්න.")
    else:
        st.info("මෙම දිනට අදාල දත්ත කිසිවක් නොමැත.")

# ==========================================
# TAB 7: Cost & Profit Summary
# ==========================================
with tab7:
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
# TAB 8: Control Panel
# ==========================================
with tab8:
    st.markdown("### ⚙️ Factory Data Control Panel")
    
    # --- Manage Products ---
    st.markdown("#### 📸 භාණ්ඩ හා මාදිලි වෙනස් කිරීම (Manage Products)")
    if len(st.session_state.products) > 0:
        for i, p in enumerate(st.session_state.products):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1: st.write(f"**{p['name']}** - Rs. {p['price']:,}")
            with c2: st.caption("✅ Photo Loaded" if p['image'] is not None else "❌ No Photo")
            with c3:
                if st.button("Delete", key=f"del_prod_{i}"):
                    st.session_state.products.pop(i)
                    st.rerun()
                    
    with st.expander("➕ අලුත් භාණ්ඩයක් ඇතුලත් කරන්න"):
        new_prod_name = st.text_input("භාණ්ඩයේ නම:")
        new_prod_price = st.number_input("මිල (Rs):", min_value=0.0, value=1000.0)
        
        new_prod_photo_file = st.file_uploader("පින්තූරය තෝරන්න (Gallery):", type=["jpg", "png", "jpeg"], key="prod_up")
            
        if new_prod_photo_file is not None:
            st.success("✅ පින්තූරය සාර්ථකව ලෝඩ් විය!")
            st.image(new_prod_photo_file, width=150)
            
        if st.button("Save Product", type="primary"):
            if new_prod_name:
                prod_bytes = new_prod_photo_file.getvalue() if new_prod_photo_file else None
                st.session_state.products.append({
                    'name': new_prod_name,
                    'price': new_prod_price,
                    'image': prod_bytes
                })
                if "prod_up" in st.session_state:
                    del st.session_state["prod_up"]
                st.success("සාර්ථකව එකතු කරන ලදී!")
                st.rerun()

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
