
import streamlit as st
import database


# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="Student Complaint Tracker",
    page_icon="🎓",
    layout="wide"
)


# ==============================
# ADMIN LOGIN
# ==============================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


# ==============================
# CREATE DATABASE
# ==============================

database.create_table()


# ==============================
# CUSTOM STYLE
# ==============================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# TITLE
# ==============================

st.markdown(
    '<div class="main-title">🎓 Student Complaint Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">College Complaint Management System</div>',
    unsafe_allow_html=True
)


# ==============================
# LOGIN SESSION
# ==============================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# ==============================
# SIDEBAR
# ==============================

if st.session_state.admin_logged_in:

    menu = st.sidebar.selectbox(
        "📌 Select Page",
        [
            "Submit Complaint",
            "View Complaints",
            "Admin Dashboard"
        ]
    )

else:

    menu = st.sidebar.selectbox(
        "📌 Select Page",
        [
            "Submit Complaint",
            "View Complaints",
            "Admin Login"
        ]
    )


# ==============================
# SUBMIT COMPLAINT
# ==============================

if menu == "Submit Complaint":

    st.header("📝 Submit a Complaint")

    st.info(
        "Please enter your details and describe your complaint clearly."
    )

    name = st.text_input("👤 Student Name")

    email = st.text_input("📧 Email")

    category = st.selectbox(
        "📂 Complaint Category",
        [
            "Academic",
            "Classroom",
            "Hostel",
            "Food",
            "Transport",
            "Other"
        ]
    )

    complaint = st.text_area(
        "💬 Complaint",
        height=150
    )

    if st.button(
        "📤 Submit Complaint",
        use_container_width=True
    ):

        if name and email and complaint:

            database.add_complaint(
                name,
                email,
                category,
                complaint
            )

            st.success(
                "✅ Complaint submitted successfully!"
            )

        else:

            st.warning(
                "⚠️ Please fill all fields."
            )


# ==============================
# VIEW COMPLAINTS
# ==============================

elif menu == "View Complaints":

    st.header("📋 Track Complaints")

    complaints = database.get_complaints()

    if complaints:

        for c in complaints:

            with st.container(border=True):

                st.subheader(
                    "🎫 Complaint ID: " + str(c[0])
                )

                st.write(
                    "**👤 Student:**",
                    c[1]
                )

                st.write(
                    "**📧 Email:**",
                    c[2]
                )

                st.write(
                    "**📂 Category:**",
                    c[3]
                )

                st.write(
                    "**💬 Complaint:**",
                    c[4]
                )

                st.write(
                    "**📌 Status:**",
                    c[5]
                )

                if c[6]:

                    st.write(
                        "**👨‍💼 Admin Response:**",
                        c[6]
                    )

    else:

        st.info(
            "📭 No complaints found."
        )


# ==============================
# ADMIN LOGIN
# ==============================

elif menu == "Admin Login":

    st.header("🔐 Admin Login")

    st.info(
        "Admin access is required to manage complaints."
    )

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    if st.button(
        "🔓 Login",
        use_container_width=True
    ):

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "✅ Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password."
            )


# ==============================
# ADMIN DASHBOARD
# ==============================

elif menu == "Admin Dashboard":

    if not st.session_state.admin_logged_in:

        st.warning(
            "⚠️ Please login as admin first."
        )

        st.stop()


    st.header("👨‍💼 Admin Dashboard")

    complaints = database.get_complaints()


    # ==============================
    # STATISTICS
    # ==============================

    total = len(complaints)

    pending = 0
    in_progress = 0
    resolved = 0

    for c in complaints:

        if c[5] == "Pending":

            pending += 1

        elif c[5] == "In Progress":

            in_progress += 1

        elif c[5] == "Resolved":

            resolved += 1


    st.subheader("📊 Complaint Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Complaints",
        total
    )

    col2.metric(
        "Pending",
        pending
    )

    col3.metric(
        "In Progress",
        in_progress
    )

    col4.metric(
        "Resolved",
        resolved
    )


    st.divider()


    # ==============================
    # SEARCH
    # ==============================

    search = st.text_input(
        "🔎 Search by Student Name"
    )


    # ==============================
    # FILTERS
    # ==============================

    col1, col2 = st.columns(2)

    with col1:

        filter_status = st.selectbox(
            "📌 Filter by Status",
            [
                "All",
                "Pending",
                "In Progress",
                "Resolved"
            ]
        )

    with col2:

        filter_category = st.selectbox(
            "📂 Filter by Category",
            [
                "All",
                "Academic",
                "Classroom",
                "Hostel",
                "Food",
                "Transport",
                "Other"
            ]
        )


    # ==============================
    # FILTER COMPLAINTS
    # ==============================

    filtered_complaints = []

    for c in complaints:

        if search.lower() not in c[1].lower():

            continue

        if (
            filter_status != "All"
            and c[5] != filter_status
        ):

            continue

        if (
            filter_category != "All"
            and c[3] != filter_category
        ):

            continue

        filtered_complaints.append(c)


    # ==============================
    # DISPLAY COMPLAINTS
    # ==============================

    if filtered_complaints:

        for c in filtered_complaints:

            with st.container(border=True):

                st.subheader(
                    "🎫 Complaint ID: " + str(c[0])
                )

                st.write(
                    "**Student:**",
                    c[1]
                )

                st.write(
                    "**Email:**",
                    c[2]
                )

                st.write(
                    "**Category:**",
                    c[3]
                )

                st.write(
                    "**Complaint:**",
                    c[4]
                )

                st.write(
                    "**Current Status:**",
                    c[5]
                )


                # ==============================
                # UPDATE STATUS
                # ==============================

                status_options = [
                    "Pending",
                    "In Progress",
                    "Resolved"
                ]

                current_status = c[5]

                if current_status not in status_options:

                    current_status = "Pending"

                status = st.selectbox(
                    "📌 Update Status",
                    status_options,
                    index=status_options.index(
                        current_status
                    ),
                    key="status_" + str(c[0])
                )


                # ==============================
                # ADMIN RESPONSE
                # ==============================

                response = st.text_area(
                    "💬 Admin Response",
                    value=c[6] or "",
                    key="response_" + str(c[0])
                )


                # ==============================
                # UPDATE BUTTON
                # ==============================

                if st.button(
                    "💾 Update Complaint",
                    key="update_" + str(c[0]),
                    use_container_width=True
                ):

                    database.update_complaint(
                        c[0],
                        status,
                        response
                    )

                    st.success(
                        "✅ Complaint updated successfully!"
                    )

                    st.rerun()

    else:

        st.info(
            "📭 No complaints match your search or filters."
        )


# ==============================
# LOGOUT
# ==============================

if st.session_state.admin_logged_in:

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.admin_logged_in = False

        st.rerun()
